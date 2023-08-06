import numpy as np

class Layer():
  def __init__(self,size,activation,lr=0.001,optimizer_name='GD',beta=1,raw=1,epsilon=1 ):
    self.W = np.random.randn(size[1], size[0]) * np.sqrt(1. / size[1])
    self.b = np.zeros(size[1])
    self.activation = activation
    self.lr = lr
    self.optimizer_name=optimizer_name
    self.beta = beta
    self.raw= raw
    self.epsilon = epsilon

  def forward(self,x):
    self.x = x
    self.Z = np.dot(self.W, self.x) + self.b
    self.A = self.activation(self.Z)
    return self.A

  def backward(self,error):
    pass