from easyDL import Layer
import numpy as np

class Input(Layer):
    """
    Input()
    
    Input Layer class.
    """
    def __init__(self, input_shape= None):
        self.input_shape = input_shape
        self.type = 'Input'
    
    def __call__(self, input_dim):
        self.input_dim = input_dim     
        self.output_dim = input_dim[1]*input_dim[2]*input_dim[3]
         
    def forward(self, input_val):
        Z = np.ravel(input_val).reshape(input_val.shape[0], -1)
        return Z.T
     
    def backward(self, dZ):
        dZ = dZ.reshape(self.input_dim)         
        return dZ