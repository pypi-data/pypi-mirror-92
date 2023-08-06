from function import *

class Layer(Function):
    """
    Abstract model of a neural network layer. In addition to Function, a Layer
    also has weights and gradients with respect to the weights.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.weight = {} 
        self.weight_update = {} 
        self.optimizer = None
        self.isBatchNorm = False
        self.isLinear = False
        # print("In Layer init is called")
        # print(f"optimizer_obj {self.optimizer}")

    def set_optimizer(self,optimizer_obj,isBatchNorm=False,isLinear=False):
        self.optimizer = optimizer_obj
        self.isBatchNorm = isBatchNorm
        self.isLinear = isLinear
        # print("In Layer set_optimizer is called")
        # print(f"optimizer_obj {self.optimizer} at layer {self}")

    def _init_weights(self, *args, **kwargs):
        pass

    def _update_weights(self,epoch_no):

        """
        Updates the weights using the corresponding _global_ gradients computed during
        backpropagation.
        """
        # print(f"In Layer _update_weights is called optimizer = {self.optimizer}")
        self.weight = self.optimizer.__call__(self.weight,self.weight_update,epoch_no,self.isBatchNorm,self.isLinear)
        # print("new weights : ",self.weight)
        # print("in layer : self.weight.shape ",self.weight.shape)