import pandas
import numpy as np
import math
import pandas
import random

class DataLoaderIterator:
    def __init__(self,dataloader):
        self.dataloader = dataloader
        self.index = 0
    def __next__(self):
        if self.index < self.dataloader.iternums:
            result = self.dataloader.__next__() 
            self.index +=1
            return result[0],result[1] 
        self.dataloader.current_position = 0    
        raise StopIteration
        
class DataLoader:
    def __init__(self,path='',batchsize=20,shuffling=True, normalization={}):
        """
        initializing the params
        @params: path
                batchsize      ---> number of raws loaded from csv
                shuffling      ---> shuffle raws indexs
                nomaliztion    ---> normalize between 0-1

        @return: 1) features raws
                2) labels raws
        """
        self.path = str(path)
        self.current_position = 0
        self.batchsize = batchsize
        self.shuffling = shuffling
        self.normalization = normalization['Transform'] if type(normalization['Transform']) == bool else RuntimeError('should be bool value ') 
        fileObject = open(self.path)
        self.row_count = sum(1 for row in fileObject) 
        self.iternums = math.ceil((self.row_count-1) / batchsize) - 5

    def __iter__(self):
           return DataLoaderIterator(self) 
    def __next__(self):
            df = pandas.read_csv(self.path, skiprows=self.current_position,nrows=self.batchsize)  
            self.current_position += self.batchsize

            if self.normalization == False:             #if No normalization

                if not self.shuffling:                  #if No shuffling
                    return df.iloc[:, 1:].to_numpy(), df.iloc[:, 0].to_numpy().reshape(-1,1)

                else:                                   #if shuffling
                    x = df.iloc[:, 1:].to_numpy()
                    y = df.iloc[:, 0].to_numpy()
                    np.random.shuffle(x)
                    np.random.shuffle(y)
                    return x , y.reshape(-1,1)
                
            else:                                       #if normalization
                if not self.shuffling:                  #if No shuffling
                    x = df.iloc[:, 1:].to_numpy()
                    norm_x = (x - np.min(x))/np.ptp(x)
                    return norm_x , df.iloc[:, 0].to_numpy().reshape(-1,1)

                else:                                   #if shuffling
                    x = df.iloc[:, 1:].to_numpy()
                    norm_x = (x - np.min(x))/np.ptp(x)
                    y = df.iloc[:, 0].to_numpy()
                    np.random.shuffle(norm_x)
                    np.random.shuffle(y)
                    return norm_x , y.reshape(-1,1)
    def load(self,normalize=False):
        if normalize:
            df = pandas.read_csv(self.path, skiprows=random.randint(0, self.row_count - self.batchsize -2),nrows=self.batchsize)
            x = df.iloc[:, 1:].to_numpy()
            norm_x = (x - np.min(x))/np.ptp(x)
            return norm_x , df.iloc[:, 0].to_numpy().reshape(-1,1)

        else:
            df = pandas.read_csv(self.path, skiprows=random.randint(0, self.row_count - self.batchsize -2),nrows=self.batchsize)
            return df.iloc[:, 1:].to_numpy(), df.iloc[:, 0].to_numpy().reshape(-1,1)

    

