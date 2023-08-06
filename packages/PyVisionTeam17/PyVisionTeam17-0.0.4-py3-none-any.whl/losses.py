import numpy as np
from function import *

class Loss(Function):
    def forward(self, X, Y):
        """
        Computes the loss of x with respect to y.

        Args:
            X: numpy.ndarray of shape (n_batch, n_dim).
            Y: numpy.ndarray of shape (n_batch, n_dim).

        Returns:
            loss: numpy.float.
        """
        pass

    def backward(self):
        """
        Backward pass for the loss function. Since it should be the final layer
        of an architecture, no input is needed for the backward pass.

        Returns:
            gradX: numpy.ndarray of shape (n_batch, n_dim). Local gradient of the loss.
        """
        # loss doesn't need to be back-propagated because it is the first thing to be back-prpagated
        return self.grad['X'] 
		

    def local_grad(self, X, Y):
        """
        Local gradient with respect to X at (X, Y).

        Args:
            X: numpy.ndarray of shape (n_batch, n_dim).
            Y: numpy.ndarray of shape (n_batch, n_dim).

        Returns:
            gradX: numpy.ndarray of shape (n_batch, n_dim).
        """
        pass


class MeanSquareLoss(Loss):
    def forward(self, X, Y):
        """
        Computes the mean square error of X with respect to Y.

        Args:
            X: numpy.ndarray of shape (n_batch, n_dim).
            Y: numpy.ndarray of shape (n_batch, n_dim).

        Returns:
            mse_loss: numpy.float. Mean square error of x with respect to y.
        """
        # calculating loss

        Y = Y.reshape(X.shape[0],1)

        sum = np.sum((X - Y) ** 2, axis=1, keepdims=True) 
        mse_loss = np.mean(sum) 

        return mse_loss

    def local_grad(self, X, Y):
        """
        Local gradient with respect to X at (X, Y).

        Args:
            X: numpy.ndarray of shape (n_batch, n_dim).
            Y: numpy.ndarray of shape (n_batch, n_dim).

        Returns:
            gradX: numpy.ndarray of shape (n_batch, n_dim). Gradient of MSE wrt X at X and Y.
        """
        Y = Y.reshape(X.shape[0],1)
        grads = {'X': 2 * (X - Y) / X.shape[0]} 

        return grads


class Multinomial_Logistic_Regression(Loss):

    def forward(self, probs, y_labels):
        """
        Computes the cross entropy loss of x with respect to y.

        Args:
            X: numpy.ndarray of shape (n_batch, n_dim).
            y: numpy.ndarray of shape (n_batch, 1). Should contain class labels
                for each data point in x.

        Returns:
            crossentropy_loss: numpy.float. Cross entropy loss of x with respect to y.
        """
        L = 0
        for i in range(probs.shape[0]):
          L -= np.log(probs[i][ int(y_labels[i])])
        
        L /= probs.shape[0]

        return L

    def local_grad(self, probs, y_labels):

        grads = np.zeros_like(probs)
        for i in range(probs.shape[0]):
            for j in range(10):
                if j == y_labels[i]:
                  grads[i][j] = -(1-probs[i][j])
                else: 
                  grads[i][j] = probs[i][j]
        grad_np = {'X': grads}
        return grad_np 