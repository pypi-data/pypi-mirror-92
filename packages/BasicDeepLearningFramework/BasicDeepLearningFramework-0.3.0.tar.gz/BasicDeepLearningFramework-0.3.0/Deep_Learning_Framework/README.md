
# Deep Learning Framework
 - This deep learning framework can be used primarily to build deep learning models with ease. it provieds many utilities such as: visualization costs with epochs, Evaluation        metrics and more.
 
 # Our project
 in this project we implement our Neural Network , a Neural network is simply a function, mapping an input (such as an image) to a prediction.
 Fundamentally, there are two simple operations you want to do with a function: 
 calculate the output and the derivative, given an input. The first one is needed to obtain predictions, the latter one is to train your network with gradient descent. 
 In neural network terminology, calculating the output is called the forward pass, while the gradient with respect to the input is called a local gradient.
 
# our modules to build our neural network
- Data Module
   "loading dataset or split the data"
- core modules  
     1. Layers
     2. Losses
     3. Activation functions
- Visualization Module
    "Visualize the cost function versus iterations/epochs during training process"
- Evaluation Module
     "Implement accuracy estimation function and implement precision & recall metric for better evaluation"
- Utility Module:
     "This module is for saving & loading model weights & configurations into a compressed format"

# Dataset :
    1-Download the dataset of  MNIST as a .csv file from kaggle
    2-Create a specific folders for training, validation & testing.
    3-Split randomly the training .csv file into training & validation dataset.
