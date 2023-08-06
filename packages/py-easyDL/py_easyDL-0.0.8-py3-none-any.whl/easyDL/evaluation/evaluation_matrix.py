import numpy as np
import pandas as pd

def calculate_scores(true, predictions):
    num_classes = len(set(true))
    precisions = np.zeros((num_classes), dtype= np.float32)
    recalls = np.zeros((num_classes), dtype= np.float32)
    f1_scores = np.zeros((num_classes), dtype= np.float32)
    for i in range(num_classes):
        TP = FP = TN = FN = 0
        ind_in_targets = np.where(i == true)[0]
        ind_in_preds = np.where(i == predictions)[0]
        ind_not_in_targets = np.where(i != true)[0]
        ind_not_in_preds = np.where(i != predictions)[0]
        for ind in ind_in_targets:
            if ind in ind_in_preds:
                TP += 1
            else:
                FP += 1
        for ind in ind_not_in_targets:
            if ind in ind_not_in_preds:
                TN += 1
            else:
                FN += 1
        precisions[i] = TP / (TP + FP)
        recalls[i] = TP / (TP + FN)
        f1_scores[i] = (2 * precisions[i] * recalls[i]) / (precisions[i] + recalls[i])
    return f1_scores, precisions, recalls

def plot_evaluation_matrix(targets, predictions):
    f1_scores, precisions, recalls = calculate_scores(targets, predictions)
    dictionary = {'Precision': precisions,
                'Recall': recalls,
                'F1 Score': f1_scores }
    
    df = pd.DataFrame(dictionary)
    
    print(df)