from ._Optimizer import _Optimizer
import numpy as np

class RMSProp(_Optimizer):
    """
    In RMSProp history of gradients is calculated using an exponentially decaying
    average unlike the sum of gradients in AdaGrad, which helps to prevent the rapid growth of
    the denominator for dense features.
    
    Attributes
    ----------
    lr: learning rate --> {float}
        the rate of change of the weights w.r.t their gradient.
    beta: {float}\n
    epsilon: {float}
        a very small number added to the denominator while updating the weights to insure that
        it is not divided by zero.
    """
    def __init__(self, lr=0.01, beta=0.9, epsilon=1e-8):
        self.beta = beta
        self.epsilon = epsilon
        self.lr = lr
        self.type = 'RMSProp'
        
    def update(self, w, b, dw, db):
        # *** weights *** #
        self.v_dw[self.counter] = self.beta*self.v_dw[self.counter] + (1-self.beta)*(dw**2)
        
        # *** biases *** #
        self.v_db[self.counter] = self.beta*self.v_db[self.counter] + (1-self.beta)*(db**2)

        ## update weights and biases
        w = w - self.lr*(dw/(np.sqrt(self.v_dw[self.counter])+self.epsilon))
        b = b - self.lr*(db/(np.sqrt(self.v_db[self.counter])+self.epsilon))

        self.counter = (self.counter + 1) % self.num_layers
        
        return w, b