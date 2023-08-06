from easyDL import Layer

class _Optimizer(Layer):
    def __init__(self):
        pass
    
    def set_num_layers(self, num_layers):
        self.num_layers = num_layers
        self.v_dw = [0]*num_layers
        self.v_db = [0]*num_layers
        self.m_dw = [0]*num_layers
        self.m_db = [0]*num_layers
        self.lr_updated = [0]*num_layers
        self.counter = 0
        
    def update(self):
        pass