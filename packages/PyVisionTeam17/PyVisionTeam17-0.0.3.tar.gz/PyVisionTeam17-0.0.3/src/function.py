class Function: 
    """
    Abstract model of a differentiable function.
    """
    def __init__(self, *args, **kwargs): 

        # initializing cache for intermediate results , intermediate results are used with backprop
        self.cache = {}
        # cache for gradients/adjoints
        self.grad = {} 

    def __call__(self, *args, **kwargs): 

        # calculating output
        output = self.forward(*args, **kwargs)
        # print("out in function = ",output.shape)

        # calculating and caching local gradients
        self.grad = self.local_grad(*args, **kwargs)

        return output

    def forward(self, *args, **kwargs):
        """
        Forward pass of the function. Calculates the output value (label) and the
        gradient at the input as well.
        """
        pass

    def backward(self, *args, **kwargs):
        """
        Backward pass. Computes the local gradient at the input value
        after forward pass.
        """
        pass

    def local_grad(self, *args, **kwargs):
        """
        Calculates the local gradients of the function at the given input.

        Returns:
            grad: dictionary of local gradients.
        """
        pass