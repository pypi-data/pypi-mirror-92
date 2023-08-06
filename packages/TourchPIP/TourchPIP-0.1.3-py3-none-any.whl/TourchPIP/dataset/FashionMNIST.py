import os
import zipfile, urllib.request, shutil
import requests
import matplotlib.pyplot as plt


MNIST_URL = 'https://drive.google.com/uc?id=1NjvEw9Ob7sJkEQLWPe_M-XhhZLYCx7lE&export=download'


class FashionMNIST:
    def __init__(self,path,download=True,train=True):
        self.path = path
        self.download = download
        self.train = train
        if self.download:
            self._Download()
         
        self.TrainFile = os.getcwd() + '/' + self.path + '/mnist_train.csv'
        self.TestFile = os.getcwd() + '/' + self.path + '/mnist_test.csv'

    def _Download(self):
        if not os.path.exists(os.getcwd() + '/' + self.path):
            os.mkdir(self.path)
        file_name = 'MNIST.zip'
        with urllib.request.urlopen(MNIST_URL) as response, open(os.getcwd() + '/' + self.path + '/' + file_name,
                                                                 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            with zipfile.ZipFile(os.getcwd() + '/' + self.path + '/' + file_name) as zf:
                zf.extractall(os.getcwd() + '/' + self.path + '/')

    def __repr__(self):
        return self.TrainFile if self.train == True else self.TestFile
    def plot(self,image):
        plt.imshow(image.reshape(28,28))
        plt.show()    