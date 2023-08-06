import numpy as np

class SoftmaxCrossEntropy:
    def  __init__ (self):
        pass

    @staticmethod
    def _Cost(prediction,label):
        lossval=0
        for i in range (label.shape[1]):

            ind=label[0,i]
            y_label= prediction[ind][i]
            if y_label != 0:
                lossval+=-np.log(y_label)

        cost = lossval/label.shape[1]

        return cost
       

        
    @staticmethod
    def _Grad(prediction,label) :
        dl_dy=np.zeros_like(prediction)

        for i in range (label.shape[1]):
            ind=label[0,i]

            dl_dy[:,i]=prediction[:, i]

            dl_dy[ind,i]= prediction[ind, i]-1

        return   dl_dy

