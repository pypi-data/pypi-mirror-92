from Activations import *
from Function import Function
from math import sqrt
from Utils import *

class Layer(Function):

    def __init__(self, Input_Matrix, Output_Dimension, Activation_fn, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_layer = False
        self.inputs =np.array(Input_Matrix)
        self.in_dimension = self.inputs.shape[0]
        self.out_dimension = Output_Dimension
        self._init_weights(self.in_dimension,self.out_dimension)
        #self.inputs = np.array(Input_Matrix).reshape(len(Input_Matrix), -1)
        self.weights_gradients = {}
        self.bias_gradients = {}
        self.act_fn_name = Activation_fn
        self.activation_Fn = get_activation(Activation_fn)
        self()

    def update_weights(self, Weights, Bias):  # bn callha f el optization 3la kol layer
        self.weights = Weights
        self.bias = Bias
        self()  # deh bt call el layer nafsha fa bt7sb el formward w el grad w kda
        # m7tag hena a recalcuate el output w el grad w el backprop bta3 kol el layers # mosh kol layer el layer el na feha bas w el optimization t loop 3la kol el layers

    def output(self):

        out = self.cache['A'].Activation_Output
        return out

    def _init_weights(self, in_dimension, out_dimension):
        scale = 1 / sqrt(self.in_dimension)

        self.weights = scale * np.random.randn(self.out_dimension,self.in_dimension)
        self.bias = scale * np.random.randn(self.out_dimension,1)

    def initialize_layers(self, dim_list, input_x):
        w = {}
        b = {}
        layers = {}
        for i in range(0, len(dim_list)):
            w[i] = np.random.rand(dim_list[i])
            b[i] = np.random.rand((1, 1))

        layers[0] = Layer(input_x, w[0], b[0])
        for i in range(1, len(dim_list)):
            layers[i] = Layer(layers[i - 1].output(), w[i], b[i])

        return layers





class Linear(Layer):

    def forward_pass(self):
        Z = np.dot(self.weights, self.inputs) + self.bias
        A = self.activation_Fn(Z)
        self.cache['X'] = self.inputs  # Z1 = W1 . X + b1
        self.cache['Z'] = Z  # A1 = f1(Z1)
        self.cache['A'] = A

        return A

    def local_gradient(self):
        gradient_X_L = self.weights
        gradient_W_L = self.inputs
        gradient_B_L = np.ones(self.bias.shape, dtype='float16')
        self.grad = {'dZ': gradient_X_L, 'dW': gradient_W_L, 'db': gradient_B_L}
        return self.grad

    def backward_pass(self, dG):
        Z = self.cache['Z']
        dA = np.multiply(dG, self.activation_Fn.grad['dA'])
        dX = np.dot(self.grad['dZ'].T, dA)  # m7tag a3dl henaa
        dW = np.dot(dA, self.grad['dW'].T)
        db = np.sum(dA, axis=1, keepdims=True)  # changed here none to 0
        self.weights_gradients = {'W': dW}
        self.bias_gradients = {'b': db}
        return dX



class Conv(Function):


    def __init__(self,X,in_channels, out_channels, kernel_size=3, stride=1, padding=0 , Activation_fn = 'relu'):
        super().__init__()
        self.last_layer = False
        self.cache['X'] = X
        self.inputs = X
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.stride = stride
        self.kernel_size = kernel_size
        self.padding = padding
        self._init_weights(in_channels, out_channels, self.kernel_size)
        self.act_fn_name = Activation_fn
        self.activation_Fn = get_activation(Activation_fn)
        self.weights_gradients = {}
        self.bias_gradients = {}
        self.grad = {}

    def _init_weights(self, in_channels, out_channels, kernel_size):
        scale = 2/sqrt(in_channels*kernel_size*kernel_size)

        self.weights = np.random.normal(scale=scale,size=(out_channels, in_channels, kernel_size , kernel_size))
        self.bias = np.zeros(shape=(out_channels, 1))

    def update_weights(self, Weights, Bias):  # bn callha f el optization 3la kol layer

        self.weights = Weights
        self.bias = Bias
        self()

    def output(self):

        self.forward_pass()
        out = self.cache['A'].Activation_Output
        return out


    def forward_pass(self):


        X = self.cache['X']

        m, n_C_prev, n_H_prev, n_W_prev = X.shape

        n_C = self.out_channels

        n_H = int((n_H_prev + 2 * self.padding - self.kernel_size)/ self.stride) + 1

        n_W = int((n_W_prev + 2 * self.padding - self.kernel_size)/ self.stride) + 1

        X_col = im2col(X, self.kernel_size, self.kernel_size, self.stride, self.padding)

        w_col = self.weights.reshape(self.out_channels, -1)

        b_col = self.bias.reshape(-1, 1)


        out = w_col @ X_col + b_col

        out = np.array(np.hsplit(out, m)).reshape((m, n_C, n_H, n_W))

        self.cache['X'] = X

        self.cache['other'] = X_col, w_col

        self.cache['Z'] = out

        A = self.activation_Fn(out)

        self.cache['A'] = A

        return A


    def backward_pass(self, dY):


        X = self.cache['X']
        X_col, w_col = self.cache['other']

        m, _, _, _ = X.shape


        #self.grad['db'] = np.sum(dY, axis=(0,2,3))
        db = np.sum(dY, axis=(0,2,3))

        db = db.reshape(self.bias.shape)

        self.bias_gradients['b'] = db

        dY = dY.reshape(dY.shape[0] * dY.shape[1], dY.shape[2] * dY.shape[3])

        dY = np.array(np.vsplit(dY, m))

        dY = np.concatenate(dY, axis=-1)

        dX_col = w_col.T @ dY

        dw_col = dY @ X_col.T

        dX = col2im(dX_col, X.shape, self.kernel_size, self.kernel_size, self.stride, self.padding)

        #self.grad['dW'] = dw_col.reshape((dw_col.shape[0], self.in_channels, self.kernel_size, self.kernel_size))

        dw = dw_col.reshape((dw_col.shape[0], self.in_channels, self.kernel_size, self.kernel_size))


        self.weights_gradients['W'] = dw

        #self.weights_gradients['W'] = self.grad['dW']

        #self.bias_gradients['b'] = self.grad['db']

        return dX

class MaxPool(Function):

    def __init__(self,X,kernel_size=3, stride=1, padding=0):

        super().__init__()

        self.cache['X'] = X
        self.inputs = X
        self.stride = stride
        self.kernel_size = kernel_size
        self.padding = padding
        self.last_layer = False
        self.weights = np.zeros((1,1))
        self.bias = np.zeros((1,1))
        self.weights_gradients = {'W' : np.zeros((1,1))}
        self.bias_gradients = {'b' : np.zeros((1,1))}


    def output(self):

        return self.forward_pass()

    def update_weights(self, Weights, Bias):  # bn callha f el optization 3la kol layer

        self.weights = Weights
        self.bias = Bias
        self()  


    def forward_pass(self):

        X = self.cache['X']

        m, n_C_prev, n_H_prev, n_W_prev = X.shape

        n_C = n_C_prev

        n_H = int((n_H_prev + 2 * self.padding - self.kernel_size)/ self.stride) + 1

        n_W = int((n_W_prev + 2 * self.padding - self.kernel_size)/ self.stride) + 1


        X_col = im2col(X, self.kernel_size, self.kernel_size, self.stride, self.padding)

        X_col = X_col.reshape(n_C, X_col.shape[0]//n_C, -1)

        M_pool = np.max(X_col, axis=1)

        M_pool = np.array(np.hsplit(M_pool, m))

        M_pool = M_pool.reshape(m, n_C, n_H, n_W)

        self.cache['A'] = M_pool

        return M_pool

    def backward_pass(self, dY):

        X = self.cache['X']

        m, n_C_prev, n_H_prev, n_W_prev = X.shape

        n_C = n_C_prev

        n_H = int((n_H_prev + 2 * self.padding - self.kernel_size)/ self.stride) + 1

        n_W = int((n_W_prev + 2 * self.padding - self.kernel_size)/ self.stride) + 1

        dY_flatten = dY.reshape(n_C, -1) / (self.kernel_size * self.kernel_size)

        dX_col = np.repeat(dY_flatten, self.kernel_size*self.kernel_size, axis=0)

        dX = col2im(dX_col, X.shape, self.kernel_size, self.kernel_size, self.stride, self.padding)

        dX = dX.reshape(m, -1)

        dX = np.array(np.hsplit(dX, n_C_prev))

        dX = dX.reshape(m, n_C_prev, n_H_prev, n_W_prev)

        return dX


class AvgPool(Function):

    def __init__(self,X,kernel_size=3, stride=1, padding=0):

        super().__init__()

        self.cache['X'] = X
        self.stride = stride
        self.kernel_size = kernel_size
        self.padding = padding
        self.has_weights = False


    def forward_pass(self):

        X = self.cache['X']
        
        m, n_C_prev, n_H_prev, n_W_prev = X.shape

        n_C = n_C_prev

        n_H = int((n_H_prev + 2 * self.padding - self.kernel_size)/ self.stride) + 1

        n_W = int((n_W_prev + 2 * self.padding - self.kernel_size)/ self.stride) + 1


        X_col = im2col(X, self.kernel_size, self.kernel_size, self.stride, self.padding)

        X_col = X_col.reshape(n_C, X_col.shape[0]//n_C, -1)

        A_pool = np.mean(X_col, axis=1)

        A_pool = np.array(np.hsplit(A_pool, m))

        A_pool = A_pool.reshape(m, n_C, n_H, n_W)


        return A_pool

    def backward_pass(self, dY):


        X = self.cache['X']

        m, n_C_prev, n_H_prev, n_W_prev = X.shape

        n_C = n_C_prev

        n_H = int((n_H_prev + 2 * self.padding - self.kernel_size)/ self.stride) + 1

        n_W = int((n_W_prev + 2 * self.padding - self.kernel_size)/ self.stride) + 1

        dY_flatten = dY.reshape(n_C, -1) / (self.kernel_size * self.kernel_size)

        dX_col = np.repeat(dout_flatten, self.kernel_size*self.kernel_size, axis=0)

        dX = col2im(dX_col, X.shape, self.kernel_size, self.kernel_size, self.stride, self.padding)

        dX = dX.reshape(m, -1)

        dX = np.array(np.hsplit(dX, n_C_prev))

        dX = dX.reshape(m, n_C_prev, n_H_prev, n_W_prev)

        return dX

class Flatten(Function):

    def __init__(self,X):

        super().__init__()
        self.inputs = X
        self.last_layer = False
        self.cache['X'] = X
        self.weights = np.zeros((1,1))
        self.bias = np.zeros((1,1))
        self.weights_gradients = {'W' : np.zeros((1,1))}
        self.bias_gradients = {'b' : np.zeros((1,1))}


    def output(self):

        return self.forward_pass()
    def forward_pass(self):

        X = self.cache['X'] 
        self.cache['shape'] = X.shape

        n_batch = X.shape[0]
        return X.reshape(n_batch, -1)

    def backward_pass(self, dY):
        dX = dY.reshape(self.cache['shape'])
        return dX

    def update_weights(self, Weights, Bias):  # bn callha f el optization 3la kol layer

        self.weights = Weights
        self.bias = Bias
        self()  