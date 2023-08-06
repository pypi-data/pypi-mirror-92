import numpy as np

class Momentum:
    def __init__(self,paramterts,lr=0.1,beta=0.9):
        self.params = paramterts
        self.lr = lr
        self.beta = beta 
        self.v = {}
    @staticmethod 
    def initialize_velocity(parameter,layerlen):
        L = layerlen 
        v = {}
        for l in range(L):
            v['dW'+str(l+1)] = np.zeros(parameter['W'+str(l+1)].shape) 
            v['db'+str(l+1)] = np.zeros(parameter['b'+str(l+1)].shape)
        return v
    @staticmethod    
    def update(layerlen,v,parameter,lr,beta=0.9):
        L = layerlen  
        for l in range(L):
            v["dW" + str(l+1)] = (beta*v["dW" + str(l+1)]) + ((1-beta)*parameter['W'+str(l+1)])
            v["db" + str(l+1)] = (beta*v["db" + str(l+1)]) + ((1-beta)*parameter['b'+str(l+1)])
            parameter["W" + str(l+1)] = parameter["W" + str(l+1)] - (lr*v["dW" + str(l+1)])
            parameter["b" + str(l+1)] = parameter["b" + str(l+1)] - (lr*v["db" + str(l+1)])
        return parameter
    def __repr__(self):
        self.initialize_velocity()
        self.update()
        return {'velocity':self.v,
                    'parameters':self.params}    

                
