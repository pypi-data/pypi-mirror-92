import numpy as np

class pool_layer():
    def __init__(self, Filter=2, Stride=1, mode = "max", input_dimensions=(1,1,1)):
        
        self.mode = mode # maxpool (max) or average pool (average)
        self.S = Stride
        
        try:
            FH, FW = Filter    # Filter is tuple (3,4)
        except:
            FH = Filter   # Filter is an integer [square filter]
            FW = Filter 
       
        self.FH = FH
        self.FW = FW
        
        # input_dimensions is tuple (32, 32, 3)
        self.h_X, self.w_X, self.d_X = input_dimensions
        
        
        # the dimensions of output
        n_H_prev, n_W_prev, n_C_prev = input_dimensions 
        self.n_H = int(((n_H_prev-FH)/self.S)+1)
        self.n_W = int(((n_W_prev-FW)/self.S)+1)
        self.n_C = n_C_prev
        
        
    def forward(self, X):    
        # X dimensions are (m,h,w,c)
        
        if self.mode == "max":
            # pool = np.max(X_col, axis=1)
            self.n_X = X.shape[0]
            X_reshaped = X.reshape(X.shape[0]*X.shape[1],1,X.shape[2],X.shape[3])
    
            self.X_col = im2col_indices(X_reshaped, self.FH, self.FW, 0, self.S)
            
            self.max_indexes = np.argmax(self.X_col,axis=0)
            out = self.X_col[self.max_indexes,range(self.max_indexes.size)]
    
            out = out.reshape(self.n_H,self.n_W,self.n_X,self.n_C).transpose(2,3,0,1)
            return out, 0
        
        elif self.mode == "average":
            # number of examples
            m, _,_,_ = X.shape
        
            X_col = im2col(X, self.FH, self.FW, self.S, 0)
            X_col = X_col.reshape(self.n_C, X_col.shape[0]//self.n_C, -1)
            pool = np.mean(X_col, axis=1)
        
            # Reshape pool
            pool = np.array(np.hsplit(pool, m))
            pool = pool.reshape(m, self.n_C, self.n_H, self.n_W)
            self.X_shape=X.shape
            return pool, 0
    
    def backward(self, dA, Lambda=0):
        
        
        if self.mode == "max":
            dX_col = np.zeros_like(self.X_col)
            # flatten the gradient
            dout_flat = dA.transpose(2,3,0,1).ravel()
            
            dX_col[self.max_indexes,range(self.max_indexes.size)] = dout_flat
            
            # get the original X_reshaped structure from col2im
            shape = (self.n_X*self.d_X,1,self.h_X,self.w_X)
            dX = col2im_indices(dX_col,shape, self.FH, self.FW, 0, self.S)
            dX = dX.reshape(self.n_X,self.d_X,self.h_X,self.w_X)
            return dX
        
        elif self.mode == "average":
            m, n_C_prev, n_H_prev, n_W_prev = self.X_shape
            dA_flatten = dA.reshape(self.n_C, -1) / (self.FH * self.FW)
            dX_col = np.repeat(dA_flatten, self.FH*self.FW, axis=0)
            dX = col2im(dX_col, self.X_shape, self.FH, self.FW, self.S, 0) 
            # Reshape dX properly.
            dX = dX.reshape(m, -1)
            dX = np.array(np.hsplit(dX, n_C_prev))
            dX = dX.reshape(m, n_C_prev, n_H_prev, n_W_prev)
            return dX
 
    
    def getGrads(self):
        return None
    
    def output_dims(self):
        return self.n_H, self.n_W, self.n_C
    
    def getLayerParams(self):
        LayerParams = self.S, self.n_H, self.n_W, self.n_C, self.FH, self.FW, self.mode
        return "pool_layer", LayerParams

    def setLayerParams(self, LayerParams):
        self.S, self.n_H, self.n_W, self.n_C, self.FH, self.FW, self.mode = LayerParams



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
        return X_padded[:, :,pad:-pad, pad:-pad]
    
    

def get_im2col_indices(x_shape, field_height=3, field_width=3, padding=1, stride=1):
  # First figure out what the size of the output should be
  N, C, H, W = x_shape
  assert (H + 2 * padding - field_height) % stride == 0
  assert (W + 2 * padding - field_height) % stride == 0
  out_height = (H + 2 * padding - field_height) / stride + 1
  out_width = (W + 2 * padding - field_width) / stride + 1

  i0 = np.repeat(np.arange(field_height,dtype='int32'), field_width)
  i0 = np.tile(i0, C)
  i1 = stride * np.repeat(np.arange(out_height,dtype='int32'), out_width)
  j0 = np.tile(np.arange(field_width), field_height * C)
  j1 = stride * np.tile(np.arange(out_width,dtype='int32'), int(out_height))
  i = i0.reshape(-1, 1) + i1.reshape(1, -1)
  j = j0.reshape(-1, 1) + j1.reshape(1, -1)

  k = np.repeat(np.arange(C,dtype='int32'), field_height * field_width).reshape(-1, 1)

  return (k, i, j)

def im2col_indices(x, field_height=3, field_width=3, padding=1, stride=1):
  """ An implementation of im2col based on some fancy indexing """
  # Zero-pad the input
  p = padding
  x_padded = np.pad(x, ((0, 0), (0, 0), (p, p), (p, p)), mode='constant')

  k, i, j = get_im2col_indices(x.shape, field_height, field_width, padding,
                               stride)

  cols = x_padded[:, k, i, j]
  C = x.shape[1]
  cols = cols.transpose(1, 2, 0).reshape(field_height * field_width * C, -1)
  return cols


def col2im_indices(cols, x_shape, field_height=3, field_width=3, padding=1,
                   stride=1):
  """ An implementation of col2im based on fancy indexing and np.add.at """
  N, C, H, W = x_shape
  H_padded, W_padded = H + 2 * padding, W + 2 * padding
  x_padded = np.zeros((N, C, H_padded, W_padded), dtype=cols.dtype)
  k, i, j = get_im2col_indices(x_shape, field_height, field_width, padding,
                               stride)
  cols_reshaped = cols.reshape(C * field_height * field_width, -1, N)
  cols_reshaped = cols_reshaped.transpose(2, 0, 1)
  np.add.at(x_padded, (slice(None), k, i, j), cols_reshaped)
  if padding == 0:
    return x_padded
  return x_padded[:, :, padding:-padding, padding:-padding]




# forward propagation
'''
F = 3
S = 2
input_dims = (4, 4, 3)
maxpool = pool_layer(F, S, "max", input_dims)
avgpool = pool_layer(F, S, 'average', input_dims)

np.random.seed(1)
X = np.random.randn(2, 4, 4, 3).transpose(0,3,1,2)
print("maxpool forward:\n",maxpool.forward(X))
print("avgpool forward:\n",avgpool.forward(X))
'''

# back propagation
'''
F = 2
S = 1
input_dims = (5, 3, 2)
maxpool = pool_layer(F, S, "max", input_dims)
avgpool = pool_layer(F, S, 'average', input_dims)

np.random.seed(1)
X = np.random.randn(5, 5, 3, 2).transpose(0,3,1,2)
A = maxpool.forward(X)
A = avgpool.forward(X)
dA = np.random.randn(5, 4, 2, 2).transpose(0,3,1,2)


dX = maxpool.backward(dA).transpose(0,2,3,1)
print("mode = max")
print('mean of dA = ', np.mean(dA))
print('dX[1,1] = ', dX[1,1])  
print()
dX = avgpool.backward(dA).transpose(0,2,3,1)
print("mode = average")
print('mean of dA = ', np.mean(dA))
print('dX[1,1] = ', dX[1,1])
'''

# storing and loading

'''
par = maxpool.getLayerParams()

maxpool2 = pool_layer()
maxpool2.setLayerParams(par)
A = maxpool2.forward(X)

dX = maxpool2.backward(dA)
print("mode = max")
print('mean of dA = ', np.mean(dA))
print('dX[1,1] = ', dX[1,1])  
print()
'''

