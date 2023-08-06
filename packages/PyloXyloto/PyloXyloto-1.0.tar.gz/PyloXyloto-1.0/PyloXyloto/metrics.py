import numpy as np
import pandas as pd


def evaluation_metric(actual, predicted, metric):
    def confusion_matrix():
        classes = set(actual + predicted) # extract the different classes

        matrix = [[sum([(actual[i] == true_class) and (predicted[i] == predicted_class)
                        for i in range(len(actual))])
                   for predicted_class in classes]
                  for true_class in classes]

        conf_matrix = np.array(matrix)
        return conf_matrix

    # cm = confusion_matrix()
    # TP = np.sum([cm[i][i] for i in range(cm.shape[0])])
    # TN = np.sum(np.array([np.sum(np.delete(np.delete(cm, i, 0), i, 1)) for i in range(cm.shape[0])]))
    # FP = np.sum(np.sum(cm, axis=0) - TP)
    # FN = np.sum(np.sum(cm, axis=1) - TP)

    def accuracy():
        # Accuracy = (TP + TN) / (TP + TN + FP + FN)
        conf_mat = confusion_matrix()
        diagonal_sum = conf_mat.trace()
        sum_of_all_elements = conf_mat.sum()
        if sum_of_all_elements != 0:
            Accuracy = diagonal_sum / sum_of_all_elements
        else:
            Accuracy = 0
        return Accuracy

    def precision():
        # Precision = TP / (TP + FP)
        conf_mat = confusion_matrix()
        rows, columns = conf_mat.shape
        sum_of_precisions = 0
        for label in range(rows):
            col = conf_mat[:, label]
            if col.sum() != 0:
                precision_per_label = conf_mat[label, label] / col.sum()
            else:
                precision_per_label = 0
            sum_of_precisions += precision_per_label
        Precision = sum_of_precisions / rows
        return Precision

    def recall():
        # Recall = TP / (TP + FN)
        conf_mat = confusion_matrix()
        rows, columns = conf_mat.shape
        sum_of_recalls = 0
        for label in range(columns):
            row = conf_mat[label, :]
            if row.sum() != 0:
                recall_per_label = conf_mat[label, label] / row.sum()
            else:
                recall_per_label = 0
            sum_of_recalls += recall_per_label
        Recall = sum_of_recalls / columns
        return Recall

    if metric == 'confusion matrix':
        matrix = pd.DataFrame(confusion_matrix(), index=set(actual+predicted), columns=set(actual+predicted))
        return matrix
    elif metric == 'accuracy':
        return accuracy()
    elif metric == 'precision':
        return precision()
    elif metric == 'recall':
        return recall()
    elif metric == 'f1':
        # precision = TP / (TP + FP)
        # recall = TP / (TP + FN)
        if (recall() + precision()) == 0:
            F1 = 0
        else:
            F1 = (recall() * precision()) / (recall() + precision())

        return F1


