import csv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image
from numpy import asarray
import math


class load:
  def loadData(file_path, y , indexY):
    #y is the Label
    #indexY the index of label
    datasets = pd.read_csv(file_path)
    fin_index= indexY+1
    #datasets.head() #show first 4 rows
    #datasets.describe() #Return all the statics for every row x col
  
    all_pixels = np.array(datasets.iloc[:,fin_index:])
    Labels = None
    if(y == 'label'):
      Labels = np.array(datasets[y])


    return all_pixels, Labels

  def image(image_path):
    image = Image.open(image_path)
    #print(image.format)
    #print(image.mode)
    #print(image.size)

    # if create a thumbnail and preserve aspect ratio
    #Note about resizing in which case the largest dimension, will be reduced to desired size,
    #and the height will be scaled in order to retain the aspect ratio of the image.
    #image.thumbnail((28,28))
    # report the size of the thumbnail
    #Resize_image = image.size
    #if (Resize_image[0] != Resize_image[1]):
      #print("Alert! dimentions not equal")
  
    #this method will specify the width and height in pixels and the image will be reduced or stretched to fit the new shape.
    img_resized = image.resize((28,28))
    # report the size of the thumbnail
    final_size= img_resized.size
    #return all poxels in the image
    pixels = asarray(img_resized)
    return pixels

  def normalization(pixels):
    # confirm pixel range is 0-255
    #print('Data Type: %s' % pixels.dtype)
    #print('Min: %.3f, Max: %.3f' % (pixels.min(), pixels.max()))
    # convert from integers to floats
    pixels = pixels.astype('float32')
    # normalize to the range 0-1
    pixels /= 255.0
    # confirm the normalization
    #print('Min: %.3f, Max: %.3f' % (pixels.min(), pixels.max()))
    return pixels

  def visualize(file_path, x, y):
    datasets = pd.read_csv(file_path)
    y = datasets[y].iloc[0:10].values
    x = datasets[x].iloc[0:10].values
    #print(x)
    fig = plt.figure()
    ax = plt.subplot(111)

    ax.plot(x,y,lw=4)
    #ax.set_xlabel('pixels',fontsize=14)
    #ax.set_ylabel('Its Label',fontsize=14)
    #ax.set_title('VisualizeMyData',fontsize=14)

    #plt.show()
  def split_dataset(all_pixels, Labels,testSize):
    #testSize is th size of train 
    all_pixelstrain= all_pixels.shape
    #print(all_pixelstrain)
    indexR1 = math.floor(testSize * all_pixelstrain[0])
    #print(indexR1)
    indexR2 = (all_pixelstrain[0] - indexR1)+ 1 
    #print(indexR2)
    x_train = all_pixels[ : indexR1, :]
    y_train = Labels[ :indexR1] 
    x_tests = all_pixels[indexR2 :, :]
    y_tests = Labels[indexR2 :]
  
    return x_train, y_train, x_tests , y_tests
