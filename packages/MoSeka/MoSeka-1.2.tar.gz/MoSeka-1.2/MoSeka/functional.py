import numpy as np


def sigmoid(x):
    return 1/(1 + np.exp(-x))

def sigmoid_prime(x):
    s = sigmoid(x)
    return s * (1 - s)

def tanh(x):
    return (np.exp(2*x)-1)/(np.exp(2*x)+1)

def tanh_prime(x):
    return 1-tanh(x)^2

def hard_tanh(x):
    return np.maximum(np.minimum(x,1),-1)
def hard_tanh_prime(x):
    return 1*(x > -1 and x <1)
def relu(x):
    return x*(x > 0)
    
def relu_prime(x):
    return 1*(x > 0)


def leaky_relu(x, alpha):
    return x*(x > 0) + alpha*x*(x <= 0)


def leaky_relu_prime(x, alpha):
    return 1*(x > 0) + alpha*(x <= 0)