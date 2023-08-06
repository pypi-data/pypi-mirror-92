from Function import Function
from Layers import *
import numpy as np
from Visualizer import *

class Optimization(Function):
    def __init__(self, layers, epochs, batch_type, Loss, learning_rate=0.1, epsilon=0.01, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.learning_rate = []
        if type(learning_rate) == float or type(learning_rate) == int:
            self.learning_rate.append(learning_rate)
            self.learning_rate.append(False)
        else:
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
        self.epochs = epochs
        self.totalgradients = []

        for i in self.layers:
            self.weights.append(i.weights)
            self.bias.append(i.bias)
            self.weights_gradients.append(i.weights_gradients)
            self.bias_gradients.append(i.bias_gradients)

        if batch_type == 'Batch':
            self.batch_size = self.N
        elif batch_type == 'Online':
            self.batch_size = 1
        elif batch_type == 'minibatch':
            self.batch_size = self.N / (np.power(2, int(np.log2(self.N))))
        else:
            self.batch_size = batch_type

        self.number_of_iterations = self.N / self.batch_size

    def calculate_backprop(self, layer):
        if self.flag0 == True:
            self.flag0 = False
            self.layers[-1].last_layer = True
            dL = self.loss.backward_pass()
            self.loss()
            self.dD = dL
        #if layer.last_layer:
            #self.loss()
        self.totalgradients.append(self.dD)
        self.dD = layer.backward_pass(self.dD)
        self.totalgradients.append(self.dD)

    def GradientDescent(self):
        # get weights , bias (done)
        # get weights gradients and bias gradients , delta is same shape as weights
        # this update is done for each layers
        visualizer = Visualizer()
        visualizer.add_plot(name = 'loss' , colour = 'red')
        iteration = 0
        while True:
            self.flag0 = True
            for layer in reversed(self.layers):
                self.calculate_backprop(layer)  # 3shan e7sb el grad bta3 el weights w el bias
                #delta_weights = np.zeros_like(layer.weights_gradients['W'])
                #delta_bias = np.zeros_like(layer.bias_gradients['b'])

                delta_weights = layer.weights_gradients['W']
                delta_bias = layer.bias_gradients['b']
                #handle NAN
                delta_weights[np.isnan(delta_weights)] = 0.1
                delta_bias[np.isnan(delta_bias)] = 0.1
                #print(delta_weights)
                if self.learning_rate[1] is True:
                    decay_rate = self.learning_rate[0] / self.batch_size
                    self.learning_rate[0] = self.learning_rate[0] / (1 + decay_rate * iteration)
                #print("alpha : ", self.learning_rate[0])

                weights = layer.weights - self.learning_rate[0] * delta_weights
                bias = layer.bias - self.learning_rate[0] * delta_bias
                #if not(isinstance(layer,Flatten) or isinstance(layer,MaxPool)):
                    #print(f'iterations : \n {iteration} \n weights : \n{weights} \n bias : \n {bias}')
                layer.update_weights(weights, bias)
                if layer.last_layer:
                    self.loss.Y_hat = layer.out
                # self.loss()
                #print(f'\n Loss : {self.loss.out}')
            visualizer.update([self.loss.out])

            if (iteration > self.epochs): 
                break
            iteration += 1



    def Momentum(self, beta=0.5):
        iteration = 0
        V_weights = []
        V_bias = []

        for I in range(len(self.layers)):
            V_weights.append(np.zeros_like(self.layers[I].weights))
            V_bias.append(np.zeros_like(self.layers[I].bias))

        while True:
            self.flag0 = True
            for index in reversed(range(len(self.layers))):

                self.calculate_backprop(self.layers[index])  # 3shan e7sb el grad bta3 el weights w el bias
                delta_weights = np.zeros_like(self.layers[index].weights_gradients['W'])

                delta_bias = np.zeros_like(self.layers[index].bias_gradients['b'])

                delta_weights = self.layers[index].weights_gradients['W']
                delta_bias = self.layers[index].bias_gradients['b']

                if self.learning_rate[1] is True:
                    decay_rate = self.learning_rate[0] / self.batch_size
                    self.learning_rate[0] = self.learning_rate[0] / (1 + decay_rate * iteration)

                V_weights[index] = np.multiply(beta, V_weights[index]) - self.learning_rate[0] * delta_weights
                V_bias[index] = np.multiply(beta, V_bias[index]) - self.learning_rate[0] * delta_bias

                weights = self.layers[index].weights + V_weights[index]
                bias = self.layers[index].bias + V_bias[index]

                print(f'iterations : \n {iteration} \n weights : \n{weights} \n bias : \n {bias}')
                self.layers[index].update_weights(weights, bias)
                self.loss.Y_hat = self.layers[index].out
                #self.loss()
                print(f'\n Loss : {float(self.loss.out)}')
            if ((iteration > self.epochs) or (
                    (np.linalg.norm(delta_weights) + np.linalg.norm(delta_bias)) < self.epsilon)): break
            iteration += 1

    def AdaGrad(self):
        iteration = 0
        A_weights = []
        A_bias = []

        for I in range(len(self.layers)):
            A_weights.append(np.zeros_like(self.layers[I].weights))
            A_bias.append(np.zeros_like(self.layers[I].bias))

        while True:
            self.flag0 = True
            for index in reversed(range(len(self.layers))):

                self.calculate_backprop(self.layers[index])  # 3shan e7sb el grad bta3 el weights w el bias
                delta_weights = np.zeros_like(self.layers[index].weights_gradients['W'])

                delta_bias = np.zeros_like(self.layers[index].bias_gradients['b'])

                delta_weights = self.layers[index].weights_gradients['W']
                delta_bias = self.layers[index].bias_gradients['b']

                if self.learning_rate[1] is True:
                    decay_rate = self.learning_rate[0] / self.batch_size
                    self.learning_rate[0] = self.learning_rate[0] / (1 + decay_rate * iteration)

                A_weights[index] = A_weights[index] + np.square(delta_weights)
                A_bias[index] = A_bias[index] + np.square(delta_bias)

                shape_w = np.shape(self.layers[index].weights)
                shape_b = np.shape(self.layers[index].bias)

                weights = self.layers[index].weights - np.multiply(
                    (np.divide(self.learning_rate[0], np.sqrt(A_weights))), delta_weights)
                weights = np.reshape(weights, shape_w)
                bias = self.layers[index].bias - np.multiply((np.divide(self.learning_rate[0], np.sqrt(A_bias))),
                                                             delta_bias)
                bias = np.reshape(bias, shape_b)
                print(f'iterations : \n {iteration} \n weights : \n{weights} \n bias : \n {bias}')

                self.layers[index].update_weights(weights, bias)
                self.loss.Y_hat = self.layers[index].out
                #self.loss()
                print(f'\n Loss : {float(self.loss.out)}')

            if ((iteration > self.epochs) or (
                    (np.linalg.norm(delta_weights) + np.linalg.norm(delta_bias)) < self.epsilon)): break
            iteration += 1

    def RMSprop(self, ro=0.5):
        iteration = 0
        A_weights = []
        A_bias = []

        for I in range(len(self.layers)):
            A_weights.append(np.zeros_like(self.layers[I].weights))
            A_bias.append(np.zeros_like(self.layers[I].bias))

        while True:
            self.flag0 = True
            for index in reversed(range(len(self.layers))):

                self.calculate_backprop(self.layers[index])  # 3shan e7sb el grad bta3 el weights w el bias
                delta_weights = np.zeros_like(self.layers[index].weights_gradients['W'])

                delta_bias = np.zeros_like(self.layers[index].bias_gradients['b'])

                delta_weights = self.layers[index].weights_gradients['W']
                delta_bias = self.layers[index].bias_gradients['b']

                if self.learning_rate[1] is True:
                    decay_rate = self.learning_rate[0] / self.batch_size
                    self.learning_rate[0] = self.learning_rate[0] / (1 + decay_rate * iteration)

                A_weights[index] = ro * A_weights[index] + (1 - ro) * np.square(delta_weights)
                A_bias[index] = A_bias[index] + np.square(delta_bias)

                shape_w = np.shape(self.layers[index].weights)
                shape_b = np.shape(self.layers[index].bias)

                weights = self.layers[index].weights - np.multiply(
                    (np.divide(self.learning_rate[0], np.sqrt(A_weights))), delta_weights)
                weights = np.reshape(weights, shape_w)
                bias = self.layers[index].bias - np.multiply((np.divide(self.learning_rate[0], np.sqrt(A_bias))),
                                                             delta_bias)
                bias = np.reshape(bias, shape_b)
                print(f'iterations : \n {iteration} \n weights : \n{weights} \n bias : \n {bias}')


                self.layers[index].update_weights(weights, bias)
                self.loss.Y_hat = self.layers[index].out
                #self.loss()
                print(f'\n Loss : {float(self.loss.out)}')
            if ((iteration > self.epochs) or (
                    (np.linalg.norm(delta_weights) + np.linalg.norm(delta_bias)) < self.epsilon)): break
            iteration += 1

    def AdaDelta(self, ro=0.5):

        iteration = 0
        A_weights = []
        A_bias = []

        d_weights = []
        d_bias = []

        for I in range(len(self.layers)):
            A_weights.append(np.zeros_like(self.layers[I].weights))
            A_bias.append(np.zeros_like(self.layers[I].bias))

            d_weights.append(np.random.random(np.shape(self.layers[I].weights)))
            d_bias.append(np.random.random(np.shape(self.layers[I].bias)))

        while True:
            self.flag0 = True
            for index in reversed(range(len(self.layers))):
                self.calculate_backprop(self.layers[index])  # 3shan e7sb el grad bta3 el weights w el bias
                delta_weights = np.zeros_like(self.layers[index].weights_gradients['W'])

                delta_bias = np.zeros_like(self.layers[index].bias_gradients['b'])

                delta_weights = self.layers[index].weights_gradients['W']
                delta_bias = self.layers[index].bias_gradients['b']

                A_weights[index] = A_weights[index] + np.square(delta_weights)
                A_bias[index] = A_bias[index] + np.square(delta_bias)

                triangle_w = np.multiply((np.sqrt(np.divide(d_weights, np.add(A_weights, self.epsilon)))),
                                         delta_weights)
                triangle_b = np.multiply((np.sqrt(np.divide(d_bias, np.add(A_bias, self.epsilon)))), delta_bias)

                d_weights = np.multiply(ro, d_weights) + np.multiply(1 - ro, np.square(triangle_w))
                d_bias = np.multiply(ro, d_bias) + np.multiply(1 - ro, np.square(triangle_b))

                shape_w = np.shape(self.layers[index].weights)
                shape_b = np.shape(self.layers[index].bias)

                weights = self.layers[index].weights - np.multiply(
                    np.sqrt(np.divide(d_weights, np.add(A_weights, self.epsilon))), delta_weights)
                weights = np.reshape(weights, shape_w)
                bias = self.layers[index].bias - np.multiply(np.sqrt(np.divide(d_bias, np.add(A_bias, self.epsilon))),
                                                             delta_bias)
                bias = np.reshape(bias, shape_b)
                print(f'iterations : \n {iteration} \n weights : \n{weights} \n bias : \n {bias}')


                self.layers[index].update_weights(weights, bias)
                self.loss.Y_hat = self.layers[index].out
                #self.loss()
                print(f'\n Loss : {float(self.loss.out)}')
            if ((iteration > self.epochs) or (
                    (np.linalg.norm(delta_weights) + np.linalg.norm(delta_bias)) < self.epsilon)): break
            iteration += 1
    def Adam(self,ro=0.5,ro_f=0.5):
        iteration = 0
        alpha= self.learning_rate
        A_weights = []
        A_bias = []

        F_weights = []
        F_bias = []

        for I in range(len(self.layers)):
            A_weights.append(np.zeros_like(self.layers[I].weights))
            A_bias.append(np.zeros_like(self.layers[I].bias))

            F_weights.append(np.zeros_like(self.layers[I].weights))
            F_bias.append(np.zeros_like(self.layers[I].bias))
        while True:
            self.flag0 = True
            for index in reversed(range(len(self.layers))):

                self.calculate_backprop(self.layers[index])  # 3shan e7sb el grad bta3 el weights w el bias
                delta_weights = np.zeros_like(self.layers[index].weights_gradients['W'])

                delta_bias = np.zeros_like(self.layers[index].bias_gradients['b'])

                delta_weights = self.layers[index].weights_gradients['W']
                delta_bias = self.layers[index].bias_gradients['b']


                A_weights[index] = np.multiply(ro,A_weights[index]) + np.multiply(1-ro,np.square(delta_weights))
                A_bias[index] = np.multiply(ro,A_bias[index]) + np.multiply(1-ro,np.square(delta_bias))

                F_weights[index] = np.multiply(ro, F_weights[index]) + np.multiply(1 - ro, np.square(delta_weights))
                F_bias[index] = np.multiply(ro_f, F_bias[index]) + np.multiply(1 - ro_f, np.square(delta_bias))

                alpha = np.multiply(alpha , np.sqrt((1-ro)/(1-ro_f)))

                shape_w = np.shape(self.layers[index].weights)
                shape_b = np.shape(self.layers[index].bias)

                weights = self.layers[index].weights - np.multiply(np.sqrt(np.divide(alpha,np.add(A_weights,self.epsilon))),F_weights)
                weights = np.reshape(weights, shape_w)

                bias = self.layers[index].bias - np.multiply(np.sqrt(np.divide(alpha,np.add(A_bias,self.epsilon))),F_bias)
                bias = np.reshape(bias, shape_b)
                print(f'iterations : \n {iteration} \n weights : \n{weights} \n bias : \n {bias}')


                self.layers[index].update_weights(weights, bias)
                self.loss.Y_hat = self.layers[index].out
                #self.loss()
                print(f'\n Loss : {float(self.loss.out)}')
            if ((iteration > self.epochs) or (
                    (np.linalg.norm(delta_weights) + np.linalg.norm(delta_bias)) < self.epsilon)): break
            iteration += 1

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
