import numpy as np
import utils

# Base class for Layers
class Layer:
    def __init__(self):
        """
        Initialization for the parameters of the class layer
        """
        self.input = None
        self.output = None

    def forward(self, input):
        """
        input -- the input to the layer for forward propagation.
        Returns:
        return -- computes the output of a layer for a given input
        """
        raise NotImplementedError

    # computes dE/dX for a given dE/dY (and update parameters if any)
    def backward(self, dY, learning_rate):
        """
         input -- dY = The gradient of the error with respect to previous layer,
         input -- learning_rate = learning rate to update weights.
         Returns:
         return -- computes the gradient of the error with respect to this layer and update parameters if any.
         """
        raise NotImplementedError


class FC(Layer):
    # input_size = number of input neurons
    # output_size = number of output neurons
    def __init__(self, output_size):
        """
        Initialization for the parameters of the class fully connected layer
        input_size = number of input neurons
        output_size = number of output neurons
        """
        self.output_size = output_size
        

    def forward(self, input_data):
        """
        input -- the input to the layer for forward propagation.
        Returns:
        return -- computes the output of a layer for a given input
        """
        input_size = len(input_data[0])
    
        self.weights = 0.1 * np.random.rand(input_size, self.output_size) 
        self.bias = 0.1 * np.random.rand(1, self.output_size) 
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    def backward(self, dY, learning_rate):
        """
        input -- dY = The gradient of the error with respect to previous layer,
        input -- learning_rate = learning rate to update weights.
        Returns:
        return -- computes the gradient of the error with respect to this layer and update weights.
        """

        m = len(dY)
        grad = np.dot(dY, self.weights.T)
        dW = np.dot(self.input.T, dY)/m
        dB = np.squeeze(np.sum(dY, axis=0, keepdims=True)).reshape(1,dY.shape[1])/m

        # update parameters
        self.weights -= learning_rate * dW
        self.bias -= learning_rate * dB
        return grad

class ActivationLayer(Layer):
    def __init__(self, activation, activation_grad):
        """
        input -- activation = pass the name of the activation function,
        input -- learning_rate = pass the name of the activation function gradient.
        """

        self.activation = activation
        self.activation_grad = activation_grad

    # returns the activated input
    def forward(self, input_data):
        """
        input -- the input to the layer for forward propagation.
        Returns:
        return -- computes the output of a layer for a given input
        """

        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    # Returns grad=dE/dX for a given dY=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    def backward(self, dY, learning_rate):
        """
        input -- dY = The gradient of the error with respect to previous layer,
        input -- learning_rate = learning rate to update weights if any.
        Returns:
        return -- computes the gradient of the error with respect to this activation
        """

        return self.activation_grad(self.input) * dY

class Flatten(Layer):

    def forward(self, X):
        """
        input -- x = the input from the previous layer,
        Returns:
        return -- changes the shape of the input to flatten the input into one dimension
        extra:
        save -- save the value of the input to use it in reshaping in back propagation.
        """
        self.input = X
        samples = X.shape[0]
        return X.reshape(samples, -1)

    def backward(self, dY, learning_rate):
        """
        input -- dY = The gradient of the error with respect to previous layer,
        input -- learning_rate = learning rate to update weights if any.
        while we aren't using the input parameters but to follow the notation of backward function in all layers
        Returns:
        return -- changes the shape of the previous layer to be as the input in the forward propagation which stored in input.shape
        """
        return dY.reshape(self.input.shape)

class Conv_layer(Layer):
    def __init__(self,filters, kernel_shape=(3, 3), padding='valid', stride=1,):
        self.stride = stride
        self.kernel_shape = kernel_shape
        self.padding = padding
        self.filters = filters
        


    def conv_single_step(self, input, W, b):
        '''
        Function to apply one filter to input slice.
        :param input:[numpy array]: slice of input data of shape (f, f, n_C_prev)
        :param W:[numpy array]: One filter of shape (f, f, n_C_prev)
        :param b:[numpy array]: Bias value for the filter. Shape (1, 1, 1)
        :return:
        '''
        return np.sum(np.multiply(input, W) + float(b))
    

    def forward(self,X):
          
        '''
        forward propagation for a 3D convolution layer
        :param X: Input
        :return: Z
        '''
        
        (samples, prev_height, prev_width, prev_channels) = X.shape
        filter_shape_h, filter_shape_w = self.kernel_shape

       
        shape = (filter_shape_h, filter_shape_w, prev_channels, self.filters)
        self.W , self.b = utils.glorot_uniform(shape=shape)

        if self.padding == 'same':
            pad_h = int(((prev_height - 1)*self.stride + filter_shape_h - prev_height) / 2)
            pad_w = int(((prev_width - 1)*self.stride + filter_shape_w - prev_width) / 2)
            n_H = prev_height
            n_W = prev_width
        else:
            pad_h = 0
            pad_w = 0
            n_H = int((prev_height - filter_shape_h) / self.stride) + 1
            n_W = int((prev_width - filter_shape_w) / self.stride) + 1


        Z = np.zeros(shape=(samples, n_H, n_W, self.filters))
        self.pad_h , self.pad_w = pad_h, pad_w
        X_pad = utils.pad_inputs(X, (pad_h, pad_w))

        for i in range(samples):
            x = X_pad[i]
            for h in range(n_H):
                for w in range(n_W):
                    vert_start = self.stride * h
                    vert_end = vert_start + filter_shape_h
                    horiz_start = self.stride * w
                    horiz_end = horiz_start + filter_shape_w

                    for c in range(self.filters):

                        x_slice = x[vert_start: vert_end, horiz_start: horiz_end, :]

                        Z[i, h, w, c] = self.conv_single_step(x_slice, self.W[:, :, :, c],
                                                              self.b[:, :, :, c])
        self.A = X
        return Z

    def backward(self, dY, learning_rate):   
        '''
        backward propagation for 3D convlution layer
        :param dY: grad input
        :param learning_rate: the learning rate
        :return: dA
        '''
        A = self.A
        filter_shape_h, filter_shape_w = self.kernel_shape
        pad_h, pad_w = self.pad_h , self.pad_w

        (samples, prev_height, prev_width, prev_channels) = A.shape

        dA = np.zeros((samples, prev_height, prev_width, prev_channels))

        self.dW = np.zeros_like(self.W)
        self.db = np.zeros_like(self.b)


        if self.padding != 'same':
            dY_pad_h = abs(prev_height-dY.shape[1])
            dY_pad_w = abs(prev_width-dY.shape[2])
            dY = utils.pad_inputs(dY,(dY_pad_h,dY_pad_w))
            A_pad = utils.pad_inputs(A, (dY_pad_h, dY_pad_w))
            dA_pad = utils.pad_inputs(dA, (dY_pad_h, dY_pad_w))
            pad_h = dY_pad_h
            pad_w = dY_pad_w
        else:
            A_pad = utils.pad_inputs(A, (pad_h, pad_w))
            dA_pad = utils.pad_inputs(dA, (pad_h, pad_w))
        

        for i in range(samples):
            a_pad = A_pad[i]
            da_pad = dA_pad[i]

            for h in range(prev_height):
                for w in range(prev_width):

                    vert_start = self.stride * h
                    vert_end = vert_start + filter_shape_h
                    horiz_start = self.stride * w
                    horiz_end = horiz_start + filter_shape_w

                    for c in range(self.filters):
                        a_slice = a_pad[vert_start: vert_end, horiz_start: horiz_end, :]

                        da_pad[vert_start:vert_end, horiz_start:horiz_end, :] += self.W[:, :, :, c] * dY[i, h, w, c]
                        self.dW[:, :, :, c] += a_slice * dY[i, h, w, c]
                        self.db[:, :, :, c] += dY[i, h, w, c]
            dA[i, :, :, :] = da_pad[pad_h: -pad_h, pad_w: -pad_w, :]

            self.W  -= learning_rate * self.dW
            self.b -= learning_rate * self.db

        return dA

class Pool(Layer):

    def __init__(self, filter_size, stride,mode):
        self.f = filter_size
        self.s = stride
        self.mode = mode
        self.cache = None

    def forward(self, X):
        """
            Apply average pooling.
            Arguments:
            - X: Output of activation function.

            Returns:
            - A_pool: X after average pooling layer.
        """
        m, n_C_prev, n_H_prev, n_W_prev = X.shape

        n_C = n_C_prev
        n_H = int((n_H_prev - self.f) / self.s) + 1
        n_W = int((n_W_prev - self.f) / self.s) + 1

        A_pool = np.zeros((m, n_C, n_H, n_W))

        for i in range(m):

            for c in range(n_C):

                for h in range(n_H):
                    h_start = h * self.s
                    h_end = h_start + self.f

                    for w in range(n_W):
                        w_start = w * self.s
                        w_end = w_start + self.f
                        if self.mode == "average":
                            A_pool[i, c, h, w] = np.mean(X[i, c, h_start:h_end, w_start:w_end])
                        elif self.mode == "max":
                            A_pool[i, c, h, w] = np.max(X[i, c, h_start:h_end, w_start:w_end])

        self.cache = X

        return A_pool


    def backward(self, dout, learning_rate):
        """
            Distributes error through pooling layer.
            Arguments:
            - dout: Previous layer with the error.

            Returns:
            - dX: Conv layer updated with error.
        """
        X = self.cache
        m, n_C, n_H, n_W = dout.shape
        dX = np.zeros(X.shape)

        for i in range(m):

            for c in range(n_C):

                for h in range(n_H):
                    h_start = h * self.s
                    h_end = h_start + self.f

                    for w in range(n_W):
                        w_start = w * self.s
                        w_end = w_start + self.f
                        if self.mode == "max":
                            prev_a = X[i,c,h_start:h_end,w_start:w_end]
                            max_pool = prev_a == np.max(prev_a)
                            dX[i,c,h_start:h_end,w_start:w_end] += np.multiply(max_pool, dout[i, c, h, w])
                        elif self.mode == "average":
                            average = dout[i, c, h, w] / (self.f * self.f)
                            filter_average = np.full((self.f, self.f), average)
                            dX[i, c, h_start:h_end, w_start:w_end] += filter_average

        return dX