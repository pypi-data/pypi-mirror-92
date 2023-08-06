import numpy as np
from .Layers import Layer_Dense

class Sigmoid:
    def forwards(self, inputs):
        X = inputs.out
        sig =   1 / (1 + (np.exp(-1 * X)))
        inputs.pass_act('Sigmoid',sig)
        return sig
    @staticmethod
    def sigmoid_(inputs):
        return 1 / (1 + (np.exp(-inputs)))
    @staticmethod    
    def sigmoidBW_(inputs):
        return Sigmoid.sigmoid_(inputs) * (1-Sigmoid.sigmoid_(inputs))    

    def backwards(self, inputs):
        s = self.forwards(inputs)
        return s * (1 - s)

class ReLU:

    def forwards(self, inputs):
        rel = np.maximum(0, inputs.out)
        inputs.pass_act('relu',rel)
        return rel
    @staticmethod     
    def ReLU_(inputs):
        return np.maximum(0, inputs)    
    @staticmethod
    def ReLUBW_(inputs):
        dZ = np.where(inputs > 0,1,inputs)
        dZ = np.where(dZ <= 0 ,0,dZ)
        return dZ
    def Backwards(self, inputs):
         if inputs > 0:
             return 1
         elif inputs <= 0:
             return 0

class Identity:
    def forwards(self, inputs):
        ident =inputs.out
        inputs.pass_act('identity',ident)
        return ident

    def backwards(self, inputs):
        pass

class Tanh:
    def forwards(self, inputs):
        tan = np.tanh(inputs.out)
        inputs.pass_act('tanh',tan)
        return tan
    @staticmethod
    def Tanh_(inputs):
        return np.tanh(inputs)
    @staticmethod 
    def TanhBW_(inputs):
        return (1 - Tanh.Tanh_(inputs)**2)

    def backwards(self, inputs):
        a = self.forwards(inputs)
        return 1 - a ** 2


class Softmax:
    @staticmethod
    def Softmax_(inputs):
        f = np.exp(inputs - np.max(inputs))  # shift values
        return f / f.sum()

    @staticmethod   
    def SoftmaxBW_(prediction,label):
        dy_dz=np.zeros_like(prediction)

        for i in range (label.shape[1]):
            ind=label[0,i]

            dy_dz[:,i]=prediction[:, i]*-prediction[ind, i]

            dy_dz[ind,i]+= prediction[ind, i]


        return   dy_dz 
