import numpy as np
from easyDL import Layer

class MeanSquaredError(Layer):
    def __init__(self, pred, real):
        self.type = 'Mean Squared Error'  
        self.predicted = pred
        self.real = real
     
    def forward(self):
        return np.power(self.predicted - self.real, 2).mean()
 
    def backward(self):
        return 2 * (self.predicted - self.real).mean()