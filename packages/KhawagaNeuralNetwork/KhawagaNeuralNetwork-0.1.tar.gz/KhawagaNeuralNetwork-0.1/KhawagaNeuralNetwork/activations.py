import numpy as np


def sigmoid(x, derivative=False):
        if derivative:
            return (np.exp(-x))/((np.exp(-x)+1)**2)
        return 1/(1 + np.exp(-x))

def softmax( x, derivative=False):
    # Numerically stable with large exponentials
    exps = np.exp(x - x.max())
    if derivative:
        return exps / np.sum(exps, axis=0) * (1 - exps / np.sum(exps, axis=0))
    return exps / np.sum(exps, axis=0)

def relu(x, derivative=False):
    if derivative:
        x[x<=0] = 0
        x[x>0] = 1
        return x
    
    else:
        shapex=x.shape
        k=np.zeros(shapex,dtype=float)
        return np.maximum(k,x)