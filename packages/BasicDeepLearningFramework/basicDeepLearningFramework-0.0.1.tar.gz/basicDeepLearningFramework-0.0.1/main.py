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
    """changes one hot vector to normal class numbers, e.g : [0 0 1] -> [2]"""
    res = []
    for i in range(len(y)):
        curr = y[i]
        res.append(int(np.argmax(curr)))
    return res



if __name__ == '__main__':
    print('Hello Engineers !')


