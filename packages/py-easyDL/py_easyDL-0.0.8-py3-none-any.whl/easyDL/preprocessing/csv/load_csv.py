"""
This module loads data from a CSV file.
"""
import numpy as np
import pandas as pd

def load_csv(path, out_indicies=None, split_ratio=0.2, suffle=True):
    """
    Loading data from a CSV file.
    """
    dataframe = pd.read_csv(path)

    if out_indicies is None:
        inputs = dataframe.iloc[:, :-1].values
        outputs = dataframe.iloc[:, -1].values
    else:
        inputs = dataframe.iloc[:, :out_indicies[0]].values
        outputs = dataframe.iloc[:, out_indicies[0]:out_indicies[-1]].values

    if suffle:
        shuffler = np.random.permutation(len(inputs))
        inputs = inputs[shuffler]
        outputs = outputs[shuffler]

    train_inputs = inputs[0:int(inputs.shape[0] * (1 - split_ratio))]
    train_outputs = outputs[0:int(inputs.shape[0] * (1 - split_ratio))]
    test_inputs = inputs[int(inputs.shape[0] * (1 - split_ratio) + 1):]
    test_outputs = inputs[int(inputs.shape[0] * (1 - split_ratio)+1):]

    return (train_inputs, train_outputs), (test_inputs, test_outputs)
