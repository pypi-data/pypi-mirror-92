from ._Activation import _Activation
import numpy as np

class Softmax(_Activation):
    """
    Softmax()
    
    Softmax activation function.
    
    Attributes
    ----------
    No Attributes needed.
    """
    def __init__(self):
        self.type = 'Softmax'
    
    def forward(self, input_val):
        # print(input_val)
        self._prev_acti = np.exp(input_val, dtype='float64') / (np.sum(np.exp(input_val, dtype='float64'), axis=0, dtype='float64'))
        return self._prev_acti
     
    def backward(self, dJ):
        return dJ.T