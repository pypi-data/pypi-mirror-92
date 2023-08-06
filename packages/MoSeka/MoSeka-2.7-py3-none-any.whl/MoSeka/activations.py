import numpy as np
from functional import *
from layers import Function


class Sigmoid(Function):
    
    def forward(self, X):
        return sigmoid(X)

    def backward(self, dY):
        return dY * self.grad['X']

    def local_grad(self, X):
        grads = {'X': sigmoid_prime(X)}
        return grads


class tanh(Function):
    def forward(self, X):
        return tanh(X)

    def backward(self, dY):
        return dY * self.grad['X']

    def local_grad(self, X):
        grads = {'X': tanh_prime(X)}
        return grads

class ReLU(Function):
    def forward(self, X):
        return relu(X)

    def backward(self, dY):
        return dY * self.grad['X']

    def local_grad(self, X):
        grads = {'X': relu_prime(X)}
        return grads


class LeakyReLU(Function):
    def forward(self, X):
        return leaky_relu(X)

    def backward(self, dY):
        return dY * self.grad['X']

    def local_grad(self, X):
        grads = {'X': leaky_relu_prime(X)}
        return grads


class Softmax(Function):
    def forward(self, X):
        exp_x = np.exp(X)
        probs = exp_x / np.sum(exp_x, axis=1, keepdims=True)
        return softmax()

    def backward(self, dY):
        return dY * self.grad['X']

    def local_grad(self, X):
        pass
