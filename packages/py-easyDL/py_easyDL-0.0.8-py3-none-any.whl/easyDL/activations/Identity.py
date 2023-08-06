from ._Activation import _Activation
import numpy as np

class Identity(_Activation):    
    """
    Identity()
    
    Identity activation function.
    
    Attributes
    ----------
    No Attributes needed.
    """
    def __init__(self):
        self.type = 'Identity'
    
    def forward(self, input_val):
        self._prev_acti = np.array(input_val)
        return self._prev_acti
     
    def backward(self, dJ):
        return dJ * np.ones_like(self._prev_acti)