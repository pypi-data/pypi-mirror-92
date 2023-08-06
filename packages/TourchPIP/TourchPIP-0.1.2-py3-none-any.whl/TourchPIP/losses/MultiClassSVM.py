# import numpy as np

# class multi_class_SVM:


#     @staticmethod
#     def _Cost(prediction,label):

#         lossval=0

#         for i in range(label.shape[1]):

#             ind=label[0,i]

#             y_label=prediction[ind][i]
            
#             for j in range(prediction.shape[0]):

#                 if max(1+prediction[j][i]-y_label , 0) and j!= ind:

#                     lossval+=1+prediction[j][i]-y_label

#         m = label.shape[1] # datasize 
#         cost = lossval/m

#         return cost

        

          

    
    
#     @staticmethod
#     def _Grad(prediction,label) :
        
        
#         dl_dy=np.zeros_like(prediction)

#         for i in range (label.shape[1]):
#             ind=label[0,i]

#             y_label=prediction[ind][i]

#             count = 0
            
#             for j in range(prediction.shape[0]):

#                 if max(1+prediction[j][i]-y_label , 0) and j!= ind:

#                     count+=1
#                     dl_dy[j][i]=1
                    

#             if count>0:

#                 dl_dy[ind][i]=-count

    
        
#         return  dl_dy

    
    
   
