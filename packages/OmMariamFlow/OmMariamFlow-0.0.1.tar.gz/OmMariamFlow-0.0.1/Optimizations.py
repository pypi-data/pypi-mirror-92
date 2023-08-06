from Function import Function

import numpy as np


class Optimization(Function):
    def __init__(self, layers, learning_rate, epsilon, number_of_iterations, batch_type, Loss, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.loss = Loss
        self.loss_gradient = Loss.grad['dL']
        self.layers = layers
        self.weights = []
        self.bias = []
        self.weights_gradients = []
        self.bias_gradients = []
        self.N = self.layers[0].inputs.shape[1]
        self.number_of_iterations = number_of_iterations
        self.totalgradients = []

        for i in self.layers:
            if (i.has_weights == True):

                self.weights.append(i.weights)
                self.bias.append(i.bias)
                self.weights_gradients.append(i.weights_gradients)
                self.bias_gradients.append(i.bias_gradients)

        if batch_type == 'Batch':
            self.batch_size = self.N
        if batch_type == 'Online':
            self.batch_size = 1
        if batch_type == 'minibatch':
            self.batch_size = self.N / (np.power(2, int(np.log2(self.N))))

    def calculate_backprop(self, layer):
        if self.flag0 == True:
            self.flag0 = False
            self.layers[-1].last_layer = True
            dL = self.loss.backward_pass()
            self.dD = dL
        self.totalgradients.append(self.dD)
        self.dD = layer.backward_pass(self.dD)
        self.totalgradients.append(self.dD)

    def GradientDescent(self):
        # get weights , bias (done)
        # get weights gradients and bias gradients , delta is same shape as weights
        # this update is done for each layer
        it = 0
        while True:
            self.flag0 = True
            for layer in reversed(self.layers):
                print('backprop start')
                self.calculate_backprop(layer)  # 3shan e7sb el grad bta3 el weights w el bias
                print('backprop end')
                if (layer.has_weights == True):
                    delta_weights = np.zeros_like(layer.weights_gradients['W'])
                    delta_bias = np.zeros_like(layer.bias_gradients['b'])

                    delta_weights = layer.weights_gradients['W']
                    delta_bias = layer.bias_gradients['b']
                    weights = layer.weights - self.learning_rate * delta_weights
                    bias = layer.bias - self.learning_rate * delta_bias
                    #print(f'iterations : \n {it} \n weights : \n{weights} \n bias : \n {bias}')
                    layer.update_weights(weights, bias)
                    self.loss.Y_hat = layer.out
                    print('yhat type : {} , layer type : {}'.format(type(self.loss.Y_hat), type(layer)))
                    self.loss()
            if ((it > self.number_of_iterations) or (
                    (np.linalg.norm(delta_weights) + np.linalg.norm(delta_bias)) < self.epsilon)): break
            it += 1

    def SteepestGradientDescent(self):
        delta = np.zeros((3, 2))

        while np.linalg.norm(delta) > self.epsilon:
            for j in range(0, self.N):
                delta = np.zeros((3, 2))
            for i in range(self.batch_size * j, self.batch_size):
                delta = delta + self.loss_gradient
            delta = delta / self.batch_size
            # self.learning_rate =0
            weights = weights - self.learning_rate * delta

    def NewtonRaphson(self):
        delta = np.zeros((3, 2))

        while np.linalg.norm(delta) > self.epsilon:
            for j in range(0, self.N):
                delta = np.zeros((3, 2))
            for i in range(self.batch_size * j, self.batch_size):
                delta = delta + self.loss_gradient
            delta = delta / self.batch_size
            # self.learning_rate =np.linalg.inv()
            weights = weights - self.learning_rate * delta
