import numpy as np
from Function import Function


class Loss(Function):
    def __init__(self, Y, Y_hat, cache, weights, bias, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Y_hat = np.array(Y_hat)
        self.Y = np.array(Y)
        #self.Y = np.reshape(self.Y, np.shape(self.Y_hat))

        self.flag = 0

        self.layer_cache = cache
        self.layer_weights = weights
        self.layer_bias = bias

        self.Loss_Value = self.forward_pass()
        self.local_gradient()

    def backward_pass(self):
        # Since it is the final layer the backward pass is the same as the local gradient
        # self.Y_hat = self.layer_cache['A'].forward()
        if self.flag == 2:
            self()
        return self.grad['dL']

    def MSE(self):
        Mse_Loss = MSE((self.Y), (self.Y_hat), self.layer_cache, self.layer_weights, self.layer_bias)
        return Mse_Loss

    def SignLoss(self):
        Sign_Loss = SignLoss((self.Y), (self.Y_hat), self.layer_cache, self.layer_weights, self.layer_bias)
        return Sign_Loss

    def SVMLoss(self):
        SVM_Loss = SVMLoss((self.Y), (self.Y_hat), self.layer_cache, self.layer_weights, self.layer_bias)
        return SVM_Loss

    def LogisticRegressionSigmoid(self):
        LogisticRegressionSigmoid_loss = LogisticRegressionSigmoid((self.Y), (self.Y_hat), self.layer_cache,
                                                                   self.layer_weights, self.layer_bias)
        return LogisticRegressionSigmoid_loss

    def LogisticRegressionIdentity(self):
        LogisticRegressionIdentity_loss = LogisticRegressionIdentity((self.Y), (self.Y_hat), self.layer_cache,
                                                                   self.layer_weights, self.layer_bias)
        return LogisticRegressionIdentity_loss

    def CrossEntropy(self):
        Cross_Loss = CrossEntropy((self.Y), (self.Y_hat), self.layer_cache, self.layer_weights, self.layer_bias)
        return Cross_Loss


class MSE(Loss):
    def forward_pass(self):
        L = np.mean((self.Y - self.Y_hat) ** 2, axis=1, keepdims=True) / 2
        self.cache['Loss'] = L
        return L

    def local_gradient(self):
        self.grad = {'dL': ((self.Y_hat - self.Y) / self.Y_hat.shape[1])}
        self.flag = 1
        return self.grad


class SignLoss(Loss):
    def forward_pass(self):
        L = np.mean(np.max(0, -(np.dot(self.Y, self.Y_hat))), axis=1, keepdims=True)
        self.cache['Loss'] = L
        return L

    def local_gradient(self):
        #self.grad = {'dL': (- (np.dot(self.Y, self.layer_cache['X'])))}
        self.grad = {'dL': (- self.Y)/ self.Y_hat.shape[1]}
        return self.grad


class SVMLoss(Loss):
    def forward_pass(self):
        L = np.mean(np.max(0, -(np.dot(self.Y, self.Y_hat)) + 1), axis=1, keepdims=True)
        self.cache['Loss'] = L
        return L

    def local_gradient(self):
        #self.grad = {'dL': (- (np.dot(self.Y, self.cache['X'])))}  # X is not defined here yet
        self.grad = {'dL': (- self.Y)/ self.Y_hat.shape[1]}
        return self.grad


class LogisticRegressionSigmoid(Loss):
    def forward_pass(self):
        L = np.mean(-np.log(np.absolute((self.Y / 2) - (1 / 2) + self.Y_hat)), axis=1, keepdims=True)
        self.cache['Loss'] = L
        return L

    def local_gradient(self):
        # self.grad = {'dL': (- (np.multiply(self.Y, self.layer_cache['X'])) / (1 + np.exp(np.multiply(self.Y, np.dot(self.layer_weights,self.layer_cache['X'])))))}
        self.grad = {'dL': (-(1 / (self.Y / 2) - (1 / 2) + self.Y_hat)) / self.Y_hat.shape[1]}

        return self.grad

class LogisticRegressionIdentity_loss(Loss):
    def forward_pass(self):
        L = np.mean(np.log(1+np.exp(np.dot(-self.Y,self.Y_hat))), axis=1, keepdims=True)
        self.cache['Loss'] = L
        return L

    def local_gradient(self):
        # self.grad = {'dL': (- (np.multiply(self.Y, self.layer_cache['X'])) / (1 + np.exp(np.multiply(self.Y, np.dot(self.layer_weights,self.layer_cache['X'])))))}
        self.grad = {'dL': ( np.exp(np.dot(-self.Y,self.Y_hat)*-self.Y)/(1+np.exp(np.dot(-self.Y,self.Y_hat)))) /self.Y_hat.shape[1]}

        return self.grad
class CrossEntropy(Loss): #######33 used for softmax only
    def forward_pass(self):

        log_Y_hat = -np.log(np.abs([self.Y_hat[(self.Y[i]),i] for i in range(np.shape(self.Y_hat)[1])]))

        log_Y_hat[np.isnan(log_Y_hat)] = 0
        crossentropy_loss = np.mean(log_Y_hat)
        self.cache['Loss'] = crossentropy_loss
        return crossentropy_loss

    def local_gradient(self):

        for i in range(np.shape(self.Y_hat)[1]):
            self.Y_hat[self.Y[i],i] =self.Y_hat[self.Y[i],i] -1

        self.grad = {'dL': self.Y_hat/np.shape(self.Y_hat)[1]}
        #self.grad = {'dL': (self.Y_hat - np.ones_like(self.Y_hat)) / float(len(self.Y))} ############           need to check for yi!=r
        return self.grad

        '''
        ones = np.zeros(self.Y_hat.shape, dtype='float16')
        for row_idx, col_idx in enumerate(self.Y):
            ones[row_idx, col_idx] = 1.0


def get_loss(loss):
    if (loss == 'mse'):
        return MSE()
    elif (loss == 'sign'):
        return SignLoss()
    elif (loss == 'svm'):
        return HingeLoss()
    elif (loss == 'crossentropy'):
        return CrossEntropy()
'''

'''
y = np.random.rand(3,1)
y_cap = np.random.rand(3,1)
Loss = Loss.MSE(y,y_cap)
print(Loss.Y_hat)
'''
