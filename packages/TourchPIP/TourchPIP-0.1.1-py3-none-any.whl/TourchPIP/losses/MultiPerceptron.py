import numpy as np


class MultiPerceptron:

    @staticmethod
    def _Cost(prediction,label):

        lossval=0

        for i in range (label.shape[1]):

            ind=label[0,i]

            m = max(prediction[:,i])
            max_indexes=[s for s, t in enumerate(prediction[:,i]) if t == m]

            ind= label[0,i]
            
            if ind not in max_indexes:
                

                lossval+=prediction[max_indexes[0]][i]-prediction[ind][i]

        cost = lossval/label.shape[1]

        return cost
                
       

    
    @staticmethod
    def _Grad(prediction,label) :
        
        
        dl_dy=np.zeros_like(prediction)

        for i in range (label.shape[1]):

            m = max(prediction[:,i])
            max_indexes=[s for s, t in enumerate(prediction[:,i]) if t == m]

            ind= label[0,i]
            
            if ind not in max_indexes:
                
                dl_dy[ind][i]=-1

                for j in max_indexes:
                    dl_dy[j][i]=1
        
        
        return dl_dy

    
    
        
    
