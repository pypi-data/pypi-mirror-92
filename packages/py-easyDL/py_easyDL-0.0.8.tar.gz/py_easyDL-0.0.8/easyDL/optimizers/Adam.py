from ._Optimizer import _Optimizer
import numpy as np

class Adam(_Optimizer):
    """  
    Adam maintains two histories, ‘mₜ’ similar to the history used in Momentum GD and
    ‘vₜ’ similar to the history used in RMSProp.\n
    In practice, Adam does something known as bias correction.\n
    Bias correction ensures that at the beginning of the training updates don’t behave in a weird
    manner. The key point in Adam is that it combines the advantages of Momentum
    GD (moving faster in gentle regions) and RMSProp GD (adjusting learning rate).
    
    Attributes
    ----------
    lr: learning rate --> {float}
        the rate of change of the weights w.r.t their gradient.
    beta1: {float}\n
    beta2: {float}\n
    epsilon: {float}
        a very small number added to the denominator while updating the weights to insure that
        it is not divided by zero.
    # """
    def __init__(self, lr=0.01, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.lr = lr
        self.t = 1
        self.type = 'Adam'
    def update(self, w, b, dw, db):
        ## dw, db are from current minibatch
        ## momentum beta 1
        # *** weights *** #

        self.m_dw[self.counter] = self.beta1*self.m_dw[self.counter] + (1-self.beta1)*dw
        # *** biases *** #
        self.m_db[self.counter] = self.beta1*self.m_db[self.counter] + (1-self.beta1)*db

        ## rms beta 2
        # *** weights *** #
        self.v_dw[self.counter] = self.beta2*self.v_dw[self.counter] + (1-self.beta2)*(dw**2)
        # *** biases *** #
        self.v_db[self.counter] = self.beta2*self.v_db[self.counter] + (1-self.beta2)*(db**2)

        ## bias correction
        m_dw_corr = self.m_dw[self.counter] / (1. - self.beta1 ** self.t)
        m_db_corr = self.m_db[self.counter] / (1. -self. beta1 ** self.t)
        v_dw_corr = self.v_dw[self.counter] / (1. - self.beta2 ** self.t)
        v_db_corr = self.v_db[self.counter] / (1. - self.beta2 ** self.t)
        
        self.lr_updated[self.counter] = self.lr * np.sqrt(1-self.beta2**self.t)/(1-self.beta1**self.t)
        self.t +=1
        lr = self.lr_updated[self.counter]
        ## update weights and biases
        w = w - lr*(m_dw_corr/(np.sqrt(v_dw_corr)+self.epsilon))
        b = b - lr*(m_db_corr/(np.sqrt(v_db_corr)+self.epsilon))
        
        self.counter = (self.counter + 1) % self.num_layers

        return w, b
  