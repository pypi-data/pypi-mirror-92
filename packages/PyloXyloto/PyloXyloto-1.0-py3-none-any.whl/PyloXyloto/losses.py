import numpy as np
from PyloXyloto.activations import softmax


def mse(y, y_hat, x):  # Mean Square Error Loss
    loss_sum = np.sum((y_hat - y) ** 2, axis=1, keepdims=True)
    mse_loss = np.mean(loss_sum)
    return mse_loss


def mse_derivative(y, y_hat, x):
    grads = (2 * (y_hat - y)) / y.shape[0]
    return grads


def perceptron_criterion(y, y_hat, x):
    loss_sum = np.sum(np.maximum(0, -y * y_hat))
    perceptron_loss = np.mean(loss_sum)
    return perceptron_loss


def perceptron_criterion_derivative(y, y_hat, x):
    grads = -y * (y * y_hat <= 0)  # -y
    return grads


def hinge(y, y_hat, x):
    loss_sum = np.sum(np.maximum(0, 1 - y * y_hat))
    hinge_loss = np.mean(loss_sum)
    return hinge_loss


def hinge_derivative(y, y_hat, x):
    grads = -y * (y * y_hat <= 1)  # -y
    return grads


def crossentropy(y, y_hat, x):  # negative log likelihood
    probs = softmax(y_hat)
    log_probs = -np.log([probs[i, y_hat[i]] for i in range(len(probs))])
    loss = np.mean(log_probs)
    return loss


def crossentropy_derivative(y, y_hat, x):
    probs = softmax(y_hat)
    ones = np.zeros_like(probs)
    for i, j in enumerate(y_hat):
        ones[i, j] = 1.0

    grads = (probs - ones) / float(len(y))
    return grads


def log_likelihood_identity(y, y_hat, x):  # for logistic regression with identity activation function
    loss = np.sum((np.log(1 + np.exp(-y*y_hat))))
    return loss


def log_likelihood_identity_derivative(y, y_hat, x):
    grads = -y * np.exp(-y*y_hat) / (1 + np.exp(-y*y_hat))
    return grads


def log_likelihood_sigmoid(y, y_hat, x):  # for logistic regression with sigmoid activation function
    loss_sum = -np.sum((np.log(np.abs(y/2 + y_hat - 0.5))))
    loss = np.mean(loss_sum)
    return loss


def log_likelihood_sigmoid_derivative(y, y_hat, x):
    grads = -np.sign(y/2 + y_hat - 0.5) / np.abs(y/2 + y_hat - 0.5)
    return grads
