from ._Activation import _Activation
import numpy as np

class LeakyReLU(_Activation):    
    """
    LeakyReLU(rate= 0)
    
    Leaky Rectified Linear Unit (LeakyReLU) activation function.
    
    Attributes
    ----------
    rate : float, [0, 1[
        The slope of the line from 0 to -inf.
    """
    def __init__(self, rate= 0):
        self.rate = rate
        self.type = 'LeakyReLU'
    
    def forward(self, input_val):
        self._prev_acti = np.where(input_val > 0, input_val, input_val * self.rate)
        return self._prev_acti
     
    def backward(self, dJ):
        dx = np.ones_like(self._prev_acti)
        dx[self._prev_acti <= 0] = self.rate
        return dJ * dx