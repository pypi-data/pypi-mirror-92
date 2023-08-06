import numpy as np
import pickle


# save model to the disk
def save_model(file_path, file_name, model):
    """
    save a model in disk in .pkl extension to be loaded  at any time
    :param file_path: path that we want to save the file at
    :param file_name: name of the file
    :param model: list containing [x_train, x_validation, y_train, y_validation, actual_labels,
    predicted_labels]
    """
    with open("{}/{}.pkl".format(file_path, file_name), "bw") as save:
        data = model
        pickle.dump(data, save)


# load model from disk
def load_model(file_path):
    """
    load data from .pkl file from disk
    assuming that data is a list containing [x_train, x_validation, y_train, y_validation, actual_labels,
    predicted_labels]
    :param file_path: file to be loaded with its full path
    :return: model data
    """
    with open(file_path, "br") as load:
        data = pickle.load(load)
    return data


# encode labels
def label_encoder(label):
    """
    encode output which is a number in range [0,i] into a vector of size i+1
    :param label: output vector to be encoded
    :return: encoded matrix represent the value of each vector value in terms of zeroes and ones
    """
    labels = set([label[i][0] for i in range(len(label))])
    encoded_label = np.zeros([len(label), len(labels)])
    for i in range(len(label)):
        index = list(labels).index(label[i][0])
        encoded_label[i][index] = 1

    return encoded_label


# decode labels
def label_decoder(label):
    decoded_label = []
    for i in range(len(label)):
        if len(label[i]) != 1:
            index = list(label[i]).index(max(list(label[i])))
            decoded_label.append(index)
        else:
            item = max(list(label[i]))
            if item > 0.5:
                decoded_label.append(1)
            else:
                decoded_label.append(0)
    return decoded_label


# decode labels in 0 and 1 representation
def identity_decoder(label):
    col = label.shape[-1]
    decoded_label = np.squeeze(np.eye(col)[np.argmax(label, axis=-1)])
    return decoded_label


# normalize data using batch normalization technique
def batch_normalization(data, epsilon=1e-6):
    """
    normalize data around zero with mean=0 and variance
    :param data: data to be normalized
    :param epsilon: epsilon value, default value is 10^-6
    :return: normalized data
    """
    normalized_data = []
    for i in range(len(data)):
        normalized_sample = []
        for j in range(len(data[i])):
            x = data[i][j] - data[i].mean(axis=0) / np.sqrt(data[i].var(axis=0)+epsilon)
            normalized_sample.append(x)
        normalized_data.append(list(normalized_sample))
    return np.array(normalized_data)


# add zero padding to the kernel un convolution
def zero_pad(x, pad_width, dims):
    """
    for convolution padding
    Pads the given array x with zeroes at the both end of given dims.
    :param x: array to be padded
    :param pad_width: width of the padding
    :param dims: dimensions to be padded
    :return: x_padded -> zero padded x
    """
    dims = dims if isinstance(dims, int) else dims
    pad = [(0, 0) if idx not in dims else (pad_width, pad_width) for idx in range(len(x.shape))]
    x_padded = np.pad(x, pad, 'constant')
    return x_padded



