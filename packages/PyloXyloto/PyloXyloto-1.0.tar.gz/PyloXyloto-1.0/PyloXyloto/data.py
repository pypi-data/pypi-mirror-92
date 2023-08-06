import pandas as pd
import numpy as np


def load_data(file_path):
    """
    :param file_path: dataset in csv file assuming label is the first column
    :return: x, y  indicating inputs and corresponding labels
    """
    df = pd.read_csv(file_path, na_values=' ', keep_default_na=False)
    x = df.iloc[:, 1:]
    y = df.iloc[:, 0:1]
    return df, x, y


def save_data(data, file_name, file_extension):
    if file_extension == 'csv':
        data.to_csv('{}.{}'.format(file_name, file_extension))
    elif file_extension == 'xlsx':
        data.to_excel('{}.{}'.format(file_name, file_extension))


def split_data(df, percentage=0.8):
    """
    like train_test_split function in sklearn, it shuffles dataset randomly and return x_train, x_test, y_train, y_test
    :param df: dataset
    :param percentage: required percentage for training dataset and the rest of dataset will be assigned for testing
    :return: x_train, x_test, y_train, y_test
    """
    train = df.sample(frac=percentage)
    test = df.drop(train.index)
    x_train = train.iloc[:, 1:].values
    x_test = test.iloc[:, 1:].values
    y_train = train.iloc[:, 0:1].values
    y_test = test.iloc[:, 0:1].values

    return x_train, x_test, y_train, y_test


def normalize_data(data):
    """
    normalize the given dataset using min-max normalization
    :param data: given dataset
    :return: normalized dataset (between 0 and 1)
    """
    normalized_data = []
    for i in range(len(data)):
        normalized_sample = []
        x = (data[i] - np.min(data[i])) / np.ptp(data[i])
        normalized_sample.append(x)
        normalized_data.append(normalized_sample)

    return np.array(normalized_data)

