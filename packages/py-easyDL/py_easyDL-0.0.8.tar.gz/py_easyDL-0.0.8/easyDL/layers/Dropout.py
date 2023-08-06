from easyDL import Layer
import numpy as np

class Dropout(Layer):
    """
    Dropout(rate= 0.1)
    
    Dropout Layer class.

    Attributes
    ----------
    rate: float -> [0, 1[
        probability that given unit will not be dropped out
    """
    def __init__(self, rate= 0.1):
        self._rate = rate
        self._mask = None
        self.type = 'Flatten'
    
    def __call__(self, input_dim):
        self.output_dim = input_dim

    def _apply_mask(self, array, mask):
        array *= mask
        array /= self._rate
        return array    
    
    def forward(self, input_val, training= True):
        if training:
            self._mask = (np.random.rand(*input_val.shape) < self._rate)
            return self._apply_mask(input_val, self._mask)
        else:
            return input_val
     
    def backward(self, dZ):
        return self._apply_mask(dZ, self._mask)