import sys
import os
#import activations, evaluation, layers, losses, models, optimizers, preprocessing, visualization
path = os.getcwd()
parent_path = os.path.abspath(os.path.join(path, os.pardir))

if parent_path not in sys.path:
    sys.path.append(parent_path)

del path, parent_path
 
class Layer:
    """Layer abstract class"""
    def __init__(self):
        pass
     
    def __len__(self):
        pass
     
    def __str__(self):
        return "{} Layer".format(self.type)
     
    def forward(self):
        pass
     
    def backward(self):
        pass
     
    def optimize(self):
        pass


print('\nWelcome to EasyDL.')
print('Where Deep learning is meant to be easy.')
