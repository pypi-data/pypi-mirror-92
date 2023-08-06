import numpy as np


class SD():
    def __init__(self,pred,lable,learning_rate=0.1):
        self.pred = pred
        self.lable = lable
        self.parameters = 1 #Layer_Dense._params #Layer_Dense._params 
        self.dl={}
        
    def loss(self) :    
      pred_minus_lable = np.subtract(self.pred , self.lable)
      pred_minus_lable_T = pred_minus_lable.T
      return 0.5 * np.dot(pred_minus_lable_T, pred_minus_lable)

    def grad(self) :
      return np.subtract(self.pred , self.lable)


    @staticmethod
    def _Loss(prediction,label) :  
      lossval = 0.5*(prediction-label)**2
      return lossval
    
    @staticmethod
    def _Cost(prediction,label):
      m = label.shape[1] # datasize 
      cost = (1/m) * np.sum(SD._Loss(prediction,label))
      cost = np.squeeze(cost)
      return cost 

    @staticmethod
    def _Grad(prediction,label) :
      return np.subtract(prediction,label)  

    

