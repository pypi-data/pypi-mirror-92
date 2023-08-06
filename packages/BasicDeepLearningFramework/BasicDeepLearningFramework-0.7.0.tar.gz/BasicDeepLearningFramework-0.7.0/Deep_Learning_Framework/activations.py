import numpy as np
from numpy.core.getlimits import _register_type
from numpy.lib.function_base import kaiser

# tanh activation function 
def tanh(x):
    """
    tanh activation function
    x -- Output of the linear layer, of any shape.
    Returns:
    return -- activation of x using tanh
    """
    return np.tanh(x)

# tanh derivative
def tanh_grad(x):
    """
    derivative of the tanh function
    x -- Output of the linear layer, of any shape.
    Returns:
    return -- gradient of activation tanh(x) for back propagation
    """
    return 1-np.tanh(x)**2


# ReLU activation function
def ReLU(x):
    """
    ReLU activation function
    x -- Output of the linear layer, of any shape.
    Returns:
    return -- activation of x using RelU
    """
    return x * (x > 0)

# ReLU derivative
def ReLU_grad(x):
    """
    derivative of ReLU activation
    x -- Output of the linear layer, of any shape.
    Returns:
    return -- gradient of activation RelU(x) for back propagation
    """
    return 1 * (x>0)

# sigmoid activation function
def sigmoid(x):
    """
    sigmoid activation function
    x -- Output of the linear layer, of any shape.
    Returns:
    return -- activation of x using sigmoid
    """
    return 1/(1 + np.exp(-x))

# sigmoid derivative
def sigmoid_grad(x):
    """
    derivativre of the sigmoid
    x -- Output of the previous layer, of any shape.
    Returns:
    return -- gradient of activation sigmoid(x) for back propagation
    """
    x = sigmoid(x)
    return x * (1 - x)

def softmax(x):
    """
    softmax activation function
    x -- Output of the linear layer, of any shape.
    Returns:
    return -- activation of x using softmax
    """
    e_x = np.exp(x - np.max(x,axis=1, keepdims=True))
    e_x = e_x / np.sum(e_x, axis=1, keepdims=True)
    if(np.sum(e_x[0]) != 1.0):
        ylahwy = np.sum(e_x[0])
        print()

    return e_x
       


def softmax_grad(x):
    """
    derivative  of softmax
    x -- Output of the previous layer, of any shape.
    Returns:
    return -- gradient of activation softmax(x) for back propagation
    """
    #s = x.reshape(-1,1)
    #return np.diagflat(s) - np.dot(s, s.T)
    Z = softmax(x)
    return x * ( Z* (1 - Z))



# x = np.random.rand(100,10) * 5

# z = softmax(x)
# z = softmax_grad(z)
# print(z.shape)
# print(np.sum(z[0]))