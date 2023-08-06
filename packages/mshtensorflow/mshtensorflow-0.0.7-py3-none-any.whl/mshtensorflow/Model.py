import numpy as np
from .Layer import layer
from .conv_layer import conv_layer
from .pool_layer import pool_layer
from .Visualization import visualization
from .Flatten import flatten
from .Dropout import dropout

import time

class model:
    
    def __init__(self, input_dimensions=0):
        self.input_dimensions = input_dimensions 
        self.layers=[]
    
    def input_dims(self, input_dimensions):
        self.input_dimensions = input_dimensions 
    
    def add(self, *argv):
        
        layer_type = argv[0]
        
        if(layer_type=='maxpool'):
            Filter_size, Stride = argv[1:3]
            input_dimensions=self.layers[-1].output_dims() # output dims of previous layer
            l=pool_layer(Filter_size, Stride, "max", input_dimensions)
        
        elif(layer_type=='avgpool'):
            Filter_size, Stride = argv[1:3]
            input_dimensions=self.layers[-1].output_dims() # output dims of previous layer
            l=pool_layer(Filter_size, Stride, "average", input_dimensions)
        
        elif(layer_type=='conv'):
            Filter_size, num_of_filters, Stride, padding, activation_type = argv[1:6]
            if(self.layers == []):
                input_dimensions = self.input_dimensions # output dims of previous layer
            else:
                input_dimensions=self.layers[-1].output_dims() # output dims of previous layer
            
            l=conv_layer(Filter_size, num_of_filters, Stride, padding, activation_type, input_dimensions)
        
        elif(layer_type=='flatten'):
            if(self.layers == []):
                input_dimensions = self.input_dimensions # output dims of previous layer
            else:
                input_dimensions=self.layers[-1].output_dims() # output dims of previous layer
            
            l=flatten(input_dimensions)
        
        elif(layer_type=='dropout'):
            probability = argv[1]
            in_nodes = self.layers[-1].output_dims()
            l=dropout(probability, in_nodes)

        
        else:
            out_nodes = argv[1]
            if(self.layers == []):
                in_nodes = self.input_dimensions
            else:
                in_nodes = self.layers[-1].output_dims() # output dims of previous layer
            l=layer(in_nodes, out_nodes, layer_type)
        
        self.layers.append(l)

    def Initialize_Parameters(self):        
        for Layer in self.layers:
            w,b=Layer.getParams()
            w= np.random.randn(w.shape[0],w.shape[1]) * 0.01
            b = np.zeros(b.shape)
            Layer.setParams(w, b)

    def create_mini_batches(self, X, y, batch_size): 
        mini_batches = [] 
        if(len(X.shape) == 2): # fully connected
            n_minibatches = X.shape[1] // batch_size 
            y = y[:,:X.shape[1]] # trim y as x
            for i in range(n_minibatches + 1): 
                X_mini = X[:, i * batch_size:(i + 1)*batch_size] 
                Y_mini = y[:, i * batch_size:(i + 1)*batch_size]
                mini_batches.append((X_mini, Y_mini)) 
            if(X.shape[1] % batch_size == 0 ):
                mini_batches.pop()
                
        elif(len(X.shape) == 4): # convulution
            n_minibatches = X.shape[0] // batch_size 
            y = y[:,:X.shape[0]] # trim y as x
            for i in range(n_minibatches + 1): 
                X_mini = X[i * batch_size:(i + 1)*batch_size] 
                Y_mini = y[:, i * batch_size:(i + 1)*batch_size]
                mini_batches.append((X_mini, Y_mini)) 
            if(X.shape[0] % batch_size == 0 ):
                mini_batches.pop()
                
        return mini_batches, len(mini_batches)
    
    def fit(self, X, label, batch_size,num_epochs,optimizer,loss_fn):
        loss_history = []
        batches_loss_history = []
        mini_batches, num_of_batches = self.create_mini_batches(X, label, batch_size)
        Lambda=loss_fn.getLambda()
        # T = time.time()
        for epoch in range (num_epochs):
            
            current_batch=0
            epoch_loss = 0
            print('\repoch:{}/{} [{}] {}%'.format(epoch, num_epochs, '.' * (50), 0), end='')
                
            for X, label in mini_batches:
                start_time = time.time()
                current_batch += 1
                A=X
                weights_sum=0
                
                for Layer in self.layers: 
                    A, w_squared = Layer.forward(A)
                    weights_sum += w_squared 
                
                batch_loss = loss_fn.forward(A,label,weights_sum)
                epoch_loss += batch_loss
                batches_loss_history+= [batch_loss]
                grad = loss_fn.backward()
                
                for Layer in self.layers[::-1]:
                    grad = Layer.backward(grad,Lambda) 
                    
                optimizer.step(self.layers)
                done = int(100*current_batch/num_of_batches)
                ETA = int((time.time() - start_time) * (num_of_batches-current_batch))
                print('\repoch:{}/{} [{}{}] {}% ETA:{}'.format(epoch+1, num_epochs,'█' * int(done/2), '.' * int(50-int(done/2)), done, format_time(ETA)), end='')
                # if(time.time()-T > 5):
                #     T=time.time()
                #     visualization(loss_history, batches_loss_history)
            
            loss_history+=[epoch_loss/num_of_batches]
            print("\nLoss of epoch {} = {:.3f}".format(epoch+1,loss_history[-1]))
            visualization(loss_history, batches_loss_history)
        # return loss_history 
        
    def predict(self, X):
        
        if(len(X.shape) == 2): # fully connected
            for Layer in self.layers: 
                X, _ = Layer.forward(X)
            return X
                    
        elif(len(X.shape) == 4): # convulution
            L=[]
            batch_size=32
            mini_batches=[]
            num_of_batches = X.shape[0] // batch_size 
            for i in range(num_of_batches + 1): 
                X_mini = X[i * batch_size:(i + 1)*batch_size] 
                mini_batches.append(X_mini) 
            if(X.shape[0] % batch_size == 0 ):
                mini_batches.pop()
                
            for batch in mini_batches:
                
                X = batch
                for Layer in self.layers: 
                    X, _ = Layer.forward(X)
                L.append(X)
                
            arr = np.hstack(L)
            return arr 
            
    def getParams(self):
        List=[]
        for Layer in self.layers:
            List.append(Layer.getLayerParams())
        return List
    
    def setParams(self, List):
        for LayerType, LayerParams in List:
            if(LayerType == "layer"): Layer = layer()
            elif(LayerType == "conv_layer"): Layer = conv_layer()
            elif(LayerType == "pool_layer"): Layer = pool_layer()
            elif(LayerType=='flatten'): Layer = flatten()
            # elif(LayerType=='batch_norm'): Layer = batch_norm()
            Layer.setLayerParams(LayerParams)
            self.layers.append(Layer)
    
def format_time(time):
    out=''
    if(time>=60):
        minutes = time // 60
        out+=str(minutes)+'m '
    time %= 60
    seconds = time
    out+=str(seconds)+'s\t\t\t'
    return out
    
'''  
m = model()
m.add(2,2,"Relu")
m.add(2,2,"Relu")
m.Initialize_Parameters()
'''
