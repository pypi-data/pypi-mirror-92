# -*- coding: utf-8 -*-

from easyDL import Layer
import numpy as np

class BatchNorm(Layer):
    """
    BatchNorm()
    
    BatchNorm Layer class.
    """
    def __init__(self):
        self.type = 'BatchNorm'

    
    def __call__(self, input_dim):
        self.input_dim = input_dim       
        self.output_dim = input_dim
        if  isinstance(self.input_dim, int):
            shape = (self.input_dim, 1)
            scale = 1/np.maximum(1., self.input_dim)
        else:
            shape = (1, 1, 1, self.input_dim[-1])
            scale = 1/np.maximum(1., self.input_dim[-1])
        
        limit = np.sqrt(3.0 * scale)
        self._weights = np.random.uniform(-limit, limit, size=shape)
        self._biases = np.random.uniform(-limit, limit, size=shape)
         
    def forward(self, input_val):
        self._a_prev = np.array(input_val, copy=True)
        
        if len(input_val.shape) == 2:
            self._mu = np.mean(input_val,axis=(0))
            self._var = np.var(input_val,axis=(0))
        else:
            self._mu = np.mean(input_val,axis=(0, 2, 3), keepdims=True)
            self._var = np.var(input_val,axis=(0, 2, 3), keepdims=True)

        self.X_norm = (input_val - self._mu) / np.sqrt(self._var + 1e-8)
        Z = self._weights * self._a_prev + self._biases

        return Z
         
    def backward(self, dZ):


        N = self._a_prev.shape[0]

        X_mu = self._a_prev - self._mu
        std_inv = 1. / np.sqrt(self._var + 1e-8)

        dX_norm = dZ * self._weights
        dvar = np.sum(dX_norm * X_mu, axis=0) * -.5 * std_inv**3
        dmu = np.sum(dX_norm * -std_inv, axis=0) + dvar * np.mean(-2. * X_mu, axis=0)

        dX = (dX_norm * std_inv) + (dvar * 2 * X_mu / N) + (dmu / N)
        self._dw = np.sum(dZ * self.X_norm, axis=0)
        self._db = np.sum(dZ, axis=0)

        return dX