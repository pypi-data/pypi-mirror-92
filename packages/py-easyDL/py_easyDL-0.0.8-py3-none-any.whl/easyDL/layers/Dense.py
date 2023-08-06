from easyDL import Layer
import numpy as np

class Dense(Layer):
    """
    Dense(input_dim, output_dim)
    
    Dense Layer class.

    Attributes
    ----------
    input_shape : int
        Dimensions of the input of the first layer of the network (Data dimensions).
    output_dim : int
        Output dimensions of the layer.
    """
    def __init__(self, output_dim, input_shape= None):
        self.input_shape = input_shape         
        self.output_dim = output_dim
        self.type = 'Dense'
   
    def __call__(self, input_dim):
        self.input_dim = input_dim
        # self._weights = np.random.randn(self.output_dim, self.input_dim)
        #Xavier Initilization
        scale = 1/np.maximum(1., (self.output_dim+self.input_dim)/2.)
        limit = np.sqrt(3.0 * scale)
        self._weights = np.random.uniform(-limit, limit, size=(self.output_dim,self.input_dim))
        self._biases = np.random.uniform(-limit, limit, size=(self.output_dim, 1))
    def forward(self, input_val):
        """
        This function performs the forwards propagation using activations from previous layer
        Args:
            A_prev:  Activations/Input Data coming into the layer from previous layer
        """
        self.A_prev = input_val
        Z = np.dot(self._weights, self.A_prev) + self._biases
        return Z
    
    def backward(self, dZ):
        """
        This function performs the back propagation using upstream gradients
        Args:
            dZ: gradient coming in from the upper layer to couple with local gradient
        """
        self._dw = np.dot(dZ, self.A_prev.T)
        self._db = np.sum(dZ, axis= 1, keepdims= True)
        
        delta = np.dot(self._weights.T, dZ)
         
        return delta
    
    def optimize(self, optimizer):
        """
        This function performs the gradient descent update
        Args:
            optimizer: optimizer.
        """
        self._weights, self._biases = optimizer.update(self._weights, self._biases, self._dw, self._db)
