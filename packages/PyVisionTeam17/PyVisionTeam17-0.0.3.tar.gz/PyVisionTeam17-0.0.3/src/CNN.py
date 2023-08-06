from function import *
from layer import *

def zero_pad(X, pad_width, dims):
    """
    Pads the given array X with zeroes at the both end of given dims.

    Args:
        X: numpy.ndarray.
        pad_width: int, width of the padding.
        dims: int or tuple, dimensions to be padded.

    Returns:
        X_padded: numpy.ndarray, zero padded X.
    """
    dims = (dims) if isinstance(dims, int) else dims
    pad = [(0, 0) if idx not in dims else (pad_width, pad_width)
           for idx in range(len(X.shape))]
    X_padded = np.pad(X, pad, 'constant')
    return X_padded

class Conv(Layer):
    def __init__(self,optimizer_obj, in_channels, out_channels, kernel_size=3, stride=1, padding=0 ):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.stride = stride
        self.kernel_size = kernel_size if isinstance(kernel_size, tuple) \
                           else (kernel_size, kernel_size)
        self.padding = padding
        self._init_weights(in_channels, out_channels, self.kernel_size)
        self.optimizer = optimizer_obj
        # print(f"In Conv  : {self.optimizer}")
        super().set_optimizer(self.optimizer,isBatchNorm=False,isLinear=False)

    def _init_weights(self, in_channels, out_channels, kernel_size):
        scale = 2/sqrt(in_channels*kernel_size[0]*kernel_size[1])

        self.weight = {'W': np.random.normal(scale=scale,
                                             size=(out_channels, in_channels, *kernel_size)),
                       'b': np.zeros(shape=(out_channels, 1))}

    def forward(self, X):
        """
        Forward pass for the convolution layer.

        Args:
            X: numpy.ndarray of shape (N, C, H_in, W_in).

        Returns:
            Y: numpy.ndarray of shape (N, F, H_out, W_out).
        """
        if self.padding:
            X = zero_pad(X, pad_width=self.padding, dims=(2, 3))

        self.cache['X'] = X

        # print("input : ",X.shape)
        # print(f"self.weight['b'].shape : {self.weight['b'].shape}")
        # print(f"self.weight['W'].shape : {self.weight['W'].shape}")

        N, C, H, W = X.shape
        KH, KW = self.kernel_size
        out_shape = (N, self.out_channels, 1 + (H - KH)//self.stride, 1 + (W - KW)//self.stride)
        Y = np.zeros(out_shape)

        for n in range(N):
            for c_w in range(self.out_channels):
                for h, w in product(range(out_shape[2]), range(out_shape[3])):
                    h_offset, w_offset = h*self.stride, w*self.stride
                    rec_field = X[n, :, h_offset:h_offset + KH, w_offset:w_offset + KW] #receptive field 
                    # print(f"rec_field.shape : {rec_field.shape}")
                    Y[n, c_w, h, w] = np.sum(self.weight['W'][c_w]*rec_field) + self.weight['b'][c_w]
                    Y[n, c_w, h, w] = np.sum(self.weight['W'][c_w]*rec_field) 
                    # print(f"self.weight['b'][c_w].shape : {self.weight['b'][c_w].shape}")
                    # print(f"self.weight['W'][c_w].shape : {self.weight['W'][c_w].shape}")
                    # print(f"rec_field.shape : {rec_field.shape}")
                    # print(f"np.sum(self.weight['W'][c_w]*rec_field).shape : ",np.sum(self.weight['W'][c_w]*rec_field).shape)
        return Y

    def backward(self, dY):
        # calculating the global gradient to be propagated backwards
        # TODO: this is actually transpose convolution, move this to a util function
		
        X = self.cache['X']
        dX = np.zeros_like(X)
        N, C, H, W = dX.shape
        KH, KW = self.kernel_size
		
        for n in range(N):
            for c_w in range(self.out_channels):
                for h, w in product(range(dY.shape[2]), range(dY.shape[3])):
                    h_offset, w_offset = h * self.stride, w * self.stride
                    dX[n, :, h_offset:h_offset + KH, w_offset:w_offset + KW] += \
                        self.weight['W'][c_w] * dY[n, c_w, h, w]

        # calculating the global gradient wrt the conv filter weights
        dW = np.zeros_like(self.weight['W'])
        for c_w in range(self.out_channels):
            for c_i in range(self.in_channels):
                for h, w in product(range(KH), range(KW)):
                    X_rec_field = X[:, c_i, h:H-KH+h+1:self.stride, w:W-KW+w+1:self.stride]
                    dY_rec_field = dY[:, c_w]
                    dW[c_w, c_i, h, w] = np.sum(X_rec_field*dY_rec_field)

        # calculating the global gradient wrt to the bias
        db = np.sum(dY, axis=(0, 2, 3)).reshape(-1, 1)

        # caching the global gradients of the parameters
        self.weight_update['W'] = dW
        self.weight_update['b'] = db

        return dX[:, :, self.padding:-self.padding, self.padding:-self.padding]

class MaxPool(Function):
    def __init__(self, kernel_size=(2, 2)):
        super().__init__()
        self.kernel_size = (kernel_size, kernel_size) if isinstance(kernel_size, int) else kernel_size

    def __call__(self, X):
        # in contrary to other Function subclasses, MaxPool2D does not need to call
        # .local_grad() after forward pass because the gradient is calculated during it
        return self.forward(X)

    def forward(self, X):
	
        N, C, H, W = X.shape
        KH, KW = self.kernel_size

        grad = np.zeros_like(X)
        Y = np.zeros((N, C, H//KH, W//KW)) # floor division #downsampling 16x16 ==> 2x2 ===>output max poot 8x8 where 8 =floor(16/2)=16//2

        # for n in range(N):
        for h, w in product(range(0, H//KH), range(0, W//KW)):
            h_offset, w_offset = h*KH, w*KW
            rec_field = X[:, :, h_offset:h_offset+KH, w_offset:w_offset+KW]
            Y[:, :, h, w] = np.max(rec_field, axis=(2, 3))
            for kh, kw in product(range(KH), range(KW)):
                grad[:, :, h_offset+kh, w_offset+kw] = (X[:, :, h_offset+kh, w_offset+kw] >= Y[:, :, h, w])

        # storing the gradient
        self.grad['X'] = grad

        return Y

    def backward(self, dY):
        dY = np.repeat(np.repeat(dY, repeats=self.kernel_size[0], axis=2),
                       repeats=self.kernel_size[1], axis=3)
        return self.grad['X']*dY

    def local_grad(self, X):
        # small hack: because for MaxPool calculating the gradient is simpler during
        # the forward pass, it is calculated there and this function just returns the
        # grad dictionary
        return self.grad


class LCN(Layer):
    def __init__(self,optimizer_obj, n_channels, epsilon=1e-5):
        super().__init__()
        self.epsilon = epsilon
        self.n_channels = n_channels
        self._init_weights(n_channels)
        self.optimizer = optimizer_obj
        # print(f"In BatchNorm  : {self.optimizer}")
        super().set_optimizer(self.optimizer,isBatchNorm=True,isLinear=False)

    def _init_weights(self, n_channels):

        self.weight['gamma'] = np.ones(shape=(1, n_channels, 1, 1))
        self.weight['beta'] = np.zeros(shape=(1, n_channels, 1, 1))

    def forward(self, X):
        """
        Forward pass for the 2D batchnorm layer.

        Args:
            X: numpy.ndarray of shape (n_batch, n_channels, height, width).

        Returns_
            Y: numpy.ndarray of shape (n_batch, n_channels, height, width).
                Batch-normalized tensor of X.
        """
        mean = np.mean(X, axis=(2, 3), keepdims=True)
        var = np.var(X, axis=(2, 3), keepdims=True) + self.epsilon
        invvar = 1.0/var
        sqrt_invvar = np.sqrt(invvar)
        centered = X - mean  #zero-centered
        scaled = centered * sqrt_invvar 
        normalized = scaled * self.weight['gamma'] + self.weight['beta'] #bonus =)

        # caching intermediate results for backprop
        self.cache['mean'] = mean
        self.cache['var'] = var
        self.cache['invvar'] = invvar
        self.cache['sqrt_invvar'] = sqrt_invvar
        self.cache['centered'] = centered
        self.cache['scaled'] = scaled
        self.cache['normalized'] = normalized

        return normalized

    def backward(self, dY):
        """
        Backward pass for the 2D batchnorm layer. Calculates global gradients
        for the input and the parameters.

        Args:
            dY: numpy.ndarray of shape (n_batch, n_channels, height, width).

        Returns:
            dX: numpy.ndarray of shape (n_batch, n_channels, height, width).
                Global gradient wrt the input X.
        """
        # global gradients of parameters
        dgamma = np.sum(self.cache['scaled'] * dY, axis=(0, 2, 3), keepdims=True)
        dbeta = np.sum(dY, axis=(0, 2, 3), keepdims=True)

        # caching global gradients of parameters
        self.weight_update['gamma'] = dgamma
        self.weight_update['beta'] = dbeta

        # global gradient of the input
        dX = self.grad['X'] * dY

        return dX

    def local_grad(self, X):
        """
        Calculates the local gradient for X.

        Args:
            dY: numpy.ndarray of shape (n_batch, n_channels, height, width).

        Returns:
            grads: dictionary of gradients.
        """
        # global gradient of the input
        N, C, H, W = X.shape
        # ppc = pixels per channel, useful variable for further computations
        ppc = H * W

        # gradient for 'denominator path'
        dsqrt_invvar = self.cache['centered']
        dinvvar = (1.0 / (2.0 * np.sqrt(self.cache['invvar']))) * dsqrt_invvar
        dvar = (-1.0 / self.cache['var'] ** 2) * dinvvar
        ddenominator = (X - self.cache['mean']) * (2 * (ppc - 1) / ppc ** 2) * dvar

        # gradient for 'numerator path'
        dcentered = self.cache['sqrt_invvar']
        dnumerator = (1.0 - 1.0 / ppc) * dcentered

        dX = ddenominator + dnumerator
        grads = {'X': dX}
        return grads

class Flatten(Function):
    def forward(self, X):
        self.cache['shape'] = X.shape
        n_batch = X.shape[0]
        return X.reshape(n_batch, -1)

    def backward(self, dY):
        return dY.reshape(self.cache['shape'])



