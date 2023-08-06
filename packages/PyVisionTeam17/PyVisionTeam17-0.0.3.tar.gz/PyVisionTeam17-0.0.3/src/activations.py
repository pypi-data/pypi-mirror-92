import numpy as np
from functional import *
from function import *

class Sigmoid(Function): 
    def forward(self, X):
        return sigmoid(X)

    def backward(self, dY):
        return dY * self.grad['X']

    def local_grad(self, X):
        grads = {'X': sigmoid_prime(X)} 
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
    def __init__(self,alpha):
        super().__init__()
        self.alpha =alpha		
		
    def forward(self, X):
        return leaky_relu(X,self.alpha)

    def backward(self, dY):
        return dY * self.grad['X']

    def local_grad(self, X):
        grads = {'X': leaky_relu_prime(X,self.alpha)}
        return grads

class Softmax(Function):

    def forward(self, X):
        return softmax(X)

    def backward(self, dY):
        return dY 

    def local_grad(self,X):
        pass 