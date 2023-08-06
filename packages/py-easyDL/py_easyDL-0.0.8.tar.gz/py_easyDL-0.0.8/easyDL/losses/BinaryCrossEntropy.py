import numpy as np
from easyDL import Layer
 
class BinaryCrossEntropy(Layer):
    def __init__(self, pred, real):
        self.type = 'Binary Cross-Entropy' 
        self.predicted = pred
        self.real = real
     
    def forward(self):
        n = len(self.real)
        loss = np.nansum(-self.real * np.log(self.predicted) - (1 - self.real) * np.log(1 - self.predicted)) / n
         
        return np.squeeze(loss)
     
    def backward(self):
        n = len(self.real)
        return (-(self.real / self.predicted) + ((1 - self.real) / (1 - self.predicted))) / n