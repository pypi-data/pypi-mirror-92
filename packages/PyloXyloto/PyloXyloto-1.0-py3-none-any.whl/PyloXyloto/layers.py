import numpy as np
from math import sqrt
from scipy import signal
from PyloXyloto.utils import zero_pad


# Base class
class Layer:
    def __init__(self):
        self.input = None
        self.output = None
        #self.weights = np.array([])
        #self.bias = np.array([])

    # computes the output Y of a layer for a given input X
    def forward_propagation(self, x):
        raise NotImplementedError

    # computes dE/dX for a given dE/dY (and update parameters if any)
    def backward_propagation(self, output_error, learning_rate):
        raise NotImplementedError


# inherit from base class Layer
class FCLayer(Layer):
    # in_size = number of input neurons
    # out_size = number of output neurons
    def __init__(self, in_size, out_size):
        super().__init__()
        # FCLayer class inherits from Layer class: Layer is the superclass, and FCLayer is the subclass
        """
        initialize training parameters using Gaussian distribution with mean of 0 and standard deviation of 1/sqrt(r)
        Where r is the number of input nodes. (Xavier Initialization)
        This ensures that all neurons in the network initially have approximately the same output distribution and 
        empirically improves the rate of convergence.
        # np.random.randn returns a matrix of random numbers drawn from a normal distribution with mean 0 and variance 1
        """
        scale = 1 / sqrt(in_size)
        self.weights = scale * np.random.rand(in_size, out_size)
        self.bias = scale * np.random.rand(1, out_size)

    # returns output for a given input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward_propagation(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)  # dE/dX = dE/dY . Wt  (Wt -> W transpose)
        weights_error = np.dot(self.input.T, output_error)  # dE/dW = Xt . dE/dY  (Xt -> X transpose)
        # dBias = output_error  ->  dE/dB = dE/dY

        # update parameters
        self.weights -= learning_rate * weights_error  # W = W - alpha * dE/dW
        self.bias -= learning_rate * output_error  # B = B - alpha * dE/dB
        return input_error


class FlattenLayer(Layer):
    # returns the flattened input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = input_data.flatten().reshape((1,-1))
        return self.output

    # Returns input_error=dE/dX for a given output_error=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    def backward_propagation(self, output_error, learning_rate):
        return output_error.reshape(self.input.shape)


class ConvLayer(Layer):
    """
    input_shape = (i,j,d)
    kernel_shape = (m,n)
    layer_depth = output_depth
    default stride = 1 & default padding = 0
    """
    def __init__(self, input_shape, kernel_shape, layer_depth, stride=1, padding=0):
        self.input_shape = input_shape
        self.input_depth = input_shape[2]
        self.kernel_shape = kernel_shape
        self.layer_depth = layer_depth
        self.stride = stride
        self.padding = padding
        self.output_shape = (((input_shape[0]-kernel_shape[0] + 2*padding)//stride)+1,
                             ((input_shape[1]-kernel_shape[1] + 2*padding)//stride)+1, layer_depth) # I1=(I0-F+2P)/S+1
        scale = 2/sqrt(self.input_depth*kernel_shape[0]*kernel_shape[1])
        self.weights = scale * np.random.rand(kernel_shape[0], kernel_shape[1], self.input_depth, layer_depth)
        self.bias = scale * np.random.rand(layer_depth)

    # returns output for a given input
    def forward_propagation(self, input):
        if self.padding:
            input = zero_pad(input, pad_width=self.padding, dims=(0, 1))

        self.input = input
        self.output = np.zeros(self.output_shape)

        for k in range(self.layer_depth):
            for d in range(self.input_depth):
                self.output[:,:,k] += signal.correlate2d(self.input[:,:,d], self.weights[:,:,d,k], 'valid')+self.bias[k]

        return self.output

    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward_propagation(self, output_error, learning_rate):
        input_error = np.zeros(self.input.shape)
        dweights = np.zeros((self.kernel_shape[0], self.kernel_shape[1], self.input_depth, self.layer_depth))
        dbias = np.zeros(self.layer_depth)

        for k in range(self.layer_depth):
            for d in range(self.input_depth):
                input_error[:,:,d] += signal.convolve2d(output_error[:,:,k], self.weights[:,:,d,k], 'full')
                dweights[:,:,d,k] = signal.correlate2d(self.input[:,:,d], output_error[:,:,k], 'valid')
            dbias[k] = self.layer_depth * np.sum(output_error[:,:,k])

        self.weights -= learning_rate*dweights
        self.bias -= learning_rate*dbias

        return input_error


class ActivationLayer(Layer):
    def __init__(self, activation, activation_derivative):
        super().__init__()
        # ActivationLayer class inherits from Layer class: Layer is the superclass, and ActivationLayer is the subclass
        self.activation = activation
        self.activation_derivative = activation_derivative

    # returns the activated input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    # Returns input_error=dE/dX for a given output_error=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    def backward_propagation(self, output_error, learning_rate):
        return self.activation_derivative(self.input) * output_error  # dE/dX = dE/dY * activation_derivative(X)


class SoftmaxLayer(Layer):
    def __init__(self, input_size):
        super().__init__()
        self.input_size = input_size

    def forward_propagation(self, input):
        self.input = input
        tmp = np.exp(input)
        self.output = tmp / np.sum(tmp)
        return self.output

    def backward_propagation(self, output_error, learning_rate):
        input_error = np.zeros(output_error.shape)
        out = np.tile(self.output.T, self.input_size) # repeat out.T by input_size times
        return self.output * np.dot(output_error, np.identity(self.input_size) - out)
