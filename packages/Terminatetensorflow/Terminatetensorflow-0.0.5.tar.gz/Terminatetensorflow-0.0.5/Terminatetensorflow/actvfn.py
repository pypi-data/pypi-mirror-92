import numpy as np
import math

def sigmoid(x):
   # np.clip(x,np.finfo('int64').max,-np.finfo('int64').max)
    s = 1/(1+np.exp(-x)) #np.exp
    return s


def tanh(x):
   # t = (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))
    t = 1.7159 * np.tanh(x)
    return t

def linear(x):
    return x


def relu(x):
    return np.maximum(0.0, x)


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def derivative_sigmoid(x):
    return (sigmoid(x) * (1- sigmoid(x)))


def derivative_tanh(x):
    f = 1-(tanh(x)*tanh(x))
    return f


def d_linear(func):
    return np.ones(func.shape)


def d_relu(x):
    return np.greater(x, 0).astype(int)  



def d_softmax(X):
    x = softmax(X)
    s = x.reshape(-1 , 1)
    return (np.diagflat(s) - np.dot(s, np.transpose(s)))


