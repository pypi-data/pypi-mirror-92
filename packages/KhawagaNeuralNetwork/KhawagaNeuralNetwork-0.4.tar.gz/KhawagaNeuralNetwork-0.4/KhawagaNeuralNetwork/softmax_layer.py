import numpy as np
from KhawagaNeuralNetwork.layer import Layer
from KhawagaNeuralNetwork.optimizer import optimizer

class SoftmaxLayer(Layer):
  def __init__(self,size,activation,lr=0.001,optimizer_name='GD',beta=1,raw=1,epsilon=1):
    super(). __init__(size,activation,lr=0.001,optimizer_name='GD',beta=1,raw=1,epsilon=1)

  def backward(self,y):
          error = 2 * (self.A - y) / self.A.shape[0] * self.activation(self.Z, derivative=True)
          change_w = np.outer(error, self.x)
          change_b = np.sum(error,keepdims=True)
                    
          w=optimizer(self.W,self.lr,change_w)
          b=optimizer(self.b,self.lr,change_b)

         
          if self.optimizer_name== "momentum_based":
            self.W=w.momentum_based(self.beta)
            self.b=b.momentum_based(self.beta)
          elif self.optimizer_name=="adagrad":
            self.W=w.adagrad()
            self.b=b.adagrad()
          elif self.optimizer_name=="RMSProp":
            self.W=w.RMSProp(self.raw)
            self.b=b.RMSProp(self.raw)
          elif self.optimizer_name=="adaDelta":
            self.W=w.adaDelta(self.raw,self.epsilon)
            self.b=b.adaDelta(self.raw,self.epsilon)
          else: 
            self.W=w.GD()
            self.b=b.GD()


          return np.dot(self.W.T, error)
