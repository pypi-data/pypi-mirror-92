from easyDL import Layer

class _Activation(Layer):
    def __init__(self):
        pass
 
    def __str__(self):
        return f"{self.type} Layer"      
    
    def __call__(self, input_dim):
        self._weights = None
        self._biases = None
        self.output_dim = input_dim
        self.input_dim = input_dim
    
    def forward(self, input_val):
        pass
     
    def backward(self, dJ):
        pass