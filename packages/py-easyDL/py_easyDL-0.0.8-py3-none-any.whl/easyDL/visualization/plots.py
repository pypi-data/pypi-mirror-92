import matplotlib.pyplot as plt
import numpy as np

def plot_losses(model):
    plt.figure(figsize=(10, 8))
    plt.xticks(np.arange(0, len(model.losses), 1))
    plt.plot(model.losses, label = 'Training loss')
    if len(model.losses_val):
        plt.plot(model.losses_val, label = 'Validation loss')
    plt.legend()
    plt.show()
    

def plot_accuracy(model):
    plt.figure(figsize=(10, 8))
    plt.xticks(np.arange(0, len(model.losses), 1))
    plt.plot(model.acc, label = 'Training accuracy')
    if len(model.acc_val):
        plt.plot(model.acc_val, label = 'Validation accuracy')
    plt.legend()
    plt.show()
    

    
    

    

