import numpy as np 
from ..forward import Layer_Dense#,_params,layers_num_arr,layer_activations
from ..forward import ReLU,Sigmoid,Tanh,Softmax,Identity
from ..losses import SoftmaxCrossEntropy
from ..optimizations import Momentum,Adam


class Backward:  # make inheratnce to loss, and layers 
    def __init__(self,Y,learning_rate,LossDerivative):
        # self.AL = AL
        self.Y = Y
        self.grads = {} #grads 
        self.parameters = dict(Layer_Dense._params) #Layer_Dense._params #parameters 
        self.layers_num_arr  = list(Layer_Dense.layers_num_arr)
        self.layer_activations = dict(Layer_Dense.layer_activations)
        self.learning_rate = learning_rate
        self.LossDerivative = LossDerivative
        self.caches = { i: (self.parameters['A'+str(i)],self.parameters['W'+str(i)],self.parameters['b'+str(i)]) if i != 0 else 
                                (self.parameters['A'+str(i)],'_') for i in range(0,int(((len(self.parameters.keys())-1)/3)+1))}
    def _L_model_backward(self):# caches):

        L = len(self.layers_num_arr) # the number of layers
        m = self.caches[L][0].shape[1] 

        self.Y = self.Y.reshape(self.caches[L][0].shape)
        # Initializing the backpropagation
        dAL = self.LossDerivative # loss dervatie (dl/dy)
        self.grads['dA'+str(L)] = dAL
        current_cache = (self.caches[L-1][0],self.caches[L][1],self.caches[L][2]) 
        self.grads["dA" + str(L-1)], self.grads["dW" + str(L)], self.grads["db" + str(L)] = self._LinearActivaionBW(dAL,
                                    L,linear_cache=current_cache,activation=self.layer_activations[L])
        for l in reversed(range(1,L)):

            current_cache = (self.caches[l-1][0],self.caches[l][1],self.caches[l][2])#self.caches[l]

            dA_prev_temp, dW_temp, db_temp =  self._LinearActivaionBW(self.grads['dA'+str(l)],
                                    l,linear_cache=current_cache,activation=self.layer_activations[l])
            self.grads["dA" + str(l-1)] = dA_prev_temp
            self.grads["dW" + str(l)] = dW_temp
            self.grads["db" + str(l)] = db_temp

    def backward(self): # user call it 
        self._L_model_backward()
        return self._update_parameters(), self.grads
    

    def _LinearActivaionBW(self,dAL,l,linear_cache,activation='ReLU'):
        dZ = self._bacwardActivations(dAL,l=l,activation=activation) # (1,1)dz2
        dA_prev, dW, db = self._linear_backward(dZ,linear_cache)# da1,dw2,db2
        return dA_prev,dW,db

    def _bacwardActivations(self,dAL,l,activation='Relu'):        
        if activation == 'Relu':
            self.grads['dZ'+str(l)] = ReLU.ReLUBW_(dAL)  
        elif activation == 'Sigmoid':
            self.grads['dZ'+str(l)] = Sigmoid.sigmoidBW_(dAL)
            return self.grads['dZ'+str(l)]
        elif activation == 'Tanh':
            self.grads['dZ'+str(l)] = Tanh.TanhBW_(dAL)

    def _linear_backward(self,dZ, cache):        
        A_prev, W, b = cache
        m = A_prev.shape[1]
        dW = (1/m) * np.matmul(dZ,A_prev.T) # dz2 (1,1) * a1 (3*1)
        db = (1/m) * np.sum(dZ,axis=1,keepdims=True)

        dA_prev = np.matmul(W.T,dZ) # da1 = w2.t(3,1) . dz2(1,1) 
        assert (dA_prev.shape == A_prev.shape)
        assert (dW.shape == W.shape)
        assert (db.shape == b.shape)        
        return dA_prev, dW, db

    def _update_parameters(self):
               
        L = len(self.layers_num_arr) // 2 # number of layers in the neural network
        # Update rule for each parameter. Use a for loop.
        for l in range(L):
            self.parameters["W" + str(l+1)] =  self.parameters["W" + str(l+1)] - self.learning_rate * self.grads['dW'+str(l+1)]
            self.parameters["b" + str(l+1)] = self.parameters["b" + str(l+1)] - self.learning_rate * self.grads['db'+str(l+1)]
        return self.parameters  


    ################################################################
    ####################     Static Methods     ####################
    ################################################################
    @staticmethod
    def _L_Backward(layers_num_arr,parameters,Y,LossDerivative,layer_activations):# caches):   

        caches = { i: (parameters['A'+str(i)],parameters['W'+str(i)],parameters['Z'+str(i)],parameters['b'+str(i)]) if i != 0 else 
                                (parameters['A'+str(i)],'_') for i in range(0,layers_num_arr+1)}     
        L = layers_num_arr # the number of layers 
        m = caches[L][0].shape[1]  
        grads = dict()
        # Initializing the backpropagation
        if layer_activations[L-1]  != 'SoftMax':
            dAL = LossDerivative  
            grads['dA'+str(L)] = dAL 
            current_cache = (caches[L-1][0],caches[L][1],caches[L][2]) 
            grads["dA" + str(L-1)], grads["dW" + str(L)],grads["db" + str(L)] = Backward._StaticLinearActivaionBW(dAL,
                                            L,parameter=parameters,Y=Y,linear_cache=current_cache,activation=layer_activations[L-1],grads=grads)
        else: 
            dZ = SoftmaxCrossEntropy._Grad(caches[L][0],Y)#.sum(axis=1,keepdims=True)      # dl/dy * dy/dz
            current_cache = (caches[L-1][0],caches[L][1],caches[L][2])
            grads["dA" + str(L-1)], grads["dW" + str(L)],grads["db" + str(L)] = Backward._StaticLinearBW(dZ,current_cache)


        for l in reversed(range(L-1)):
            current_cache = (caches[l][0],caches[l+1][1],caches[l+1][2])

            dA_prev_temp, dW_temp, db_temp = Backward._StaticLinearActivaionBW(grads['dA'+str(l+1)],
                                    l+1,Y=Y,linear_cache=current_cache,parameter=parameters,activation=layer_activations[l],grads=grads)
            grads["dA" + str(l)] = dA_prev_temp
            grads["dW" + str(l+1)] = dW_temp
            grads["db" + str(l+1)] = db_temp

        return grads  
    @staticmethod
    def StaticBW(parameters,learning_rate,LossDerivative,Y,layersLen,layer_activations): # user call it 
        grads = Backward._L_Backward(layers_num_arr=layersLen,parameters=parameters,Y=Y,LossDerivative=LossDerivative,layer_activations=layer_activations)
        return grads
        
    @staticmethod
    def _StaticLinearActivaionBW(dAL,l,linear_cache,parameter,Y,activation='',grads=''):
        dZ = Backward._StaticBWActivations(parameter=parameter,Y=Y,l=l,activation=activation,grads=grads) # (1,1)dz2
        dZL  = Backward._multiply(dAL,dZ) # multiply 
        dA_prev, dW, db = Backward._StaticLinearBW(dZL,linear_cache)# da1,dw2,db2
        return dA_prev,dW,db
    @staticmethod
    def _StaticBWActivations(l,parameter,activation='ReLU',grads='',Y=0):  
        if activation == 'ReLU':
            grads['dZ'+str(l)] = ReLU.ReLUBW_(parameter['Z'+str(l)]) 
            return grads['dZ'+str(l)]
        elif activation == 'Sigmoid':
            grads['dZ'+str(l)] = Sigmoid.sigmoidBW_(parameter['Z'+str(l)]) 
            return grads['dZ'+str(l)]
        elif activation == 'Tanh':
            grads['dZ'+str(l)] = Tanh.TanhBW_(parameter['Z'+str(l)])
            return grads['dZ'+str(l)]
        elif activation == 'SoftMax':
            grads['dZ'+str(l)] = Softmax.SoftmaxBW_(parameter['A'+str(l)],Y)
            return grads['dZ'+str(l)]
    @staticmethod 
    def _multiply(A,Z):
        return A * Z
    @staticmethod
    def _StaticLinearBW(dZ,cache):
        A_prev, W, b = cache
        m = A_prev.shape[1]
        dW =  np.matmul(dZ,A_prev.T) 
        db =  np.sum(dZ,axis=1,keepdims=True)
        dA_prev = np.matmul(W.T,dZ)  
        assert (dA_prev.shape == A_prev.shape)
        assert (dW.shape == W.shape)        
        return dA_prev, dW, db
