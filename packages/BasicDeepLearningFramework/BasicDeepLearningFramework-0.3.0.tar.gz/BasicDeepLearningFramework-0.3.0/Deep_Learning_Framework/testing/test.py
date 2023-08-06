from activations import *
from Evaluation import *
from layer import *
from Load import *
from loss import *
from model import *
from save_and_load import *
from utils import *
from visualization import *


def change_to_multi (y):
    """takes y as vector , returns result as matrix"""
    res = np.zeros((len(y), np.max(y) + 1))
    res[np.arange(len(y)), y] = 1
    return res


def change_to_vector(y):
    print(len(y))
    res = []
    for i in range(len(y)):
        curr = y[i]
        res.append(int(np.argmax(curr)))
    return res



def get_params(layers):
    """get all paramerteers in all layers"""



if __name__ == '__main__':
    # train_data = Load.load.loadData('DataSet/train.csv', 'label', 0)

    # habd omar hatem
    y = 'label'
    indexY = 0
    x, y = load.loadData('../DataSet/train.csv', y, indexY)
    test_x, _ = load.loadData('../DataSet/test.csv', 'no', -1)
    x, y, _, _ = load.split_dataset(x, y, 0.001)


    x = load.normalization(x)
    y_matrix = change_to_multi(y)
    #end habd omarhatem

    # print(train_data[0].shape)

    # x = train_data[0]
    # Y = train_data[1]

    x = x.reshape(42, 28,28,1)
    # test_x = test_x.reshape(28000, 28*28)
    y_old = y
    y = y.reshape(42, 1)

    # y = np.eye(10)[y]
    # y = int(y.reshape(420,10))



    print(x.shape, y.shape)

    our_model = Model('batch')

    # Alex-net Maybee??
    # layer1 = Conv_layer(6, kernel_shape=(5,5),padding='same',stride=1)
    # layer2 = Pool(filter_size=3,stride=2,mode='max')
    # layer3 = Conv_layer(256, kernel_shape=(5,5),padding='same',stride=4)
    # layer4 = Pool(filter_size=3,stride=2,mode='max')
    # layer5 = Conv_layer(384, kernel_shape=(3,3),padding='same',stride=4)
    # layer6 = Conv_layer(384, kernel_shape=(3,3),padding='same',stride=4)
    # layer7 = Conv_layer(256, kernel_shape=(3,3),padding='same',stride=4)
    # layer8 = Pool(filter_size=3,stride=2,mode='max')
    # layer9 = Flatten()
    # layer10 = FC(4096)
    # layer11 = FC(4096)

    layer1 = Conv_layer(6, kernel_shape=(5, 5), padding='same', stride=1)
    activation1 = ActivationLayer(ReLU, ReLU_grad)
    # # layer2 = Pool(filter_size=2, stride=2, mode='average')
    # # layer3 = Conv_layer(16, kernel_shape=(5, 5), padding='same', stride=1)
    # # activation2 = ActivationLayer(ReLU, ReLU_grad)
    # layer4 = Pool(filter_size=2, stride=2, mode='average')
    layer5 = Flatten()
    layer6 = FC(120)
    layer7 = FC(84)
    layer8 = FC(10)



    our_model.add(layer1)
    our_model.add(activation1)
    # our_model.add(layer2)
    # our_model.add(layer3)
    # our_model.add(activation2)
    # our_model.add(layer4)
    our_model.add(layer5)
    our_model.add(layer6)
    our_model.add(ActivationLayer(ReLU, ReLU_grad))
    our_model.add(layer7)
    our_model.add(ActivationLayer(ReLU, ReLU_grad))
    our_model.add(layer8)
    our_model.add(ActivationLayer(softmax, softmax_grad))

    #test habd shdeeeeeeeeeeeeeeeed awy
    #working with acc 1.0 !!!!!!!!!!!
    # layer1 = FC(32)
    # activation1 = ActivationLayer(ReLU, ReLU_grad)
    # our_model.add(layer1)
    # our_model.add(activation1)
    #
    #
    #
    # layer2 = FC(10)
    # our_model.add(layer2)
    # our_model.add(ActivationLayer(softmax,softmax_grad))



    #end test habd

    our_loss = Loss()
    our_model.use(our_loss.softmax_loss, our_loss.prime_CrossEntropy)

    # plt.imshow(x[6].reshape(28, 28))
    print(y)

    print('fitting.....')
    our_model.fit(x, y, 100, 0.1)

    # w, b = our_model.get_weights()
    #
    #
    # #save weights biases
    # save_model(w, 'weights.pickle')
    # save_model(b, 'bias.pickle')

    #get layers from model
    # layers = our_model.save()
    #
    # #save to pickle file
    # save_model(layers, 'model.pickle')
    #
    loss = our_model.get_losses()
    visualize(loss, 100, 0.1)


    # save model
    # doda= our_model.save()
    # load model
    # layers = load_model('model.pickle')
    # our_model.load(layers)
    # our_model.predict(x)

    print(x.shape)

    predict_matrix = our_model.predict(x)

    print('prediction size', len(predict_matrix))
    print('________________________________')

    out = change_to_vector(predict_matrix[0])
    outlabel = change_to_vector(y)

    print('________________________________')

    print('predictions: ')
    print(y_old)
    print(out)
    print(len(out))

    print('accuracy: ' + str(accuracy(y_old,out,10)))
    print('precision: ' + str(precision(y_old, out,10)))
    print('recall: ' + str(recall(y_old, out, 10)))
    print('F1 score: ' + str(F1_score(y_old, out,10)))