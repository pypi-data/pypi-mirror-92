from ._Optimizer import _Optimizer

class GradientDescent(_Optimizer):
    """
    Gradient descent algorithm updates the parameters by moving in the direction opposite
    to the gradient of the objective function with respect to the network parameters.
    
    Attributes
    ----------
    lr: learning rate --> {float}
        the rate of change of the weights w.r.t their gradient.
    """
    def __init__(self, lr= 0.01):
        self.lr = lr
        self.type = 'Gradient Descent'
    
    def update(self, w, b, dW, dB):
        w = w - self.lr * dW
        b = b - self.lr * dB.sum(axis= 0)
        return w, b