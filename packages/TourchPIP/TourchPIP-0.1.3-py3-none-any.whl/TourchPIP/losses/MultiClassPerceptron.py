
from ..forward import Sigmoid,ReLU,Tanh,Linear,Identity 
import numpy as np

class MultiClassPerceptron:

    def __init__(self , y_out , y_true ):

        self.y_true= y_true-1
        self.y_out=y_out

        self.grads={}


    def loss(self):

        sample_loss=0
        
        last_layer=len(self.layers_num_arr)
        a_prelast= self._params['A'+ str(last_layer-1)] 
        z=self._params['Z'+ str(last_layer)]
        dW = np.zeros((len(z), len(a_prelast)+1))
        dA_prev = np.zeros((len( z), len(a_prelast)))
        a_prelast= np.append( a_prelast ,1).T
        w=self._params['W'+ str(last_layer)] 
        act_fc=self.layer_activations[last_layer]
        dl_dz=(np.zeros(len(z))).reshape(len(z) , 1)

        label=self.y_true

        if act_fc == Sign or act_fc == Identity or act_fc == None:

            m = max(z)
            max_indexes=[i for i, j in enumerate(z) if j == m]

            if label not in max_indexes:
                for i in max_indexes:
                    dW[i] = a_prelast 
                    dA_prev[i] = w[i]
                    dl_dz[i] = 1
        
                dW[label] = -a_prelast
                dA_prev[label] = w[label]
                dl_dz[label] = -1
                sample_loss = m - z[label]

            dl_db=dW[:,-1]
            dl_db=dl_db.reshape(len( z),1)

        
            self.grads['dW'+str(last_layer)] = dW[:,:-1]
            self.grads['db'+str(last_layer)] =dl_db
            self.grads['dA'+str(last_layer)] = (np.dot(dA_prev.T , dl_dz)).reshape(len(a_prelast)-1 ,1)


       
    

        else:
            m = max( self.y_out)
            max_indexes=[i for i, j in enumerate( self.y_out) if j == m]

            if label not in max_indexes:
                for i in max_indexes:
                    dl_dz[i] =act_fc.backwards( self.y_out[i]) 
                    dW[i] =  a_prelast * dl_dz[i]
                    dA_prev[i] = w[i]
                
                dl_dz[label] = -act_fc.backwards( self.y_out[label]) 

                dW[label] =  a_prelast * dl_dz[label]
                dA_prev[label] = w[label]     
                
                sample_loss = m -  self.y_out[label]
                
            dl_db=dW[:,-1]
            dl_db=dl_db.reshape(len( z),1)

        
            self.grads['dW'+str(last_layer)] = dW[:,:-1]
            self.grads['db'+str(last_layer)] =dl_db
            self.grads['dA'+str(last_layer)] = (np.dot(dA_prev.T , dl_dz)).reshape(len(a_prelast)-1 ,1)



        
        return sample_loss 


