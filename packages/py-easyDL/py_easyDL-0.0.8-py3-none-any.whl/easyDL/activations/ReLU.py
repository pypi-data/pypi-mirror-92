from ._Activation import _Activation
import numpy as np

class ReLU(_Activation):
    """
    ReLU()
    
    Rectified Linear Unit (ReLU) activation function.
    
    Attributes
    ----------
    No Attributes needed.
    """
    def __init__(self):
        self.type = 'ReLU'
    
    def forward(self, input_val):       
        self._z = np.maximum(0, input_val)
        return self._z
     
    def backward(self, dJ):
        dZ = np.array(dJ, copy=True)
        dZ[self._z <= 0] = 0
        return dZ