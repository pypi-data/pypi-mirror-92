import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd

from Layers import *
from Data import *
from Model import *

train_path = 'data/mnist_train.csv'

img_data = Image(path = train_path,test_frac = 0.8,val_frac = 0.195,image_size=(28,28), colour = 'gray')
train_data = img_data.train_data

Layer2 = Conv(X = train_data,in_channels = 1, out_channels = 3, kernel_size=3, stride=1, padding= 2  , Activation_fn = 'relu')

#Layer2 = MaxPool(Layer1.output(),kernel_size = 2, stride=2, padding=0)

Layer3 = Flatten(Layer2.output())

l3out = Layer3.output()

n_out = 1
weights = np.random.random((n_out,l3out.shape[1]))

bias = np.random.random((n_out))

print(l3out.T.shape,weights.shape,bias.shape)

Layer4 = Linear(Layer3.output().T, weights, bias, 'sigmoid')

my_Model = Model([Layer2,Layer3,Layer4])


train_labels = img_data.train_labels
train_labels.shape
zeros = train_labels == 0
train_labels[zeros] = 1

my_Loss = my_Model.Loss(train_labels, Layer4.output()).LogisticRegressionSigmoid()

# Parameters
learning_rate = 1
training_epochs = 20
epsilon = 0.2
opt = my_Model.Optimization(learning_rate, epsilon, 5, 'Batch', my_Loss).GradientDescent()


