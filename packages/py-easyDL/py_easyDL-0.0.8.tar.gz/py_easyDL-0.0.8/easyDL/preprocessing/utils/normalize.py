"""
This module normalizes the inputs.
"""
import numpy as np

def normalize(inputs):
    """
    Normalizing the inputs.
    """
    epsilon = 1e-8
    return (inputs - np.mean(inputs)) / np.std(inputs + epsilon)
