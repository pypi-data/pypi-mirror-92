from .Activation import activation
import numpy as np

class conv_layer():
   
    def __init__(self,  Filter=2, num_of_filters=5, Stride=1, padding=0, activation_type="Linear", input_dimensions=(1,1,1)):
        
        self.act_func = activation(activation_type)
        self.S = Stride
        self.P = padding
        
        try:
            FH, FW = Filter    # Filter is tuple (3,4)
        except:
            FH = Filter   # Filter is an integer [square filter]
            FW = Filter 
        
        # input_dimensions is tuple (32, 32, 3)
        n_H_prev, n_W_prev, n_C_prev = input_dimensions 
        
        # layer parameters
        # filters dimensions are (n,c,h,w)
        self.filters = np.random.randn(num_of_filters, n_C_prev, FH, FW ) * 0.01
        self.b = np.zeros(num_of_filters)
        
        # the dimensions of output
        self.n_H = int(((n_H_prev+2*self.P-FH)/self.S)+1)
        self.n_W = int(((n_W_prev+2*self.P-FW)/self.S)+1)
        self.n_C = num_of_filters
        
    def forward(self, X):
        # X dimensions are (n,c,h,w)
        # number of examples
        m, _,_,_ = X.shape
        
        # filter dimensions
        n_F, n_C_prev, FH, FW = self.filters.shape
        
        X_col = im2col(X, FH, FW, self.S, self.P)
        filter_col = self.filters.reshape((n_F, -1))
        b_col = self.b.reshape(-1, 1)
       
        # Perform matrix multiplication.
        out = filter_col @ X_col + b_col
        
        # Reshape back matrix to image.
        out = np.array(np.hsplit(out, m)).reshape(m, self.n_C, self.n_H, self.n_W)
        
        # apply activation function
        out = self.act_func.forward(out)
        
        #Cache inputs for back propagation
        self.cache = X.shape, X_col, filter_col
        
        return out, 0

    def backward(self, dA, Lambda=0):
        # dA dimensions are (n,c,h,w)
        # number of examples
        m, _,_,_ = dA.shape
        
        # retieve cache
        X_shape, X_col, filter_col = self.cache
        
        # filter dimensions
        _, n_C_prev, FH, FW = self.filters.shape
        
        # back propagate from activation function
        dA = self.act_func.backward(dA) 
        
        # back propagate from convolution
        # Compute bias gradient.
        self.db = np.sum(dA, axis=(0,2,3))
        
        # Reshape dA
        dA = dA.reshape(dA.shape[0] * dA.shape[1], dA.shape[2] * dA.shape[3])
        dA = np.array(np.vsplit(dA, m))
        dA = np.concatenate(dA, axis=-1)
        
        # Perform matrix multiplication between reshaped dout and filter_col to get dX_col.
        dX_col = filter_col.T @ dA
        
        # Perform matrix multiplication between reshaped dout and X_col to get dfilter_col.
        dfilter_col = dA @ X_col.T
        
        # Reshape back to image (col2im).
        dX = col2im(dX_col, X_shape, FH, FW, self.S, self.P)
        # dX = col2im_indices(dX_col, X_shape, FH, FW, self.P, self.S)
        
        # Reshape dfilter_col into dw.
        self.dfilters = dfilter_col.reshape((dfilter_col.shape[0], n_C_prev, FH, FW))
    
        return dX

    def output_dims(self):
        return self.n_H, self.n_W, self.n_C
    
    def getParams(self):
        return self.filters, self.b

    def getGrads(self):
        return self.dfilters, self.db    

    def setParams(self, filters, b):
        self.filters = filters
        self.b = b
        
    def getLayerParams(self):
        LayerParams = self.filters, self.b, self.S, self.P, self.n_H, self.n_W, self.n_C, self.act_func.activation_type
        return "conv_layer", LayerParams

    def setLayerParams(self, LayerParams):
        self.filters, self.b, self.S, self.P, self.n_H, self.n_W, self.n_C, activation_type = LayerParams
        self.act_func = activation(activation_type)




def get_indices(X_shape, HF, WF, stride, pad):
    
    # get input size
    m, n_C, n_H, n_W = X_shape

    # get output size
    out_h = int((n_H + 2 * pad - HF) / stride) + 1
    out_w = int((n_W + 2 * pad - WF) / stride) + 1
  
    # ----Compute matrix of index i----

    # Level 1 vector.
    level1 = np.repeat(np.arange(HF), WF)
    # Duplicate for the other channels.
    level1 = np.tile(level1, n_C)
    # Create a vector with an increase by 1 at each level.
    everyLevels = stride * np.repeat(np.arange(out_h), out_w)
    # Create matrix of index i at every levels for each channel.
    i = level1.reshape(-1, 1) + everyLevels.reshape(1, -1)

    # ----Compute matrix of index j----
    
    # Slide 1 vector.
    slide1 = np.tile(np.arange(WF), HF)
    # Duplicate for the other channels.
    slide1 = np.tile(slide1, n_C)
    # Create a vector with an increase by 1 at each slide.
    everySlides = stride * np.tile(np.arange(out_w), out_h)
    # Create matrix of index j at every slides for each channel.
    j = slide1.reshape(-1, 1) + everySlides.reshape(1, -1)

    # ----Compute matrix of index d----

    # This is to mark delimitation for each channel
    # during multi-dimensional arrays indexing.
    d = np.repeat(np.arange(n_C), HF * WF).reshape(-1, 1)

    return i, j, d

def im2col(X, HF, WF, stride, pad):

    # Padding
    X_padded = np.pad(X, ((0,0), (0,0), (pad, pad), (pad, pad)), mode='constant')
    i, j, d = get_indices(X.shape, HF, WF, stride, pad)
    
    # Multi-dimensional arrays indexing.
    cols = X_padded[:, d, i, j]
    cols = np.concatenate(cols, axis=-1)
    return cols

def col2im(dX_col, X_shape, HF, WF, stride, pad):
    # Get input size
    N, D, H, W = X_shape
    
    H_padded, W_padded = H + 2 * pad, W + 2 * pad
    X_padded = np.zeros((N, D, H_padded, W_padded))
    
    # Index matrices, necessary to transform our input image into a matrix. 
    i, j, d = get_indices(X_shape, HF, WF, stride, pad)
    
    # Retrieve batch dimension by spliting dX_col N times: (X, Y) => (N, X, Y)
    dX_col_reshaped = np.array(np.hsplit(dX_col, N))
    
    # Reshape our matrix back to image.
    # slice(None) is used to produce the [::] effect which means "for every elements".
    np.add.at(X_padded, (slice(None), d, i, j), dX_col_reshaped)
    
    # Remove padding from new image if needed.
    if pad == 0:
        return X_padded
    elif type(pad) is int:
        return X_padded[:,:,pad:-pad, pad:-pad]

# forward and backward propagation

'''
activation_type="Linear"
Filter = 2
num_of_filters = 8
input_dimensions = (4, 4, 3)
Stride = 2 
padding = 2
conv = conv_layer(Filter, num_of_filters, Stride, padding, activation_type, input_dimensions)

np.random.seed(1)
X = np.random.randn(10,4,4,3).transpose(0,3,1,2)
filters = np.random.randn(2,2,3,8).transpose(3,2,0,1)
b = np.random.randn(8)
conv.setParams(filters, b)

A,_ = conv.forward(X)
print("A's mean =", np.mean(A.transpose(0,2,3,1)))
print("A[3,2,1] =", A.transpose(0,2,3,1)[3,2,1])

dX = conv.backward(A).transpose(0,2,3,1)
dfilters, db = conv.getGrads()
dfilters = dfilters.transpose(2,3,1,0)
db = db
print("dX_mean =", np.mean(dX))
print("dfilters_mean =", np.mean(dfilters))
print("db_mean =", np.mean(db))
'''

# # Pytorch
# W, b = conv.getParams()
# import torch 
# import torch.nn as nn
# inputs_pt = torch.Tensor(X).double()
# conv_pt = nn.Conv2d(3, 2, 2, stride=2, padding=2, bias=True)
# conv_pt.weight = nn.Parameter(torch.DoubleTensor(W))
# conv_pt.bias = nn.Parameter(torch.DoubleTensor(b))
# out_pt = conv_pt(inputs_pt) # Forward.
# out_pt.backward(torch.Tensor(A)) # Backward.


# storing and loading

'''
par = conv.getLayerParams()

conv2=conv_layer()
conv2.setLayerParams(par)
A = conv2.forward(X)
print("\n\n\nA's mean =", np.mean(A))
print("A[3,2,1] =", A[3,2,1])

dX=conv2.backward(A)
dfilters, db = conv2.getGrads()
print("dX_mean =", np.mean(dX))
print("dfilters_mean =", np.mean(dfilters))
print("db_mean =", np.mean(db))
'''
