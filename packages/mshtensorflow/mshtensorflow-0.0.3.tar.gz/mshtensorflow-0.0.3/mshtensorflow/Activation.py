import numpy as np

class activation:
    def __init__(self, activation_type):
        self.activation_type = activation_type
        A=0
        self.A= A

    def forward(self, Z):

        if self.activation_type =="Linear":
           return Z

        elif self.activation_type == "Sigmoid":

            self.A = np.divide(1, 1+np.exp(-Z))

        elif self.activation_type == "Relu":
            self.A = np.maximum(0,Z)

        return self.A

    def backward(self,dA):

        if self.activation_type == "Linear":
            return dA

        elif self.activation_type == "Sigmoid":
            dZ = dA * self.A * (1 - self.A)

        elif self.activation_type == "Relu":

            dZ = np.multiply(dA, np.int64(self.A > 0))

        return dZ







