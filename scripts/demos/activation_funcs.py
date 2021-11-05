#!/bin/python

import numpy as np

def binary_step(x):
    return np.where(x < 0, 0, 1)

def binary_step_(x):
    return np.where(x != 0, 0, np.inf)

def linear(x, a=1):
    return a * x

def linear_(x, a=1):
    return a

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
    
def sigmoid_(x):
    return sigmoid(x) * (1-sigmoid(x))

def tanh(x):
    return (2 / (1 + np.exp(-2*x))) -1

def tanh_(x):
    return 1 - np.power(tanh(x), 2)

def relu(x):
    """Rectified Linear Unit (ReLU) (Hahnloser et al., 2000; Jarrett et al., 2009; Nair & Hinton, 2010)"""
    return np.where(x < 0, 0, x)

def relu_(x):
    return np.where(x < 0, 0, 1)

def leaky_relu(x, a=0.01):
    """Leaky ReLU (LReLU) (Maas et al., 2013)"""
    return np.where(x < 0, a * x, x)

def leaky_relu_(x, a=0.01):
    return np.where(x < 0, a, 1)

def elu(x, a=1):
    """Exponential Linear Unit (ELU) (Clevert et al., 2015)"""
    return np.where(x < 0, a * (np.exp(x)-1), x)

def elu_(x, a=1):
    return np.where(x < 0, a * (np.exp(x)), 1)

def swish(x, beta=1):
    """SWISH: A SELF-GATED ACTIVATION FUNCTION
    https://arxiv.org/pdf/1710.05941v1.pdf"""
    return 2 * x * sigmoid(beta * x)

def swish_(x, beta=1):
    return swish(x, beta) + sigmoid(x)*(1 - swish(x, beta))

def eswish(x, beta=1):
    """Eswish
    https://arxiv.org/abs/1801.07145
    > Eswish is just a generalization of the Swish activation function (x*sigmoid(x)),
      which is multiplied by a parameter beta
    """
    return beta * x * sigmoid(x)

def eswish_(x, beta=1):
    return eswish(x, beta) + sigmoid(x) * (beta - eswish(x, beta))
