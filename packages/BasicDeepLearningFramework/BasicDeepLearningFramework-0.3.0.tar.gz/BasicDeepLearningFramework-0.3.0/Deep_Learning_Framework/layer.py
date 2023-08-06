import numpy as np
import copy
from math import sqrt
from itertools import product
from Deep_Learning_Framework import *


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
        self.firstTime = 1
        self.output_size = output_size

    def get_weights(self):
        """return weights, biases """
        return self.weights, self.bias

    def test_forward(self, x, w, b):
        input_size = len(x[0])

        # to be seeen!

        self.weights = copy.deepcopy(w)
        self.bias = copy.deepcopy(b)
        self.input = copy.deepcopy(x)
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    def forward(self, input_data):
        """
        input -- the input to the layer for forward propagation.
        Returns:
        return -- computes the output of a layer for a given input
        """
        input_size = len(input_data[0])

        # to be seeen!
        if (self.firstTime):
            self.weights = 0.1 * np.random.randn(input_size, self.output_size)
            self.bias = 0.1 * np.random.randn(1, self.output_size)
            self.firstTime = 0

        self.input = input_data

        self.output = np.dot(self.input, self.weights)
        self.output += self.bias

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
        dW = np.dot(self.input.T, dY) / m
        dB = np.squeeze(np.sum(dY, axis=0, keepdims=True)).reshape(1, dY.shape[1]) / m

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
        res = self.activation_grad(self.input) * dY
        return res


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
    def __init__(self, filters, kernel_shape=(3, 3), padding='valid', stride=1, ):
        self.stride = stride
        self.kernel_shape = kernel_shape
        self.padding = padding
        self.filters = filters
        self.initialized = False

    def conv_single_step(self, input, W, b):
        '''
        Function to apply one filter to input slice.
        :param input:[numpy array]: slice of input data of shape (f, f, n_C_prev)
        :param W:[numpy array]: One filter of shape (f, f, n_C_prev)
        :param b:[numpy array]: Bias value for the filter. Shape (1, 1, 1)
        :return:
        '''
        return np.sum(np.multiply(input, W) + float(b))

    def forward(self, X):

        '''
        forward propagation for a 3D convolution layer
        :param X: Input
        :return: Z
        '''

        (samples, prev_height, prev_width, prev_channels) = X.shape
        filter_shape_h, filter_shape_w = self.kernel_shape

        shape = (filter_shape_h, filter_shape_w, prev_channels, self.filters)
        if self.initialized == False:
            self.W, self.b = utils.glorot_uniform(shape=shape)
            self.initialized = True

        if self.padding == 'same':
            pad_h = int(((prev_height - 1) * self.stride + filter_shape_h - prev_height) / 2)
            pad_w = int(((prev_width - 1) * self.stride + filter_shape_w - prev_width) / 2)
            n_H = prev_height
            n_W = prev_width
        else:
            pad_h = 0
            pad_w = 0
            n_H = int((prev_height - filter_shape_h) / self.stride) + 1
            n_W = int((prev_width - filter_shape_w) / self.stride) + 1

        Z = np.zeros(shape=(samples, n_H, n_W, self.filters))
        self.pad_h, self.pad_w = pad_h, pad_w
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
        pad_h, pad_w = self.pad_h, self.pad_w

        (samples, prev_height, prev_width, prev_channels) = A.shape

        dA = np.zeros((samples, prev_height, prev_width, prev_channels))

        self.dW = np.zeros_like(self.W)
        self.db = np.zeros_like(self.b)

        if self.padding != 'same':
            dY_pad_h = abs(prev_height - dY.shape[1])
            dY_pad_w = abs(prev_width - dY.shape[2])
            dY = utils.pad_inputs(dY, (dY_pad_h, dY_pad_w))
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

            self.W -= learning_rate * self.dW
            self.b -= learning_rate * self.db

        return dA


class Pool(Layer):

    def __init__(self, filter_size, stride, mode):
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
                            prev_a = X[i, c, h_start:h_end, w_start:w_end]
                            max_pool = prev_a == np.max(prev_a)
                            dX[i, c, h_start:h_end, w_start:w_end] += np.multiply(max_pool, dout[i, c, h, w])
                        elif self.mode == "average":
                            average = dout[i, c, h, w] / (self.f * self.f)
                            filter_average = np.full((self.f, self.f), average)
                            dX[i, c, h_start:h_end, w_start:w_end] += filter_average

        return dX


class Conv2D(Layer):
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=0):
        super().__init__()
        self.cache = {}
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.stride = stride
        self.kernel_size = kernel_size if isinstance(kernel_size, tuple) \
            else (kernel_size, kernel_size)
        self.padding = padding
        self._init_weights(in_channels, out_channels, self.kernel_size)

    def _init_weights(self, in_channels, out_channels, kernel_size):
        scale = 2 / sqrt(in_channels * kernel_size[0] * kernel_size[1])

        self.weight = {'W': np.random.normal(scale=scale,
                                             size=(out_channels, in_channels, *kernel_size)),
                       'b': np.zeros(shape=(out_channels, 1))}

    def forward(self, X):
        """
        Forward pass for the convolution layer.

        Args:
            X: numpy.ndarray of shape (N, C, H_in, W_in).

        Returns:
            Y: numpy.ndarray of shape (N, F, H_out, W_out).
        """
        if self.padding:
            X = zero_pad(X, pad_width=self.padding, dims=(2, 3))

        self.cache['X'] = X

        N, C, H, W = X.shape
        KH, KW = self.kernel_size
        out_shape = (N, self.out_channels, 1 + (H - KH) // self.stride, 1 + (W - KW) // self.stride)
        Y = np.zeros(out_shape)
        for n in range(N):
            for c_w in range(self.out_channels):
                for h, w in product(range(out_shape[2]), range(out_shape[3])):
                    h_offset, w_offset = h * self.stride, w * self.stride
                    rec_field = X[n, :, h_offset:h_offset + KH, w_offset:w_offset + KW]
                    Y[n, c_w, h, w] = np.sum(self.weight['W'][c_w] * rec_field) + self.weight['b'][c_w]

        return Y

    def backward(self, dY, learning_rate):
        # calculating the global gradient to be propagated backwards
        # TODO: this is actually transpose convolution, move this to a util function
        X = self.cache['X']
        dX = np.zeros_like(X)
        N, C, H, W = dX.shape
        KH, KW = self.kernel_size
        for n in range(N):
            for c_w in range(self.out_channels):
                for h, w in product(range(dY.shape[2]), range(dY.shape[3])):
                    h_offset, w_offset = h * self.stride, w * self.stride
                    dX[n, :, h_offset:h_offset + KH, w_offset:w_offset + KW] += \
                        self.weight['W'][c_w] * dY[n, c_w, h, w]

        # calculating the global gradient wrt the conv filter weights
        dW = np.zeros_like(self.weight['W'])
        for c_w in range(self.out_channels):
            for c_i in range(self.in_channels):
                for h, w in product(range(KH), range(KW)):
                    X_rec_field = X[:, c_i, h:H - KH + h + 1:self.stride, w:W - KW + w + 1:self.stride]
                    dY_rec_field = dY[:, c_w]
                    dW[c_w, c_i, h, w] = np.sum(X_rec_field * dY_rec_field)

        # calculating the global gradient wrt to the bias
        db = np.sum(dY, axis=(0, 2, 3)).reshape(-1, 1)

        # caching the global gradients of the parameters
        # self.weight_update['W'] = dW
        # self.weight_update['b'] = db

        self.weight['W'] -= learning_rate * dW
        self.weight['b'] -= learning_rate * db

        return dX[:, :, self.padding:-self.padding, self.padding:-self.padding]


def zero_pad(X, pad_width, dims):
    """
    Pads the given array X with zeroes at the both end of given dims.

    Args:
        X: numpy.ndarray.
        pad_width: int, width of the padding.
        dims: int or tuple, dimensions to be padded.

    Returns:
        X_padded: numpy.ndarray, zero padded X.
    """
    dims = (dims) if isinstance(dims, int) else dims
    pad = [(0, 0) if idx not in dims else (pad_width, pad_width)
           for idx in range(len(X.shape))]
    X_padded = np.pad(X, pad, 'constant')
    return X_padded


class Pooling(Layer):
    def __init__(self, kernel_shape=(3, 3), stride=1, mode="max", name=None):
        '''

        :param kernel_shape:
        :param stride:
        :param mode:
        '''
        self.params = {
            'kernel_shape': kernel_shape,
            'stride': stride,
            'mode': mode
        }
        self.type = 'pooling'
        self.cache = {}
        self.has_units = False
        self.name = name

    def forward(self, X):
        '''

        :param X:
        :param save_cache:
        :return:
        '''

        (num_data_points, prev_height, prev_width, prev_channels) = X.shape
        filter_shape_h, filter_shape_w = self.params['kernel_shape']

        n_H = int(1 + (prev_height - filter_shape_h) / self.params['stride'])
        n_W = int(1 + (prev_width - filter_shape_w) / self.params['stride'])
        n_C = prev_channels

        A = np.zeros((num_data_points, n_H, n_W, n_C))

        for i in range(num_data_points):
            for h in range(n_H):
                for w in range(n_W):

                    vert_start = h * self.params['stride']
                    vert_end = vert_start + filter_shape_h
                    horiz_start = w * self.params['stride']
                    horiz_end = horiz_start + filter_shape_w

                    for c in range(n_C):

                        if self.params['mode'] == 'average':
                            A[i, h, w, c] = np.mean(X[i, vert_start: vert_end, horiz_start: horiz_end, c])
                        else:
                            A[i, h, w, c] = np.max(X[i, vert_start: vert_end, horiz_start: horiz_end, c])

        self.cache['A'] = X

        return A

    def create_mask(self, x):
        return x == np.max(x)

    def backward(self, dA, learning_rate):
        A = self.cache['A']
        filter_shape_h, filter_shape_w = self.params['kernel_shape']

        (num_data_points, prev_height, prev_width, prev_channels) = A.shape
        m, n_H, n_W, n_C = dA.shape

        dA_prev = np.zeros(shape=(num_data_points, prev_height, prev_width, prev_channels))

        for i in range(num_data_points):
            a = A[i]

            for h in range(n_H):
                for w in range(n_W):

                    vert_start = h * self.params['stride']
                    vert_end = vert_start + filter_shape_h
                    horiz_start = w * self.params['stride']
                    horiz_end = horiz_start + filter_shape_w

                    for c in range(n_C):

                        if self.params['mode'] == 'average':
                            da = dA[i, h, w, c]
                            dA_prev[i, vert_start: vert_end, horiz_start: horiz_end, c] += \
                                self.distribute_value(da, self.params['kernel_shape'])

                        else:
                            a_slice = a[vert_start: vert_end, horiz_start: horiz_end, c]
                            mask = self.create_mask(a_slice)
                            dA_prev[i, vert_start: vert_end, horiz_start: horiz_end, c] += \
                                dA[i, h, w, c] * mask

        return dA_prev


class BatchNorm(Layer):

    def __init__(self, beta, gamma, eps=1e-8):
        self.beta = beta
        self.gamma = gamma
        self.eps = eps

    def forward(self, x):
        # Mean of the mini-batch, mu
        mu = np.mean(x, axis=0)

        # Variance of the mini-batch, sigma^2
        var = np.var(x, axis=0)
        std_inv = 1.0 / np.sqrt(var + self.eps)

        # The normalized input, x_hat
        x_hat = (x - mu) * std_inv

        # Batch normalizing (affine) transformation
        y = self.gamma * x_hat + self.beta

        self.std_inv = std_inv
        self.x_hat = x_hat

        return y

    def backward(self, dY, learning_rate):
        # m: mini-batch size
        # d: number of dimensions
        m, d = dy.shape
        gamma, std_inv, x_hat = backprop_stuff

        # Equation 1 in paper
        dx_hat = dy * gamma

        # Equation 2, 3, 4 in paper
        # Equation 2 was rederived as the one in the paper was not simplified
        dx = std_inv * (dx_hat - np.mean(dx_hat, axis=0) - x_hat * np.mean(dx_hat * x_hat, axis=0))
        dgamma = np.sum(dy * x_hat, axis=0)
        dbeta = np.sum(dy, axis=0)

        return dx, dgamma, dbeta


class BatchNorm2D(Layer):
    def __init__(self, n_channels, epsilon=1e-5):
        self.epsilon = epsilon
        self.weight = {}
        self.cache = {}
        self.grad = {}
        self.n_channels = n_channels
        self._init_weights(n_channels)

    def _init_weights(self, n_channels):
        self.weight['gamma'] = np.ones(shape=(1, n_channels, 1, 1))
        self.weight['beta'] = np.zeros(shape=(1, n_channels, 1, 1))

    def forward(self, X):
        """
        Forward pass for the 2D batchnorm layer.

        Args:
            X: numpy.ndarray of shape (n_batch, n_channels, height, width).

        Returns_
            Y: numpy.ndarray of shape (n_batch, n_channels, height, width).
                Batch-normalized tensor of X.
        """
        mean = np.mean(X, axis=(2, 3), keepdims=True)
        var = np.var(X, axis=(2, 3), keepdims=True) + self.epsilon
        invvar = 1.0 / var
        sqrt_invvar = np.sqrt(invvar)
        centered = X - mean
        scaled = centered * sqrt_invvar
        normalized = scaled * self.weight['gamma'] + self.weight['beta']

        # caching intermediate results for backprop
        self.cache['mean'] = mean
        self.cache['var'] = var
        self.cache['invvar'] = invvar
        self.cache['sqrt_invvar'] = sqrt_invvar
        self.cache['centered'] = centered
        self.cache['scaled'] = scaled
        self.cache['normalized'] = normalized
        self.X = X
        return normalized

    def backward(self, dY, learning_rate):
        """
        Backward pass for the 2D batchnorm layer. Calculates global gradients
        for the input and the parameters.

        Args:
            dY: numpy.ndarray of shape (n_batch, n_channels, height, width).

        Returns:
            dX: numpy.ndarray of shape (n_batch, n_channels, height, width).
                Global gradient wrt the input X.
        """
        # global gradients of parameters
        dgamma = np.sum(self.cache['scaled'] * dY, axis=(0, 2, 3), keepdims=True)
        dbeta = np.sum(dY, axis=(0, 2, 3), keepdims=True)

        # caching global gradients of parameters
        # self.weight_update['gamma'] = dgamma
        # self.weight_update['beta'] = dbeta
        self.weight['gamma'] -= learning_rate * dgamma
        self.weight['beta'] -= learning_rate * dbeta

        # global gradient of the input
        # dX = self.grad['X'] * dY

        return self.local_grad(self.X) * dY

    def local_grad(self, X):
        """
        Calculates the local gradient for X.

        Args:
            dY: numpy.ndarray of shape (n_batch, n_channels, height, width).

        Returns:
            grads: dictionary of gradients.
        """
        # global gradient of the input
        N, C, H, W = X.shape
        # ppc = pixels per channel, useful variable for further computations
        ppc = H * W

        # gradient for 'denominator path'
        dsqrt_invvar = self.cache['centered']
        dinvvar = (1.0 / (2.0 * np.sqrt(self.cache['invvar']))) * dsqrt_invvar
        dvar = (-1.0 / self.cache['var'] ** 2) * dinvvar
        ddenominator = (X - self.cache['mean']) * (2 * (ppc - 1) / ppc ** 2) * dvar

        # gradient for 'numerator path'
        dcentered = self.cache['sqrt_invvar']
        dnumerator = (1.0 - 1.0 / ppc) * dcentered

        dX = ddenominator + dnumerator
        # grads = {'X': dX}
        return dX


class MaxPool2D(Layer):
    def __init__(self, kernel_size=(2, 2)):

        self.kernel_size = (kernel_size, kernel_size) if isinstance(kernel_size, int) else kernel_size

    def forward(self, X):
        N, C, H, W = X.shape
        KH, KW = self.kernel_size

        grad = np.zeros_like(X)
        Y = np.zeros((N, C, H // KH, W // KW))

        # for n in range(N):
        for h, w in product(range(0, H // KH), range(0, W // KW)):
            h_offset, w_offset = h * KH, w * KW
            rec_field = X[:, :, h_offset:h_offset + KH, w_offset:w_offset + KW]
            Y[:, :, h, w] = np.max(rec_field, axis=(2, 3))
            for kh, kw in product(range(KH), range(KW)):
                grad[:, :, h_offset + kh, w_offset + kw] = (X[:, :, h_offset + kh, w_offset + kw] >= Y[:, :, h, w])

        # storing the gradient
        self.grad = grad

        return Y

    def backward(self, dY, learning_rate):
        dY = np.repeat(np.repeat(dY, repeats=self.kernel_size[0], axis=2),
                       repeats=self.kernel_size[1], axis=3)
        return self.grad * dY

    # def local_grad(self, X):
    #     # small hack: because for MaxPool calculating the gradient is simpler during
    #     # the forward pass, it is calculated there and this function just returns the
    #     # grad dictionary
    #     return self.grad
