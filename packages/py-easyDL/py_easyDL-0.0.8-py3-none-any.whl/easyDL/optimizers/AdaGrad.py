from ._Optimizer import _Optimizer
import numpy as np

class AdaGrad(_Optimizer):
    """
    The main motivation behind the AdaGrad was the idea of Adaptive Learning rate for
    different features in the dataset, i.e.instead of using the same learning rate across
    all the features in the dataset, we might need different learning rate for different features.
    
    Attributes
    ----------
    lr: learning rate --> {float}
        the rate of change of the weights w.r.t their gradient.
    epsilon: {float}
        a very small number added to the denominator while updating the weights to insure that
        it is not divided by zero.
    """
    def __init__(self, lr=0.01, epsilon=1e-8):
        self.epsilon = epsilon
        self.lr = lr
        
    def update(self, w, b, dw, db):
        # *** weights *** #
        self.v_dw[self.counter] = self.v_dw[self.counter] + (dw**2)
        
        # *** biases *** #
        self.v_db[self.counter] = self.v_db[self.counter] + (db**2)

        ## update weights and biases
        w = w - self.lr*(dw/(np.sqrt(self.v_dw[self.counter])+self.epsilon))
        b = b - self.lr*(db/(np.sqrt(self.v_db[self.counter])+self.epsilon))
        
        self.counter = (self.counter + 1) % self.num_layers
        
        return w, b