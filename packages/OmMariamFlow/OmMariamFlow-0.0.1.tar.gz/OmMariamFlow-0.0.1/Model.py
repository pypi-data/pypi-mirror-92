import numpy as np
from Losses import *
from Activations import Activation
from Optimizations import Optimization
from Layers import *


class Model:
    def __init__(self, layer_list=[], *args, **kwargs):
        self.layers_list = []
        self.layers_cache = []
        self.layers_weights = []
        self.layers_bias = []
        for l in layer_list:
            '''l.activation_fn'''
            l.activation_Fn = l()
            self.layers_list.append(l)
            self.layers_cache.append(l.cache)
            if (l.has_weights == True):
                self.layers_weights.append(l.weights)
                self.layers_bias.append(l.bias)
        self.layers_no = len(self.layers_list)

    def AddLayer(self, L1):
        self.layers_list.append(L1)

    def Loss(self, Y, Y_hat):
        MyLoss = Loss(Y, Y_hat, self.layers_cache[-1], self.layers_weights[-1], self.layers_bias[-1])
        return MyLoss

    def Activation(self, Z):  # Z = W . X + b
        MyActivation = Activation(Z)
        return MyActivation

    def Optimization(self, learning_rate, epsilon, number_of_iterations, batch_type, Loss):
        MyOptimization = Optimization(self.layers_list, learning_rate, epsilon, number_of_iterations, batch_type, Loss)
        return MyOptimization

# model = Model()
# opt = model.Optimization()
# train = opt.GradientDescent()
