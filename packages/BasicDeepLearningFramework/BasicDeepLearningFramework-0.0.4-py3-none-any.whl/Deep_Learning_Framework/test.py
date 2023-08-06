
import layer
import activations
import numpy as np
import model
from activations import *


x = np.random.rand(5,28,28,3)
y = np.random.rand(5,5)

network = model.Model(training_method='patch')

layer1 = layer.Conv_layer(4,padding='same',stride=1,kernel_shape=(5,5))
network.add(layer1)
# acti = layer.ActivationLayer(ReLU,ReLU_grad)
# network.add(acti)
network.use(mse,mse_prime)

network.fit(x,y,5,0.1)



print(x)
x = np.pad(x, ( (2, 2), (1, 1)), 'constant')
print(x)
print(x.shape)