from ._Activation import _Activation
import numpy as np

class Step(_Activation):    
    """
    Step()
    
    Binary step activation function.
    
    Attributes
    ----------
    No Attributes needed.
    """
    def __init__(self):
        self.type = 'Step'
    
    def forward(self, input_val):
        self._prev_acti = np.where(input_val > 0, 1, 0)
        return self._prev_acti
     
    def backward(self, dJ):
        return dJ * np.where(self._prev_acti != 0, 0, float("inf"))