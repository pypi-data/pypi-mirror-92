import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from prettytable import PrettyTable


def confusionmatrix(currentDataClass, predictedClass):
    classes = set(currentDataClass)
    number_of_classes = len(classes)
    conf_matrix = pd.DataFrame(np.zeros((number_of_classes, number_of_classes),dtype=int), index=classes, columns=classes)
    for i, j in zip(currentDataClass,predictedClass):
        conf_matrix.loc[i, j] += 1
    fp = conf_matrix.sum(axis=0) - np.diag(conf_matrix)
    fn = conf_matrix.sum(axis=1) - np.diag(conf_matrix)
    tp = np.diag(conf_matrix)
    tn = conf_matrix.values.sum() - (fp + fn + tp)
    accuracy = (tp+tn)/(tp+tn+fp+fn)
    precision = tp / (tp+fp)
    recall = tp / (tp+fn)
    f1score = (2*tp) / ((2*tp)+fp+fn)
    plt.figure(figsize=(10,7))
    sn.set(font_scale=1.4) # for label size
    sn.heatmap(conf_matrix, annot=True, annot_kws={"size": 16}) # font size
    plt.xlabel('Predicted', size=20);
    plt.ylabel('Target', size=20)
    plt.title('Confusion Matrix', fontsize=18)
    plt.show()
    print(conf_matrix.values)
    x = PrettyTable()
    x.field_names = ["FP", "FN", "TP", "TN", "Accuracy", "Precision", "Recall", "F1 score"]
    x.add_row([fp, fn, np.diagflat(tp), tn, accuracy, precision, recall, f1score])
    print(x)


