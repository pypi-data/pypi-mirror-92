import numpy as np


def softmax(x):
    """
    x -- Output of the linear layer, of any shape,used for multiclass classification
    Returns:
    return -- Post-activation parameter, of the same shape as x
    cash --  for computing the backward pass efficiently
    """
    expnential = np.exp(x - np.max(x))
    cash = x
    return expnential / expnential.sum(axis=0)


def sigmoid(x):
    """
     Arguments:
     Z -- numpy array of any shape
     Returns:
     A -- output of sigmoid(z), same shape as Z
     cash -- for backpropagation
     """
    A = 1 / (1 + np.exp(-x))
    cash = x
    return A, cash


def relu(x):
    """
    x -- Output of the linear layer, of any shape
    Returns:
    Vec -- Post-activation parameter, of the same shape as Z
    cash --  for computing the backward pass efficiently
    """
    Vec = np.maximum(0, x)
    assert(Vec.shape == x.shape)
    cash = x
    return Vec, cash


def tanh(x):
    """
    x -- Output of the linear layer, of any shape
    Returns:
    result -- Post-activation parameter, of the same shape as Z
    cash -- for computing the backward pass efficiently
    """
    expnential_pos = np.exp(x)
    expnential_neg = np.exp(-x)
    result = (expnential_pos-expnential_neg)/(expnential_pos+expnential_neg)
    cash = x
    return result, x


def activate(Z, name):
    """apply activation function named 'name' to matrix z
       return new matrix activated"""
    if name == "relu":
        result, activation_cache = relu(Z)
    elif name == "sigmoid":
        result, activation_cache = sigmoid(Z)
    elif name == "tanh":
        result, activation_cache = tanh(Z)
    elif name == "softmax":
        result, activation_cache = softmax(Z)
    cash = activation_cache
    return result, cash
