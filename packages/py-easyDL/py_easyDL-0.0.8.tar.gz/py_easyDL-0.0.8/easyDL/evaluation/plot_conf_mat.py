import  numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd

def plot_confusion_matrix(true_labels, preds):
    true_labels=true_labels.squeeze()
    preds=preds.squeeze()
    classes=np.unique(true_labels)
    conf_matrix=np.zeros((len(classes),len(classes)), dtype= np.int32)
    for i in range(len(classes)):
        indices_of_class= np.where(true_labels == classes[i])
        for j in range(len(classes)):
            class_predictions = preds[indices_of_class]
            appearnce_count = np.count_nonzero(class_predictions == classes[j])
            if appearnce_count > 0:
                conf_matrix[i, j] = np.count_nonzero(class_predictions == classes[j])
    confusion= pd.DataFrame(conf_matrix, range(len(classes)), range(len(classes)))
    plt.figure(figsize=(10, 8))
    sn.set(font_scale=1)  # for label size
    sn.heatmap(confusion, annot= True, cmap='Blues', fmt= '.10g')  # font size
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.show()
