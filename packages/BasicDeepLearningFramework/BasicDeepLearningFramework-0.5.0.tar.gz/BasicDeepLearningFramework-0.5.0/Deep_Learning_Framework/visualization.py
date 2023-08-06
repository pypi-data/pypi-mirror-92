import matplotlib.pyplot as plt
import numpy as np

def visualize (loss, epochs, learning_rate):
    """
    draw graph between number of epochs on x-axis and losses on y-axis
    """

    plt.plot(np.squeeze(loss))
    plt.ylabel('cost')
    plt.xlabel('iterations (per tens)')
    plt.title("Learning rate =" + str(learning_rate))
    plt.show()





