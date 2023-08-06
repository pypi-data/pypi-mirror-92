from .Activation import activation
import numpy as np


class layer():
    def __init__(self, in_nodes=0, out_nodes=0, activation_type=""):
        self.w = np.random.randn(out_nodes, in_nodes)*0.01
        self.dw = np.zeros((out_nodes, in_nodes))
        self.b = np.zeros((out_nodes, 1))
        self.db = np.zeros((out_nodes, 1))
        self.act_func = activation(activation_type)
    
    def forward(self, X):
        # X dimensions are (number of input nodes) x (number of examples)
        Z = self.w @ X + self.b  # Z = w * X + b
        weights_sum=np.sum(np.square(self.w))
        output = self.act_func.forward(Z)  # A = activation(Z)
        self.X = X  # cache input to use it in back prop
        return output, weights_sum

    def backward(self, dA, Lambda):
        # dA dimensions are (number of output nodes) x (number of examples)
        m = dA.shape[1]
        dZ = self.act_func.backward(dA) # dZ = dA . g'(Z) (element wise product)
        self.dw = (1/m) * dZ @ self.X.T + (Lambda/m) * self.w   # dw = dZ * X.T+(lambda/m) * w 
        self.db = (1/m) * np.sum(dZ, axis=1, keepdims=True) # db = 1/m * sum(dZ)
        grad_input = self.w.T @ dZ
        return grad_input

    def output_dims(self):
        return self.b.shape[0]
    
    def getParams(self):
        return self.w, self.b

    def getGrads(self):
        return self.dw, self.db

    def setParams(self, w, b):
        self.w = w
        self.b = b
        
    def getLayerParams(self):
        LayerParams = self.w, self.b, self.act_func.activation_type
        return "layer", LayerParams

    def setLayerParams(self, LayerParams):
        self.w, self.b , activation_type = LayerParams
        self.act_func = activation(activation_type)
        
'''
in_nodes = 2
out_nodes = 3
activation_type = "Relu"  # (Relu, Sigmoid, Linear)
L = layer(in_nodes, out_nodes, activation_type)
w,b = L.getParams()
w = w + 5
b = np.ones((out_nodes, 1))
L.setParams(w, b)
print('Weights=\n',w,"\nb=\n",b)

# testing forward propagation

X = np.array([
    [0, 1, 2],
    [1, 4, 3]
])
A = L.forward(X)
# print("\n\nfor input=\n",X,"\noutput=\n",A)

# testing back propagation

dw, db = L.getGrads()
print('dw=\n', dw, "\ndb=\n", db)
dA = np.array([
    [1, 9, 7],
    [6, 1, 2],
    [4, 5, 8]
])
print("\n\nfor dA=\n\n", dA)
dw, db = L.getGrads()
dX = L.backward(dA)
print('dw=\n', dw, "\ndb=\n", db, "\ndX=\n", dX)
'''
