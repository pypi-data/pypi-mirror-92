import numpy as np

class optimizer:

   def __init__(self,weights,lr,delta):
     self.lr=lr
     self.delta=delta
     self.weights=weights
     self.weights=np.array(self.weights)

   def GD (self):
      self.weights=self.weights-np.multiply(self.lr,self.delta)

      return self.weights
    
   
   def momentum_based(self,beta):
      V =np.zeros((self.weights.shape[0],self.weights.shape[1])) 
      V=V+np.multiply(beta,V)-np.multiply(self.lr,self.delta)
      self.weights= self.weights+V
      return self.weights

   
   def Nesstrove(self,beta):
      V =np.zeros((self.weights.shape[0],self.weights.shape[1]))
      

   def adagrad(self):
      A=np.zeros((self.weights.shape[0],self.weights.shape[1]))
      A=np.sum(np.power(self.delta, 2))
      self.weights=self.weights-np.multiply((self.lr/np.sqrt(A)),self.delta)
      return self.weights

   def RMSProp(self,raw):
    
      A=np.zeros((self.weights.shape[0],self.weights.shape[1]))
      A=np.sum(np.multiply(np.multiply(raw,A)+(1-raw),np.power(self.delta,2)))
      self.weights=self.weights-np.multiply((self.lr/np.sqrt(A)),self.delta)
      return self.weights

    
       
 

   def adaDelta(self,raw,epsilon):
      
    A=np.zeros((self.weights.shape[0],self.weights.shape[1]))
    sigma=np.zeros((self.weights.shape[0],self.weights.shape[1]))
    sigma=np.random.rand()
    del_w=np.zeros((self.weights.shape[0],self.weights.shape[1]))
    A=np.sum(np.power(self.delta,2))
    del_w=np.sqrt(np.multiply(sigma/(A+epsilon),self.delta))
    sigma=raw*sigma+(1-raw)*np.power(del_w,2)
    self.weights=self.weights-np.sqrt(sigma/(A+epsilon))*self.delta
    return self.weights 
    
   



   