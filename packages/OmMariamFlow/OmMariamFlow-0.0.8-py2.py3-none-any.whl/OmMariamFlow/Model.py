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
            self.layers_weights.append(l.weights)
            self.layers_bias.append(l.bias)
        self.layers_no = len(self.layers_list)

    def Evaluate(self, Test_Inputs, Test_Labels, print_value=False):
        Input = Test_Inputs
        last_output = 0
        for l in self.layers_list:
            old_inputs = l.inputs
            l.inputs = Input     # ba7sb el forward bta3 el test
            l()
            Input = l.out
            last_output = l.out
            l.inputs = old_inputs
            l()              # hena barag3 kol 7aga l sa7bha
        old_label = self.MyLoss.Y
        old_out = self.MyLoss.Y_hat
        self.MyLoss.Loss_type.Y = Test_Labels
        self.MyLoss.Loss_type.Y_hat = last_output
        self.MyLoss.Loss_type()                     # ba7sb el forward bta3 el test
        Loss = self.MyLoss.Loss_type.out
        self.MyLoss.Loss_type.Y_hat = old_out
        self.MyLoss.Loss_type.Y = old_label
        self.MyLoss.Loss_type()                   # hena barag3 kol 7aga l sa7bha
        if print_value:
            print(f'Y_Hat : {last_output}\n Loss : {Loss}')
        return last_output, Loss  # and return y_hat , loss


    def inference(self, Test_Inputs):

    	X = Test_Inputs
    	for layer in self.layers_list:
    		if (isinstance(layer,Linear)):
    			X = X.T
    		layer.cache['X'] = X
    		X = layer.forward_pass()
    	return X

    def AddLayer(self, L1):
        self.layers_list.append(L1)

    def Loss(self, Y, Y_hat):
        self.MyLoss = Loss(Y, Y_hat, self.layers_cache[-1], self.layers_weights[-1], self.layers_bias[-1])
        return self.MyLoss

    def Activation(self, Z):  # Z = W . X + b
        MyActivation = Activation(Z)
        return MyActivation

    def Optimization(self, learning_rate, epsilon, number_of_iterations, batch_type, Loss):
        MyOptimization = Optimization(self.layers_list, learning_rate, epsilon, number_of_iterations, batch_type, Loss)
        return MyOptimization
