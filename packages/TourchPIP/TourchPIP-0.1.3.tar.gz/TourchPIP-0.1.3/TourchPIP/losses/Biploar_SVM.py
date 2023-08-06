import numpy as np
from ..forward import Layer_Dense
from ..forward import Sigmoid,ReLU,Tanh,Identity


class Biploar_SVM(Layer_Dense) :
    def __init__(self,pred,lable):
        self.pred = pred
        self.lable = lable
        self.parameters = Layer_Dense._params #parameter
        self.dl={}
   
    def loss(self):
        return max(0,1-(self.lable*self.parameters['Z'+str(len(Layer_Dense.layer_activations.keys()))]))
        
    def grad(self):
        L = len(Layer_Dense.layer_activations.keys())
        act_fc=Layer_Dense.layer_activations[L]
   
        if (self.lable*self.parameters['Z'+str(L)] )> 1:
                self.dl['dW'+str(L)] = np.zeros(self.parameters['W'+str(L)].shape)
                self.dl['db'+str(L)] = np.zeros(self.parameters['b'+str(L)].shape)
                self.dl['dA'+str(L)] = np.zeros(self.parameters['A'+str(L)].shape)
        else :
            dl_activation=[]
            if act_fc == 'sigmoid':
               sig_inst=Sigmoid()
               dl_activation = sig_inst.backwards(self.parameters['Z'+str(L)]) 
  
            elif act_fc == 'relu':
                relu_inst =ReLU()
                dl_activation= relu_inst.Backwards(self.parameters['Z'+str(L)])
            elif act_fc == 'tanh':
                tanh_inst = Tanh()
                dl_activation= tanh_inst.backwards(self.parameters['Z'+str(L)])
            dl_dz = np.matmul(-self.lable,dl_activation)
            self.dl['dW'+str(L)] = np.matmul(self.parameters['W'+str(L)],dl_dz)
            self.dl['db'+str(L)] = dl_dz
           
    @staticmethod
    def _Loss(parameters,label) :  
      lossval = max(0,1-(label*parameters['Z'+str(len(Layer_Dense.layer_activations.keys()))]))
      return lossval
    
    @staticmethod
    def _Cost(prediction,label):
      m = label.shape[1] # datasize 
      cost = (1/m) * np.sum(Biploar_SVM._Loss(prediction,label))
      cost = np.squeeze(cost)
      return cost 

    @staticmethod
    def _Grad(parameters,label) :
        L = len(Layer_Dense.layer_activations.keys())
        dl_dy=[]
        if (label*parameters['Z'+str(L)] )> 1:   
          dl_dy = 0
               
        else :
            dl_dy=-label
           
        return dl_dy

            
            
