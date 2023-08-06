from ._Optimizer import _Optimizer

class NesterovGD(_Optimizer):
    """
    In Nesterov Accelerated Gradient Descent we are looking forward to seeing whether
    we are close to the minima or not before we take another step based on the current gradient
    value so that we can avoid the problem of overshooting.
    
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
        w_temp = w - self.gamma * self.v_dw[self.counter]
        dw_temp = dw - self.gamma * self.v_dw[self.counter]
        w = w_temp - self.lr * dw_temp
        self.v_dw[self.counter] = self.gamma * self.v_dw[self.counter] + self.lr * dw_temp
        
        # *** biases *** #
        b_temp = b - self.gamma * self.v_db[self.counter]
        db_temp = db - self.gamma * self.v_db[self.counter]
        b = b_temp - self.lr * db_temp
        self.v_db[self.counter] = self.gamma * self.v_db[self.counter] + self.lr * db_temp
        
        self.counter = (self.counter + 1) % self.num_layers
        
        return w, b