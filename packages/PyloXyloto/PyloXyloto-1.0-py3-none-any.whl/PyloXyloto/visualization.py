import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def visualize(x, y):
    """
    draw live visualization for error vs epoch
    :param x: range of x axis
    :param y: list of error per epoch to be visualized
    :return: live graph for error per each epoch
    """
    plt.style.use('fivethirtyeight')

    def animate(i):
        x_values = pd.DataFrame(x)
        y_values = pd.DataFrame(y)
        plt.cla()
        plt.plot(x_values, y_values)
        plt.xlabel('Epoch')
        plt.ylabel('Error')
        plt.title('Error per epoch')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, 5000)

    plt.tight_layout()
    plt.show(block=False)
    plt.pause(0.9)
    plt.close()


def draw(x, y, x_label, y_label):
    """
        visualize the given data
        :param x: range of x axis
        :param y: list of values to be visualized
        :return: graph for given data
        """
    plt.style.use('fivethirtyeight')

    def animate(i):
        x_values = pd.DataFrame(x)
        y_values = pd.DataFrame(y)
        plt.cla()
        plt.plot(x_values, y_values)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, 5000)

    plt.tight_layout()
    plt.show()
    plt.close()


def show_image(x_test, y_test, y_predicted):
    """
    show the images that we are predicting and the predicted value for it
    :param x_test: data that we want to predict it
    :param y_test: correct labels
    :param y_predicted: predicted values
    :return: images with their correct labels and predicted values
    """
    i = 0
    for test, true in zip(x_test, y_test):
        image = np.reshape(test, (28, 28))
        plt.imshow(image, cmap='binary')
        plt.show(block=False)
        plt.pause(1)
        plt.close()
        pred = y_predicted[i]
        idx = np.argmax(pred)
        idx_true = np.argmax(true)
        i += 1
        print('pred: %s, prob: %.2f, true: %d' % (idx, pred[idx], idx_true))
        # prob refers to the percentage of predicting this element (the most predicted value)
