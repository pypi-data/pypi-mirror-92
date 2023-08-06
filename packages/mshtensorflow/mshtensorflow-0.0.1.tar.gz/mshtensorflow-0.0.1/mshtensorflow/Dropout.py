import numpy as np

class dropout():
    def __init__(self, prob=0.5, input_dim=(0, 0, 0)):
        self.prob = prob
        self.input_dim = input_dim

    def forward(self, input):
        self.U = np.random.random_sample(input.shape)
        self.U = self.U < (1-self.prob)
        # print(1-np.mean(self.U))
        self.U = self.U / (1-self.prob)
        out = input * self.U
        return out, 0

    def backward(self, dout, Lambda=0):
            dX = dout * self.U
            return dX

    def getGrads(self):
        return None

    def output_dims(self):
        return self.input_dim

    def getLayerParams(self):
        LayerParams = self.input_dim, self.prob
        return "dropout", LayerParams

    def setLayerParams(self, LayerParams):
        self.input_dim,self.prob = LayerParams

# array= np.arange(100000)
# array2 = array < 0.5
# print(array2)
# print(array)
# D1= dropout(0.5, 0)
# forward= D1.forward(array)
# print(forward)
# backward= D1.backward(array)
# print(backward)

