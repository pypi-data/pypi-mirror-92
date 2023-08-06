import numpy as np
from Terminatetensorflow.actvfn import *

class layer:
    def __init__(self, output_dims, input_dims, act_fn):
        self.weights = np.random.randn(output_dims, input_dims) * np.sqrt(2/input_dims)
        self.biases = np.zeros((output_dims,1))
        self.act_fn = act_fn
        self.Z = None
        self.A = None     
        self.dW = np.zeros((output_dims, input_dims))
        self.db = np.zeros((output_dims,1))
        self.dZ = None
        self.dA = None
        self.v_w = np.zeros((output_dims, input_dims))
        self.v_b = np.zeros((output_dims,1))
        self.s_w = np.zeros((output_dims, input_dims))
        self.s_b = np.zeros((output_dims,1))
        
        
    def forward_prop(self, input):
        self.Z = np.dot(self.weights, input) + self.biases
        
        
        if self.act_fn == "sigmoid":
            self.A = sigmoid(self.Z)
        if self.act_fn == "relu":
            self.A = relu(self.Z)
        if self.act_fn == "tanh":
            self.A = tanh(self.Z)
        if self.act_fn == "linear":
            self.A = linear(self.Z)
        if self.act_fn == "softmax":
            self.A = softmax(self.Z)
            
        return self.A
        
    def backward_prop(self, prev_A, dA_prev, y, output_layer = False):
        
        if output_layer is True:
            self.dZ = self.A - y            
            self.dW = (1./y.shape[1]) * np.dot(self.dZ, prev_A.T)
            self.db = (1./y.shape[1]) * np.sum(self.dZ, axis=1, keepdims=True)
            dA_prev = np.dot(self.weights.T, self.dZ)
               
        else:
            if self.act_fn == "sigmoid":
                self.dZ = dA_prev * derivative_sigmoid(self.Z)
            elif self.act_fn == "tanh":
                self.dZ = dA_prev * derivative_tanh(self.Z)
            elif self.act_fn == "relu":
                self.dZ = dA_prev * d_relu(self.Z)
            elif self.act_fn == "linear":
                self.dZ = dA_prev * d_linear(self.Z)
                
            self.dW = (1./y.shape[1]) * np.dot(self.dZ, prev_A.T)
            self.db = (1./y.shape[1]) * np.sum(self.dZ, axis=1, keepdims=True)
            dA_prev = np.dot(self.weights.T, self.dZ)
            
        return dA_prev, self.dW, self.db
    
    def update_parameters(self, learning_rate):
        self.weights = self.weights -  learning_rate * self.dW
        self.biases= self.biases -  learning_rate * self.db

    def update_parameters_momentum(self, learning_rate, gamma=0.9):
        self.v_w = gamma*self.v_w +  (1 - gamma)* self.dW
        self.v_b = gamma*self.v_b +  (1 - gamma)* self.db
        self.weights = self.weights - learning_rate * self.v_w
        self.biases = self.biases -  learning_rate  *  self.v_b
        
    def update_parameters_rmsprop(self, learning_rate, beta=0.9, epsilon = 1e-8):
        self.s_w = beta*self.s_w +  (1 - beta)* np.power(self.dW,2)
        self.s_b = beta*self.s_b +  (1 - beta)* np.power(self.db,2)
        self.weights = self.weights - learning_rate * np.divide(self.dW,np.sqrt(self.s_w + epsilon))
        self.biases = self.biases -  learning_rate  *  np.divide(self.db,np.sqrt(self.s_b + epsilon))

        
    def update_parameters_adam(self, learning_rate, t = 2, beta1 = 0.9, beta2 = 0.999,  epsilon = 1e-8):
        self.v_w = beta1*self.v_w +  (1 - beta1)* self.dW
        self.v_b = beta1*self.v_b +  (1 - beta1)* self.db
        v_wcorrected = self.v_w / (1-np.power(beta1,t))
        v_bcorrected = self.v_b / (1-np.power(beta1,t))
        self.s_w = beta2*self.s_w + (1-beta2)*np.power(self.dW,2)
        self.s_b = beta2*self.s_b + (1-beta2)*np.power(self.db,2)
        s_wcorrected = self.s_w / (1-np.power(beta2,t))
        s_bcorrected = self.s_b / (1-np.power(beta2,t))
        self.weights = self.weights - learning_rate*v_wcorrected / np.sqrt(s_wcorrected + epsilon)
        self.biases = self.biases - learning_rate*v_bcorrected / np.sqrt(s_bcorrected + epsilon)

