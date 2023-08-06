import numpy as np
class Activation:
    '''
    This class encapsulates the following activation functions: ReLU, sigmoid, tanh.
    This class aims to apply one activation function to a given input. 
    The class contains one attribute that determines which activation function is applied to the input given to the ActivationFn method.  
    The class is meant to be accessed through the following functions: init, ActivationFn and DerivativeFn.
    '''
    def __init__(self, activation="relu"):
        '''
        The __init__ function is called whenever the class is instantiated. 
        Arguments:
            activation: String represents the activation function that the instance object will be representing.
        '''
        self.activation=activation

    def sigmoid(self, z):
        '''
        Computes the sigmoid of the input z (array of predictions).
        '''
        s = 1/(1+np.exp(-z))     
        return s

    def tanh(self, z):
        '''
        Computes the tanh of the input z (array of predictions).
        '''
        s = (np.exp(z)-np.exp(-z))/(np.exp(z)+np.exp(-z))    
        return s
        
    def relu(self, x):
        '''
        Computes the max of the input x (array of predictions) and zero. This max is technically the ReLU.
        '''
        s = np.maximum(0,x)    
        return s

    def sigmoid_derivative(self, x):
        '''
        Computes the derivative of the sigmoid with respect to the input x (array of predictions).
        '''
        s = self.sigmoid(x)
        ds = s*(1-s)
        return ds

    def tanh_derivative(self, x):
        '''
        Computes the derivative of the tanh with respect to the input x (array of predictions).
        '''
        t = self.tanh(x)
        dt = 1-np.power(t, 2)
        return dt

    def relu_derivative(self, x):
        '''
        Computes the derivative of the ReLU with respect to the input x (array of predictions).
        '''
        return x>0     

    def softmax(self, x):
        '''
        Computes the softmax of the input x (array of predictions).
        '''
        exps=np.exp(x)
        return exps/np.sum(exps)

    def DerivativeFn(self, x):
        '''
        Computes the derivative of the activation function with respect to the input (array of predictions). This function is meant to be the entry point when computing the derivative i.e. don't call the specific derivative functions.
        '''
        if self.activation=="relu":
            return self.relu_derivative(x)
        elif self.activation=="tanh":
            return self.tanh_derivative(x)    
        elif self.activation=="sigmoid":
            return self.sigmoid_derivative(x)
        # elif self.activation=="softmax":
        #     return self.softmax_derivative(x)
            
    def ActivationFn(self, x):
        '''
        Computes the activation function with respect to the input (array of predictions). This function is meant to be the entry point when computing the activation i.e. don't call the specific activation functions.
        '''
        if self.activation=="relu":
            return self.relu(x)
        elif self.activation=="tanh":
            return np.tanh(x)    
        elif self.activation=="sigmoid":
            return self.sigmoid(x)
        elif self.activation=="softmax":
            return self.softmax(x) 
