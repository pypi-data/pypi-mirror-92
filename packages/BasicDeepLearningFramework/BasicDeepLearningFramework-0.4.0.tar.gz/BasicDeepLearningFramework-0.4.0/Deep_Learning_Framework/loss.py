import numpy as np
from numpy.core.numeric import ones


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

    def MeanSquareLoss(self, Y_hat, Y):
        '''
            A function to get totel loss by Mean Square Loss (Y - Y_hat)**2
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted  .
            :return : total loss  
        '''
        Msq_loss = np.mean((Y_hat - Y)**2)
        return Msq_loss

    def max_Loss(self, Y_hat, Y):
        '''
            A function to get totel loss by 1/n ( max (0 , - Y * Y_hat)).
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : total loss  
        '''
        cal_arr = np.array(-1 * Y_hat * Y)
        for i in range(len(cal_arr)):
            if cal_arr[i] < 0:
                cal_arr[i] = 0
        max_loss = (-1 * np.mean(cal_arr))
        return max_loss

    def forward_log_sigmoid_loss(self, Y_hat, Y):
        '''
            A function to get totel loss by -log ( | y/2 - 1/2 + WX|).
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : total loss  
        '''
        differences = (Y / 2) - 0.5 + Y_hat
        for i in range(len(differences)):
            if differences[i] < 0:
                differences[i] *= -1
        loss_li = -1 * np.log(differences)
        log_loss = np.mean(loss_li)
        return log_loss

    def forward_log_identity_loss(self, Y_hat, Y):
        '''
            A function to get totel loss by log ( 1+ exp (- Y WX)).
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : total loss  
        '''
        differences = 1 + np.exp(-1*Y*Y_hat)
        for i in range(len(differences)):
            if differences[i] < 0:
                differences[i] *= -1
        loss_li = np.log(differences)
        log_loss = np.mean(loss_li)
        return log_loss

    def prime_MeanSquareLoss(self, Y_hat, Y):
        '''
            A function to get differencation of loss "log ( 1+ exp (- Y WX))".
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : prime of MeanSquareLoss.
        '''
        grads = (2 * (Y_hat - Y)) / len(Y)
        return grads

    def prime_maxLoss(self, Y_hat, Y):
        '''
            A function to get differencation of max loss as "-Y * Data".
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : prime of MeanSquareLoss.
        '''
        grads = (-1 * Y) / len(Y)
        return grads

    def prime_logIdentityLoss(self, Y, Y_hat):
        '''
            A function to get differencation of logIdentity loss as "-Y / 1+e^(-Y Y_hat) * Data".
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : prime of MeanSquareLoss.
        '''
        grads = (-1 * Y * np.exp(-1*Y*Y_hat)) / \
            ((1 + np.exp(-1*Y*Y_hat))*len(Y))
        return grads

    def prime_logSigmoidLoss(self, Y, Y_hat):
        '''
            A function to get differencation of logSigmoid loss as "-Y / 1+e^(-Y Y_hat) * Data".
            :param Y_hat: numpy array of Y labeled .
            :param Y    : numpy array of Y predicted .
            :return : prime of MeanSquareLoss.
        '''
        grads = (-1 * Y) / (1 + np.exp(-1*Y*Y_hat))
        return grads

    def softmax_loss(self, y_hat, y):
        '''
            A function to get totel loss for softmax layer .
            :param y_hat    : numpy array of Y labeled of data .
            :param y        : numpy array of Y predicted  "2D" for Multiclasses.
            :return : total loss  
        '''
        no_examples, no_nodes = y_hat.shape
        total_loss = []
        for i in range(no_examples):
            total_loss.append(-1 *(np.log( 0.0000000001 + y_hat[i][y[i,0]])))
        return np.sum(total_loss)

    def softmax_grad(self, y_hat, Y_label):
        '''
            A function to get grad of softmax layer .
            :param  y_hat  : numpy array of Y labeled . 'no_of_sample * no of nodes'
            :param Y_label : numpy array of X is output of final layer. 'no_of_sample * 1'
            :return : numpy array of X is output of grad with dim 'no_of_sample * no of nodes'
        '''
        no_examples, no_of_output = y_hat.shape
        jacobian_m = np.zeros_like(y_hat)

        for i in range(no_examples):
            for j in range(no_of_output):
                if j == Y_label[i]:
                    jacobian_m[i][j] = (-1)*(1-y_hat[i][j])
                else:
                    jacobian_m[i][j] = y_hat[i][j]
        return jacobian_m

    def forward_CrossEntropy(self, Y_hat , Y_label ):
        # exp_x = np.exp(X)
        # probs = exp_x/np.sum(exp_x)
        log_probs = -1 * np.log([Y_hat[i,  Y_label[i]] for i in range(len(Y_hat))])
        crossentropy_loss = np.mean(log_probs)
        return crossentropy_loss

    def prime_CrossEntropy(self, Y_hat, X):
        # exp_x = np.exp(X)
        # probs = exp_x/np.sum(exp_x, axis=1, keepdims=True)
        row_idx, col_idx = Y_hat.shape
        ones = np.zeros_like(Y_hat)
        for row_idx, col_idx in enumerate(X):
            ones[row_idx, col_idx] = 1.0     
        grads = (Y_hat - ones)/float(len(X))
        return grads


    def CrossEntropy(self,X, y):
        """
        Computes the cross entropy loss of x with respect to y.

        Args:
            X: numpy.ndarray of shape (n_batch, n_dim).
            y: numpy.ndarray of shape (n_batch, 1). Should contain class labels
                for each data point in x.

        Returns:
            crossentropy_loss: numpy.float. Cross entropy loss of x with respect to y.
        """
        # calculating crossentropy
        exp_x = np.exp(X)
        probs = exp_x/np.sum(exp_x, axis=1, keepdims=True)
        log_probs = -np.log([probs[i, y[i]] for i in range(len(probs))])
        crossentropy_loss = np.mean(log_probs)

        # caching for backprop
        # self.cache['probs'] = probs
        # self.cache['y'] = y

        return crossentropy_loss

    def CrossEntropy_grad(self,X, Y):
        #probs = self.cache['probs']
        exp_x = np.exp(X)
        probs = exp_x/np.sum(exp_x, axis=1, keepdims=True)
        ones = np.zeros_like(probs)
        for row_idx, col_idx in enumerate(Y):
            ones[row_idx, col_idx] = 1.0

        #grads = {'X': (probs - ones)/float(len(X))}
        grads =  (probs - ones)/float(len(X))
        return grads


'''
testcase for softmax loss
'''
# a = Loss()
# x = np.array([[0,0,0.2119],
# [0,0,0.2119],
# [0,0,0.5176]]
# )

# y = np.array([0,1,2])
# print(a.softmax_loss(x, y))


# a = Loss()
# x = np.array([[4,2,3] ,[4,2,3]])
# y = np.array([1,2])
# print (a.softmax_grad(x,y))
