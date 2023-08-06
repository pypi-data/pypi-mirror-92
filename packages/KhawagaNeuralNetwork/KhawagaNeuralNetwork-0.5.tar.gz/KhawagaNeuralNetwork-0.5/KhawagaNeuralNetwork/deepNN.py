from KhawagaNeuralNetwork.softmax_layer import SoftmaxLayer
from KhawagaNeuralNetwork.evaluation_module import Evaluation_Module
import time
import numpy as np
from KhawagaNeuralNetwork.FC import FC
from KhawagaNeuralNetwork.optimizer import optimizer
from KhawagaNeuralNetwork.activations import relu, sigmoid, softmax
import logging

class DeepNeuralNetwork():
    def __init__(self, epochs=10, l_rate=0.001,optimizer_name='GD',beta=1,raw=1,epsilon=1):
        self.epochs = epochs
        self.l_rate = l_rate
        self.layers = []
        self.optimizer_name = optimizer_name
        self.beta = beta
        self.raw= raw
        self.epsilon = epsilon
       



    def add(self, size,activation):

          self.layers.append(FC(size,activation,lr=self.l_rate,beta=self.beta,raw=self.raw,epsilon=self.epsilon))

    def addout(self, size,activation):

          self.layers.append(SoftmaxLayer(size,activation,lr=self.l_rate,beta=self.beta,raw=self.raw,epsilon=self.epsilon))
        
    def forward_pass(self, x_train):

        # input layer activations becomes sample
        A = x_train


        L = len(self.layers)            # number of layers in the neural network
        
        # Implement [LINEAR -> RELU]*(L-1). Add "cache" to the "caches" list.
        for l in range(L):
            A = self.layers[l].forward(A)

                
        return A


    def backward_pass(self, y_train):
        '''
            This is the backpropagation algorithm, for calculating the updates
            of the neural network's parameters.

            Note: There is a stability issue that causes warnings. This is 
                  caused  by the dot and multiply operations on the huge arrays.
                  
                  RuntimeWarning: invalid value encountered in true_divide
                  RuntimeWarning: overflow encountered in exp
                  RuntimeWarning: overflow encountered in square
        '''
        L = len(self.layers) 
        error = y_train
        for l in range(L-1,-1,-1):
        # Calculate  update
          error = self.layers[l].backward(error)
        

        
    def loss(self,A, Y,m):
      cost = -(1.0/m) * np.sum(Y*np.log(A) + (1-Y)*np.log(1-A))
      cost = np.squeeze(cost)
      return cost


    def compute_accuracy(self, x_val, y_val):
        '''
            This function does a forward pass of x, then checks if the indices
            of the maximum value in the output equals the indices in the label
            y. Then it sums over each prediction and calculates the accuracy.
        '''
        predictions = []
        out = np.zeros(y_val.shape)
        labels = []
        i=0
        for x, y in zip(x_val, y_val):
            output = self.forward_pass(x)
            pred = np.argmax(output)
            labels.append(pred)
            out[i][pred] = 1
            i += 1
            predictions.append(pred == np.argmax(y))

        return np.mean(predictions),out, labels

    def train(self, x_train, y_train, x_val, y_val):
        start_time = time.time()
        for iteration in range(self.epochs):
            outputs = []
            for x,y in zip(x_train, y_train):
                output = self.forward_pass(x)
                outputs.append(output)
                self.backward_pass(y)
            
            outputs = np.array(outputs)
            losses = self.loss(outputs,y_train,x_train.shape[0])
            accuracy, predict, labels = self.compute_accuracy(x_val, y_val)
            logging.info('Epoch: {0}, Time Spent: {1:.2f}s, Accuracy: {2:.2f}%, Loss: {3:.4f}'.format(
                iteration+1, time.time() - start_time, accuracy * 100, losses
            ))
        return predict

