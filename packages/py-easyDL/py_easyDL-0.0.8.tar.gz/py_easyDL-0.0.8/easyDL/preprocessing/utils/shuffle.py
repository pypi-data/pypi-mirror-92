import numpy as np

def shuffle(X, Y):
    shuffler = np.random.permutation(len(X))
    X = X[shuffler]
    Y = Y[shuffler]
    
    return X, Y