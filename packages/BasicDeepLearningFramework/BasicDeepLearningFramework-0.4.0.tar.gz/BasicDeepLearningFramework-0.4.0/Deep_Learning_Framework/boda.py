class FC(Layer):
    # input_size = number of input neurons
    # output_size = number of output neurons
    def __init__(self, output_size):
        """
        Initialization for the parameters of the class fully connected layer
        input_size = number of input neurons
        output_size = number of output neurons
        """
        self.initialized = False
        self.output_size = output_size

    def forward(self, input_data):
        """
        input -- the input to the layer for forward propagation.
        Returns:
        return -- computes the output of a layer for a given input
        """
        input_size = len(input_data[0])

        if self.initialized == False:
            self.weights = 0.1 * np.random.rand(input_size, self.output_size)
            self.bias = 0.1 * np.random.rand(1, self.output_size)
            self.initialized = True

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

        return self.activation_grad(self.input) * dY


class Conv_layer(Layer):
    def __init__(self, filters, kernel_shape=(3, 3), padding='valid', stride=1):
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
