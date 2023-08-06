import os
import shutil
import tarfile
import urllib.request
import pandas as pd

CIFAR10_URL = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'


class CIFAR_10:
    def __init__(self, path, download=True, train=True):
        self.path = path
        self.download = download
        self.train = train
        self.csv_list = []
        if self.download:
            self._Download()
        self.path = os.getcwd() + '/' + self.path
        self.toCSV()

        self.TrainFile = self.path + '/' + 'cifar-10-batches-py/train_cifar.csv'
        self.TestFile = self.path + '/' + 'cifar-10-batches-py/test_batch.csv'

    def _Download(self):
        if not os.path.exists(os.getcwd() + '/' + self.path):
            os.mkdir(self.path)
        file_name = 'CIFAR-10.tar.gz'
        with urllib.request.urlopen(CIFAR10_URL) as response, open(os.getcwd() + '/' + self.path + '/' + file_name,
                                                                   'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            tar = tarfile.open(os.getcwd() + '/' + self.path + '/' + file_name, "r:gz")
            tar.extractall(os.getcwd() + '/' + self.path + '/')
            tar.close()

    def unpickle(self, file):
        import pickle
        with open(file, 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        return dict

    def toCSV(self):
        file_names = ['data_batch_1', 'data_batch_2', 'data_batch_3', 'data_batch_4', 'data_batch_5', 'test_batch']
        for name in file_names:
            df_labels = pd.DataFrame(self.unpickle(self.path + '/' + 'cifar-10-batches-py/' + name)[b'labels'])
            df_data = pd.DataFrame(self.unpickle(self.path + '/' + 'cifar-10-batches-py/' + name)[b'data'])
            new = pd.concat([df_labels, df_data], axis=1)
            if not os.path.exists(self.path + '/' + 'cifar-10-batches-py/' + name + '.csv'):
                new.to_csv(self.path + '/' + 'cifar-10-batches-py/' + name + '.csv', index=False)

        for name in file_names[0:5]:
            self.csv_list.append(self.path + '/' + 'cifar-10-batches-py/' + name + '.csv')


        if not os.path.exists(self.path + '/' + 'cifar-10-batches-py/train_cifar.csv'):
            df_from_each_file = (pd.read_csv(f, sep=',', header=None) for f in self.csv_list)
            df_merged = pd.concat(df_from_each_file, ignore_index=True)
            df_merged.to_csv(self.path + '/' + 'cifar-10-batches-py/train_cifar.csv', index=False)

    def __repr__(self):
        return self.TrainFile if self.train == True else self.TestFile



