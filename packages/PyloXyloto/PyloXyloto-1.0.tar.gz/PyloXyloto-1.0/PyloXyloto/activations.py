import numpy as np


# sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    y = sigmoid(x)
    return y * (1-y)


# tanh function
def tanh(x):
    return np.tanh(x)


def tanh_derivative(x):
    y = tanh(x)
    return 1 - (y**2)


# Relu function
def relu(x):
    return x*(x > 0)


def relu_derivative(x):
    return 1*(x > 0)


# identity function
def identity(x):
    return x


def identity_derivative():
    return 1


# sign function
def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def softmax(X):
    exp_x = np.exp(X)
    probs = exp_x / np.sum(exp_x, axis=1, keepdims=True)
    return probs
