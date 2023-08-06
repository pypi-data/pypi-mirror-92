from ._Activation import _Activation
import numpy as np

class Tanh(_Activation):
    """
    Tanh()
    
    Tanh activation function.
    
    Attributes
    ----------
    No Attributes needed.
    """
    def __init__(self):
        self.type = 'Tanh'
    
    def forward(self, input_val):
        self._prev_acti = np.tanh(input_val)
        return self._prev_acti
     
    def backward(self, dJ):
        tanh = self._prev_acti
        return dJ * (1.0 - tanh**2)
