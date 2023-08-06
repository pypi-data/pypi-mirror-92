from ._Activation import _Activation
import numpy as np

class Sigmoid(_Activation):
    """
    Sigmoid()
    
    Sigmoid activation function.
    
    Attributes
    ----------
    No Attributes needed.
    """
    def __init__(self):
        self.type = 'Sigmoid'
         
    def forward(self, input_val):
        self._prev_acti = 1 / (1 + np.exp(-input_val))
        return self._prev_acti
     
    def backward(self, dJ):
        sig = self._prev_acti
        return dJ * sig * (1 - sig)