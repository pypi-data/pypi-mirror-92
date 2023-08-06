from .Linear import Linear
from . import Sigmoid
from . import ReLU,Sigmoid,Tanh,Softmax,Identity,Softmax
from itertools import repeat
from ..losses import SD#, Biploar_SVM ,BiploarPerceptron
from ..backward import Backward
import numpy as np
from ..losses import SoftmaxCrossEntropy
from ..optimizations import Optimizer


def _tupleDivide(tup):
    layersShape =  list()    
    for i in range(len(tup)-1):
        _tup = (tup[i],tup[i+1])
        layersShape.append(_tup)
    return layersShape

class NetWork:
    def __init__(self,LayersShape,activations,optimType={'GD':True}):
        self.LayersShape = LayersShape
        self.createdLayers = [Linear(layer[0],layer[1],l_size=layer[0]) for layer in _tupleDivide(LayersShape)]
        self.activations = list(repeat(activations, len(self.createdLayers))) if type(activations) == str \
                                                else activations 

        self.LayersLen = len(self.createdLayers) 
        self.parameters = dict()
        self.Zout = list()
        self.Aout = list()
        self.lossvalues = []
        self.optimType  = optimType 

    def fit(self,X,Y,learning_rate=0.1):
        ########## Forward L Step        
        self._CalcFWD(X)
        self._ConstructParams() 

        ############## Lossess
        # cost = SD._Loss(self.Aout[self.LayersLen-1],Y)
        # cost = SD._Cost(self.Aout[self.LayersLen-1],Y)
        cost = SoftmaxCrossEntropy._Cost(self.Aout[self.LayersLen-1],Y)
        
        # cost = compute_cost(self.Aout[self.LayersLen-1],Y)
        # loss = lossClass._Loss(self.Aout[self.LayersLen-1],Y)


        # lossD = SD._Grad(self.Aout[self.LayersLen-1],Y)
        # lossD = lossgrad(self.Aout[self.LayersLen-1],Y)
        lossD = SoftmaxCrossEntropy._Grad(self.Aout[self.LayersLen-1],Y.T)
        # Y label 
        # lossD = lossClass._Grad(self.Aout[self.LayersLen-1],Y)
        
        
        ########## backward 
        grads = Backward.StaticBW(self.parameters,learning_rate=learning_rate,LossDerivative=lossD,
                    Y=Y,layersLen=self.LayersLen,layer_activations=self.activations)
        ###########
        
        ######### parameters update
        optimizer = Optimizer(parameters=self.parameters,grads=grads,optimiType=self.optimType,LayersLen=self.LayersLen,lr=learning_rate)
        self.parameters = optimizer.optimize()
        self._UpdateLayerParam()
        ###########################

        self.Aout.clear()
        self.Zout.clear()
        return cost  
    

    def Parameters(self):
        return self.parameters    
    def _updateA_Z(self):
        for i in range(len(self.createdLayers)):
            self.Zout[i] = self.parameters['Z'+str(i+1)]
            self.Aout[i] = self.parameters['A'+str(i+1)]


    def _UpdateLayerParam(self):
        for i in range(self.LayersLen):
            self.createdLayers[i].updateW_B(self.parameters['W'+str(i+1)],self.parameters['b'+str(i+1)])

    def _ConstructParams(self):
        for i in range(self.LayersLen):
            self.parameters['W'+str(i+1)],self.parameters['b'+str(i+1)] = self.createdLayers[i].__reper__()
            self.parameters['Z'+str(i+1)] = self.Zout[i]
            self.parameters['A'+str(i+1)] = self.Aout[i]

    def _CalcFWD(self,X):
        aOut = X
        self.parameters['A0'] = X
        for layer,activation in zip(self.createdLayers,self.activations):
            zOut = layer.forward(aOut)
            self.Zout.append(zOut)
            aOut = NetWork.ActivationCalc(zOut,activation)
            self.Aout.append(aOut) 
    
    def FWD_predict(self,X):
        aOut = X
        for Layer,activation in zip(self.createdLayers,self.activations):
            zOut = Layer.forward(aOut)
            aOut = NetWork.ActivationCalc(zOut,activation)
        return aOut  

    def Prediction(self,X,Y,parameter):
        if  self.LayersShape[-1] > 1:
            return self._MultiPrediction(X,Y,parameter)
        return self._BinaryPrediction(X,Y,parameter)
    # multi classfication       
    def _MultiPrediction(self,X,Y,parameter):
        m = X.shape[1]
        p = list()#np.zeros((1,m))
        probas = self.FWD_predict(X)
        for i in range(0, probas.shape[1]):
            m = max(probas[:,i])
            max_indexes=[s for s, t in enumerate(probas[:,i]) if t == m]
            p.append(max_indexes[0])
        acc = np.sum((p == Y) / m)
    
        return p, acc
    # binay classfication    
    def _BinaryPrediction(self,X,Y,parameter):
        m = X.shape[1]
        n = self.LayersLen # number of layers in the neural network
        p = np.zeros((1,m))
        
        # Forward propagation
        probas = self.FWD_predict(X)
        for i in range(0, probas.shape[1]):
            if probas[0,i] > 0.5:
                p[0,i] = 1
            else:
                p[0,i] = 0
        acc = np.sum((p == Y) / m)
        return p, acc
    @staticmethod
    def ActivationCalc(zOut,activation='ReLU'):
        if activation == 'ReLU':
            return ReLU.ReLU_(zOut)
        elif activation == 'Sigmoid':
            return Sigmoid.sigmoid_(zOut)
        elif activation == 'Tanh':
            return Tanh.Tanh_(zOut) 
        elif activation == 'SoftMax':
            return Softmax.Softmax_(zOut)    

        assert 'No Activation Setted\n'         

    def PlotLoss(self):
        pass   



    def Linear(self,n_inputs, n_neurons, weight_type="random"):
        self.McreatedLayers.append(Linear(n_inputs, n_neurons, weight_type="random"))
        return self.McreatedLayers[0]
        pass
            
   
    def save_model(self,path):
        
        with open(path, 'w') as filehandle:
            filehandle.write('%s\n' % self.LayersLen)               #print number of layers created
            filehandle.write('-'*60)                                #--------------
            for listitem in self.activations:                       #print activations
                filehandle.write('%s\n' % listitem) 
            filehandle.write('-'*60)                                #--------------
            for i in range(self.LayersLen): 
                for listitem in self.parameters['W'+ str(i+1)]:       #print weights
                    filehandle.write('%s\n' % listitem)
                filehandle.write('-'*60)                            #--------------
                for listitem in self.parameters['b'+ str(i+1)]:       #print biases
                    filehandle.write('%s\n' % listitem)
                filehandle.write('-'*60)                            #--------------