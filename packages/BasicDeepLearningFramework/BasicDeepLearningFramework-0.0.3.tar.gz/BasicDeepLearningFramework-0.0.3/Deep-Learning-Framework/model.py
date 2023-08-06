import numpy as np 
class Model:
    def __init__(self, training_method):
        self.training_method = training_method
        self.layers = []
        self.err = 0
        self.loss = None
        self.loss_prime = None
        self.losses = []

    def get_losses(self):
        "return losses"
        return self.losses


    # add layer to network
    def add(self, layer):
        '''
        adds layers to the model
        :param layer: a NN layer
        '''
        self.layers.append(layer)

    def use(self, loss, loss_prime):
        '''
        sets the used loss function
        :param loss:
        :param loss_prime:
        :return:
        '''
        self.loss = loss
        self.loss_prime = loss_prime


    def predict(self, input_data):
        '''
        predict X for given input
        :param input_data: the input data
        :return:
        '''
        # sample dimension first
        samples = len(input_data)
        result = []

        # run network over all samples
        for i in range(samples):
            # forward propagation
            X = input_data[i]
            for layer in self.layers:
                X = layer.forward(X)
            result.append(X)

        return result

    def train(self,X,Y, learning_rate):
        '''
        train  on sample data
        :param X: data sample
        :param Y: true values
        :param learning_rate: learning rate

        '''

        for layer in self.layers:
            X = layer.forward(X)

        # compute loss (for display purpose only)

        self.err += self.loss(X, Y)


        # backward propagation
        error = self.loss_prime(X, Y)
        for layer in reversed(self.layers):
            error = layer.backward(error, learning_rate)




    def fit(self, x_train, y_train, epochs, learning_rate):
        '''

        train the model on the dataset
        :param x_train: the training data
        :param y_train: the true values
        :param epochs: number of epochs
        :param learning_rate: the learning rate of the parameters

        '''
        # sample dimension first
        samples = len(x_train)

        # training loop
        for i in range(epochs):
            self.err = 0
            if(self.training_method =='online'):
                for j in range(samples):
                    # forward propagation

                    sh_x = list(x_train.shape) #shape of input, can be any dimension
                    sh_x[0] = 1  
                    X = x_train[j,: ]   #will cut the first input dimension
                    X = X.reshape( sh_x )  # will make it 1 * (dimensions)

                    sh_y = list(y_train.shape) #shape of input, can be any dimension
                    sh_y[0] = 1  
                    Y = y_train[j,: ]   #will cut the first input dimension
                    Y = Y.reshape( sh_y )  # will make it 1 * (dimensions)
                    
                    self.train(X,Y,learning_rate)
                    
            elif (self.training_method =='batch'):
                   batch_size = 100
                   num_of_batches = max(1, samples/batch_size)
                   j = 0
                   for j in range(int(num_of_batches)):
                        begin_index = j*batch_size
                        end_index = min (samples, begin_index+batch_size)
                        current_batch_size = end_index-begin_index

                        sh_x = list(x_train.shape) #shape of input, can be any dimension
                        sh_x[0] = current_batch_size 
                        X = x_train[ begin_index:end_index ,: ]   #will cut the first input dimension
                        X = X.reshape( sh_x )  # will make it 1 * (dimensions)
                        #X = x_train[begin_index:end_index , :].reshape(current_batch_size,x_train.shape[1])
                        
                        sh_y = list(y_train.shape) #shape of input, can be any dimension
                        sh_y[0] = current_batch_size  
                        Y = y_train[begin_index:end_index ,: ]   #will cut the first input dimension
                        Y = Y.reshape( sh_y )  # will make it 1 * (dimensions)
                        #Y = y_train[begin_index:end_index , : ].reshape(current_batch_size,y_train.shape[1])
                        
                        self.train(X,Y,learning_rate)



            # calculate average error on all samples

            self.err /= samples

            print('epoch %d/%d   error=%f' % (i+1, epochs, self.err))
            self.losses.append(self.err)
