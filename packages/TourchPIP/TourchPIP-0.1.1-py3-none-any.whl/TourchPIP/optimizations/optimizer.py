from . import Momentum , Adam

class Optimizer:
    def __init__(self,parameters,optimiType={'GD':True},LayersLen=0,grads=[],lr=0):
        self.optimiType = optimiType
        self.grads = grads 
        self.lr = lr
        self.LayersLen = LayersLen
        self.parameters = parameters

    def normalGD(self):
        L = self.LayersLen  # number of layers in the neural network
        # Update rule for each parameter. Use a for loop.
        for l in range(L):
            self.parameters["W" + str(l+1)] = self.parameters["W" + str(l+1)] - self.lr * self.grads['dW'+str(l+1)]
            self.parameters["b" + str(l+1)] = self.parameters["b" + str(l+1)] - self.lr * self.grads['db'+str(l+1)]
        return self.parameters     
        
    def optimize(self):
            if 'GD' in self.optimiType and self.optimiType['GD']:
                return self.normalGD() # return new paramters 
            elif 'Adam' in self.optimiType and self.optimiType['Adam']:
                v,s = Adam.initialize_adam(parameters=self.parameters,layerlen=self.LayersLen)
                return Adam.update_parameters(layerlen=self.LayersLen,v=v,s=s,grads=self.grads,parameters=self.parameters,learning_rate=self.lr)
            elif 'Momeuntum' in self.optimiType and self.optimiType['Momeuntum']:
                v = Momentum.initialize_velocity(parameter=self.parameters,layerlen=self.LayersLen)
                return Momentum.update(layerlen=self.LayersLen,v=v,parameter=self.parameters,lr=self.lr)