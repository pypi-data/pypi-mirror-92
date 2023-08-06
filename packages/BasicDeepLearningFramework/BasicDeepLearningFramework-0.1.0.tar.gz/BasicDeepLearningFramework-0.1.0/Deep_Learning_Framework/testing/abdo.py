import numpy as np

def softmax_cross_entropy_loss(Z, Y=np.array([])):
    '''
    Computes the softmax activation of the inputs Z
    Estimates the cross entropy loss
    Inputs:
        Z - numpy.ndarray (n, m)
        Y - numpy.ndarray (1, m) of labels
            when y=[] loss is set to []

    Returns:
        A - numpy.ndarray (n, m) of softmax activations
        cache -  a dictionary to store the activations later used to estimate derivatives
        loss - cost of prediction
    '''
    ### CODE HERE

    A = np.exp(Z - np.max(Z, axis=0)) / np.sum(np.exp(Z - np.max(Z, axis=0)), axis=0, keepdims=True)
    # print "A : ",A
    if Y.shape[0] == 0:
        loss = []
    else:
        loss = -np.sum(Y * np.log(A + 1e-8)) / A.shape[1]
    # loss = 0.05
    cache = {}
    cache["A"] = A
    return A, cache, loss


def softmax_cross_entropy_loss_der(Y, cache):
    '''
    Computes the derivative of softmax activation and cross entropy loss
    Inputs:
        Y - numpy.ndarray (1, m) of labels
        cache -  a dictionary with cached activations A of size (n,m)
    Returns:
        dZ - numpy.ndarray (n, m) derivative for the previous layer
    '''
    #loss = y - y^
    ### CODE HERE
    A = cache["A"]
    dZ = A - Y
    return dZ