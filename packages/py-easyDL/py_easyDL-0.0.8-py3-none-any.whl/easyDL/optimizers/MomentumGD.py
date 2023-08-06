from ._Optimizer import _Optimizer

class MomentumGD(_Optimizer):
    """
    In Momentum GD, we are moving with an exponential decaying cumulative average of
    previous gradients and current gradient.
    
    Attributes
    ----------
    lr: learning rate --> {float}
        the rate of change of the weights w.r.t their gradient.
    gamma: {float}
    """
    def __init__(self, lr=0.01, gamma=0.9):
        self.gamma = gamma
        self.lr = lr
        
    def update(self, w, b, dw, db):
        # *** weights *** #
        self.v_dw[self.counter] = self.gamma * self.v_dw[self.counter] + self.lr * dw
        
        # *** biases *** #
        self.v_db[self.counter] = self.gamma * self.v_db[self.counter] + self.lr * db

        ## update weights and biases
        w = w - self.v_dw[self.counter]
        b = b - self.v_db[self.counter]
        
        self.counter = (self.counter + 1) % self.num_layers
        
        return w, b