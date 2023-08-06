import numpy as np
 
class Loss:
    '''
    class for losses have two function for every type of loss functions 
    1-Forward function 
    error of X with respect to Y_labels.
    Args:
        X: numpy.ndarray of shape (n_batch, n_dim) which (WX).
        Y: numpy.ndarray of shape (n_batch, n_dim) which (Y_labels).
    Returns:
        loss: numpy.mean.float.
    2- Prima function
    differencation of loss function with respect to X at (X, Y).
    Args:
        X: numpy.ndarray of shape (n_batch, n_dim) which (WX).
        Y: numpy.ndarray of shape (n_batch, n_dim) which (Y_labels).
    Returns:
        gradX: numpy.ndarray of shape (n_batch, n_dim) which differencation of loss function
    '''
    def MeanSquareLoss(self, Y_hat , Y):
        '''
            A function to get totel loss by Mean Square Loss (Y - Y_hat)**2
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted  .
            :return : total loss  
        '''
        Msq_loss = np.mean((Y_hat - Y)**2)
        return Msq_loss

    def max_Loss(self , Y_hat , Y):
        '''
            A function to get totel loss by 1/n ( max (0 , - Y * Y_hat)).
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : total loss  
        '''
        cal_arr = np.array(-1 * Y_hat * Y)
        for i in range(len(cal_arr)):
            if cal_arr[i] < 0 :
                cal_arr[i] = 0
        max_loss = (-1 * np.mean(cal_arr))
        return max_loss

    def forward_log_sigmoid_loss(self , Y_hat , Y):
        '''
            A function to get totel loss by -log ( | y/2 - 1/2 + WX|).
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : total loss  
        '''
        differences = ( Y / 2) - 0.5 + Y_hat
        for i in range(len(differences)):
            if differences [ i ] < 0:
                differences [ i ] *= -1
        loss_li = -1 * np.log(differences) 
        log_loss = np.mean(loss_li)
        return log_loss

    def forward_log_identity_loss(self , Y_hat , Y):
        '''
            A function to get totel loss by log ( 1+ exp (- Y WX)).
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : total loss  
        '''
        differences = 1 + np.exp(-1*Y*Y_hat)
        for i in range(len(differences)):
            if differences [ i ] < 0:
                differences [ i ] *= -1
        loss_li =  np.log(differences) 
        log_loss = np.mean(loss_li)
        return log_loss

    def prime_MeanSquareLoss(self , Y_hat , Y):
        '''
            A function to get differencation of loss "log ( 1+ exp (- Y WX))".
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : prime of MeanSquareLoss.
        '''
        grads = (2 * (Y_hat - Y ))/ len(Y)
        return grads
    
    def prime_maxLoss(self ,Y_hat , Y ):
        '''
            A function to get differencation of max loss as "-Y * Data".
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : prime of MeanSquareLoss.
        '''
        grads = (-1 * Y ) / len(Y)
        return grads

    def prime_logIdentityLoss(self , Y , Y_hat ):
        '''
            A function to get differencation of logIdentity loss as "-Y / 1+e^(-Y Y_hat) * Data".
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : prime of MeanSquareLoss.
        '''
        grads = (-1 * Y * np.exp(-1*Y*Y_hat) ) / ((1 + np.exp(-1*Y*Y_hat))*len(Y))
        return grads
    
    def prime_logSigmoidLoss(self , Y , Y_hat ):
        '''
            A function to get differencation of logSigmoid loss as "-Y / 1+e^(-Y Y_hat) * Data".
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : prime of MeanSquareLoss.
        '''
        grads = (-1 * Y ) / (1 + np.exp(-1*Y*Y_hat))
        return grads

    def softmax( self, x , y ):
        '''
            A function to get totel loss for softmax layer .
            :param x    : numpy array of Y labeled of data .
            :param y    : numpy array of Y predicted  "2D" for Multiclasses.
            :return : total loss  
        '''
        totel_loss = 0
        softmax_layer = []
        for i in range (len(y)):
            softmax_layer.append(np.exp(x[i][y[i]-1])/(np.exp(x[i])).sum())
            totel_loss += (-1 *(np.log(softmax_layer[i])))
        return totel_loss

    def softmax_grad( self , X_list , y_labeled_value ): 
        '''
            A function to get grad of softmax layer .
            :param y_labeled_value : numpy array of Y labeled .
            :param X_list          : numpy array of X is output of final layer.
            :return : numpy array of X is output of grad with dim X_list*No_of_output.
        '''
        no_of_output = X_list[0]
        exp_x = np.exp( X_list)
        s = exp_x/np.sum(exp_x, axis=1, keepdims=True)
        jacobian_m = np.zeros_like(s)
        for i in range(len(X_list)):
            for j in range(len(no_of_output)):
                if j == (y_labeled_value -1).any() :
                    jacobian_m[i][j] = (-1)* (1-s[i][j])
                else: 
                    jacobian_m[i][j] = s[i][j]
        return jacobian_m


    def forward_CrossEntropy(self, X, y):
        exp_x = np.exp(X)
        probs = exp_x/np.sum(exp_x , axis=1 , keepdims=True)
        log_probs = -1 * np.log([probs[i, y[i]] for i in range(len(probs))])
        crossentropy_loss = np.mean(log_probs)
        return crossentropy_loss 

    def prime_CrossEntropy(self, X, Y):
        exp_x = np.exp(X)
        probs = exp_x/np.sum(exp_x, axis=1, keepdims=True)
        ones = np.zeros_like(probs)
        for row_idx, col_idx in enumerate(Y):
            ones[row_idx, col_idx] = 1.0

        grads =  (probs - ones)/float(len(X))
        return grads


'''
testcase for softmax loss
'''
# a = Loss()
# x = np.array([[4,2,3]])
# y = np.array([[1]])
# print (a.softmax_grad(x,y))


# a = Loss()
# x = np.array([[4,2,3] ,[4,2,3]])
# y = np.array([1,2])
# print (a.softmax_grad(x,y))

