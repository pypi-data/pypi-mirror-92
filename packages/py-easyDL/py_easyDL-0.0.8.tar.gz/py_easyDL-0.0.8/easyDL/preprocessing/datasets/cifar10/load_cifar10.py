import tarfile
import _pickle as cPickle
import os
import urllib.request
from time import sleep
from tqdm import tqdm
import numpy as np
import easyDL

def load_data():
    path = easyDL.__file__.split('__init__')[0] + 'preprocessing/datasets/__datasets__/cifar-10/'
    if not os.path.isdir(path):
        print('downloading...')
        os.mkdir(path)
        url='https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
        sleep(0.5)
        download_url(url, path + 'Cifar_10.tar.gz')
        tar = tarfile.open(path + 'Cifar_10.tar.gz')
        tar.extractall(path)
        tar.close()
        os.remove(path + 'Cifar_10.tar.gz')
        batches=[]
        with open(path + 'cifar-10-batches-py/test_batch', 'rb') as f:
            test = cPickle.load(f, encoding='latin1')
        testX = test['data'].reshape(-1, 32, 32, 3)
        testY = np.array(test['labels'])
        for i in range(5):
            with open(path + 'cifar-10-batches-py/data_batch_' + str(i + 1), 'rb') as f:
                batches.append(cPickle.load(f, encoding='latin1'))
        trainX = []
        trainY = []
        for batch in batches:
            trainX.append(batch['data'].reshape(-1, 32, 32, 3))
            trainY.append(np.array(batch['labels']).reshape(-1, 1))
        trainX = np.vstack(trainX)
        trainY = np.squeeze(np.vstack(trainY))
        print('\nAll Done.')
    else:
        batches = []
        with open(path + 'cifar-10-batches-py/test_batch', 'rb') as f:
            test = cPickle.load(f, encoding='latin1')
        testX = test['data'].reshape(-1, 32, 32, 3)
        testY = np.array(test['labels'])
        for i in range(5):
            with open(path + 'cifar-10-batches-py/data_batch_' + str(i + 1), 'rb') as f:
                batches.append(cPickle.load(f, encoding='latin1'))
        trainX = []
        trainY = []
        for batch in batches:
            trainX.append(batch['data'].reshape(-1, 32, 32, 3))
            trainY.append(np.array(batch['labels']).reshape(-1, 1))
        trainX = np.vstack(trainX)
        trainY = np.squeeze(np.vstack(trainY))

    return (trainX, trainY), (testX, testY)

class DownloadProgressBar(tqdm):
    """
    Progress bar.
    """
    def update_to(self, byte=1, bsize=1, tsize=None):
        """
        updating function.
        """
        if tsize is not None:
            self.total = tsize
        self.update(byte * bsize - self.n)


def download_url(url, output_path):
    """
    Download url.
    """
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as prog:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=prog.update_to)
