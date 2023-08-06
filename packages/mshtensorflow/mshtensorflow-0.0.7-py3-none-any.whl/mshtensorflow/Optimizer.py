import numpy as np
class optimizer:
    
     
    def __init__(self,optimizer,learningRate=0.01,beta1=0.9,beta2=0.999):
        self.OPTIMIZER=optimizer
        self.lr=learningRate
        self.beta1=beta1
        self.beta2=beta2
        self.t=1
        self.v={}
        self.s={}
        self.v_corrected={}
        self.s_corrected={}
        self.epsilon=1e-8
        
    
    
    
    def step(self,layers):
        
        
        i=0
        
        for layer in layers:
            grads = layer.getGrads()
            
            if(grads is not None):
            
                params=layer.getParams()
            
                w,b=params
                dw,db=grads
                
                #MOMENTUM GRADIENT DESCENT
                if(self.OPTIMIZER== "gd"):
                    
                    v=self.v
                    v["dW"+str(i+1)]=self.beta1 * v.get("dW"+str(i+1),0)+(1-self.beta1)*dw
                    v["db"+str(i+1)]=self.beta1 * v.get("db"+str(i+1),0)+(1-self.beta1)*db
                    
                    w=w-self.lr * v["dW"+str(i+1)]
                    b=b-self.lr * v["db"+str(i+1)]
                    
                    self.v=v
                    
                
                
                #ADAM OPTIMIZER
                
                if(self.OPTIMIZER== "adam"):
                    
                    v=self.v
                    v_corrected=self.v_corrected
                    s=self.s
                    s_corrected=self.s_corrected
            
                    v["dW"+str(i+1)]=self.beta1*v.get("dW"+str(i+1),0)+(1-self.beta1)*dw
                    v["db"+str(i+1)]=self.beta1*v.get("db"+str(i+1),0)+(1-self.beta1)*db
                    
                    v_corrected["dW"+str(i+1)]=v["dW"+str(i+1)]/(1-np.power(self.beta1,self.t))
                    v_corrected["db"+str(i+1)]=v["db"+str(i+1)]/(1-np.power(self.beta1,self.t))
                    
                    s["dW"+str(i+1)]=self.beta2*s.get("dW"+str(i+1),0)+(1-self.beta2)*np.power(dw,2)
                    s["db"+str(i+1)]=self.beta2*s.get("db"+str(i+1),0)+(1-self.beta2)*np.power(db,2)
                    
                    s_corrected["dW"+str(i+1)]=s["dW"+str(i+1)]/(1-np.power(self.beta2,self.t))
                    s_corrected["db"+str(i+1)]=s["db"+str(i+1)]/(1-np.power(self.beta2,self.t))
                    
                    w=w-self.lr*v_corrected["dW"+str(i+1)]/np.sqrt(s_corrected["dW"+str(i+1)]+self.epsilon)
                    b=b-self.lr*v_corrected["db"+str(i+1)]/np.sqrt(s_corrected["db"+str(i+1)]+self.epsilon)
                    
                    self.s=s
                    self.v=v
                    self.v_corrected=v_corrected
                    self.s_corrected=s_corrected
                    self.t+=1
                
            
                i=i+1
                
                #storing the new parameters in layer
                layer.setParams(w,b)
               
                
            
                
