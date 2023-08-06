import numpy as np 
class loss_Function():
    def __init__(self,loss_type):
        self.loss_type=loss_type
        self.Lambda=0
        #self.pred
        #self.labels
        
    def log(self, X): #replace log(0)=-9999999 instead of -inf
        with np.errstate(divide='ignore'):
            res = np.log(X)
        res[np.isneginf(res)]=-9999999
        return res
    
    def getLambda(self):
        return self.Lambda
    def setLambda(self,Lambda):
        self.Lambda= Lambda

    
    def forward(self,pred,labels,weights_sum):
        self.m=labels.shape[1]
        self.pred=pred
        self.labels=labels
        self.weights_sum=weights_sum
        self.regularization_cost=((self.Lambda)/(2*self.m))*(self.weights_sum)
        
        if self.loss_type=="LOG":
            return (((1/self.m)*np.sum(-self.log(np.absolute((labels/2)-0.5+pred))))+self.regularization_cost)
        
        elif self.loss_type=="MEAN":
            return ((np.sum(np.power(pred-labels,2))/(2*self.m))+self.regularization_cost)
        
        elif self.loss_type=="CROSSENTROPY":
            return (((-1/self.m)*np.sum(np.multiply(labels, self.log(pred))+np.multiply(1-labels, self.log(1-pred))))+self.regularization_cost)

        elif self.loss_type=="SoftmaxCrossEntropy":
            exp = np.exp(pred) # exp of all output nodes
            sums = np.sum(exp, axis=0) # sum of exponentials of each example
            softmax = exp/sums # softmax output for all nodes
            self.softmax = softmax # cache softmax
            L = -1*self.log(softmax[labels==1]) # individual losses for each example
            return (((1/self.m)*np.sum(L))+self.regularization_cost)


    def backward(self):
        if self.loss_type=="LOG":
            return (((-1/self.pred)*((1+self.labels)/2)) + ((1/(1-self.pred))*((1-self.labels)/2)))
        
        elif self.loss_type=="MEAN":
            return (self.pred-self.labels)
        
        elif self.loss_type=="CROSSENTROPY":
            return ((-self.labels/self.pred)+(1-self.labels/1-self.pred))
        
        elif self.loss_type=="SoftmaxCrossEntropy":
            return (self.softmax - self.labels)
        
        
        
#lossfn=Loss_Functions('MEAN') 
#pred=np.array([[1,1,1]])  
#labels=np.array([[1,1,-1]]) 

#loss=lossfn.forward(pred, labels)  
#grad=lossfn.backward()  
#print(loss)
#print(grad)


        
