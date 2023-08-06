import numpy as np
from math import sqrt
from itertools import product

from layer import *
class Linear(Layer): 

  def __init__(self, in_dim, out_dim,optimizer_obj):
    super().__init__() 
    self._init_weights(in_dim, out_dim)
    self.optimizer = optimizer_obj
    # print(f"In Linear  : {self.optimizer}")
    super().set_optimizer(self.optimizer,isBatchNorm=False,isLinear=True)


  def _init_weights(self, in_dim, out_dim):

    # Gaussian distribution  initialization of weights

    scale = 1 / sqrt(in_dim)
    self.weight['W'] = scale * np.random.randn(in_dim, out_dim) 
    self.weight['b'] = scale * np.random.randn(1, out_dim)	
    # print("___________________________________")
    # print(f"initialized_weight = {self.weight}")
    # print("___________________________________")

  def forward(self, X):
      """
      Forward pass for the Linear layer.

      Args:
          X: numpy.ndarray of shape (n_batch, in_dim) containing
              the input value.

      Returns:
          Y: numpy.ndarray of shape of shape (n_batch, out_dim) containing
              the output value.
      """
      output = np.dot(X, self.weight['W']) + self.weight['b']
      # print("X = ",X)
      # print("self.weight = ",self.weight)
      # print("self.weight_update = ",self.weight_update)
      # print("in linear : output",output)

      # caching variables for backprop (input : feature vector , output : score)
      self.cache['X'] = X 
      self.cache['output'] = output 
      return output

  def backward(self, dY):
      """
      Backward pass for the Linear layer.

      Args:
          dY: numpy.ndarray of shape (n_batch, n_out). Global gradient 
              backpropagated from the next layer.

      Returns:
          dX: numpy.ndarray of shape (n_batch, n_out). Global gradient
              of the Linear layer.
      """
      # print("dy grad loss",dY)
      # print("self.grad['X'] : ",self.grad['X'])
      dX = dY.dot(self.grad['X'].T) 

      # calculating the global gradient wrt to weights
      X = self.cache['X'] #input sample
      dW = self.grad['W'].T.dot(dY) 
      # print("Linear dY = ",dY)
      # print("Linear dY.shape :",dY.shape)
      db = np.sum(dY, axis=0, keepdims=True) 
      # print("Linear db.shape :",db.shape)
      
      # caching the global gradients
      self.weight_update = {'W': dW, 'b': db}
      # print("------------------------------------------------------------------")
      # # print("Linear self.weight_update :",self.weight_update)
      # print("Linear : max(self.weight_update['W']) = ",np.matrix(self.weight_update['W']).max())
      # print("------------------------------------------------------------------")
      return dX

  def local_grad(self, X):
      """
      Local gradients of the Linear layer at X.

      Args:
          X: numpy.ndarray of shape (n_batch, in_dim) containing the
              input data.

      Returns:
          grads: dictionary of local gradients with the following items:
              X: numpy.ndarray of shape (n_batch, in_dim).
              W: numpy.ndarray of shape (n_batch, in_dim).
              b: numpy.ndarray of shape (n_batch, 1).
      """
      gradX_local = self.weight['W']
      gradW_local = X
      gradb_local = np.ones_like(self.weight['b'])
      grads = {'X': gradX_local, 'W': gradW_local, 'b': gradb_local}
      return grads