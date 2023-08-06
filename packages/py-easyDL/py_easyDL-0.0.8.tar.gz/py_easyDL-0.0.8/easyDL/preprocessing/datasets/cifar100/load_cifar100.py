import tarfile
import _pickle as cPickle
import os
import urllib.request
from time import sleep
from tqdm import tqdm
import numpy as np
import easyDL


def load_data(labels_type= 'fine'):
    path = easyDL.__file__.split('__init__')[0] + 'preprocessing/datasets/__datasets__/cifar-100/'
    if not os.path.isdir(path):
        print('downloading...')
        os.mkdir(path)
        url='https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz'
        sleep(0.5)
        download_url(url, path + 'Cifar_100.tar.gz')
        tar = tarfile.open(path + 'Cifar_100.tar.gz')
        tar.extractall(path)
        tar.close()
        os.remove(path + 'Cifar_100.tar.gz')
        with open(path + 'cifar-100-python/test', 'rb') as f:
            test = cPickle.load(f, encoding='latin1')
        with open(path + 'cifar-100-python/train', 'rb') as f:
            train = cPickle.load(f, encoding='latin1')
        trainX = train['data'].reshape(-1, 32, 32, 3)
        testX = test['data'].reshape(-1, 32, 32, 3)
        if labels_type == 'fine':    
            trainY = np.array(train['fine_labels'])
            testY = np.array(test['fine_labels'])
        else:
            trainY = np.array(train['coarse_labels'])
            testY = np.array(test['coarse_labels'])
        print('\nAll Done.')
    else:
        with open(path + 'cifar-100-python/test', 'rb') as f:
            test = cPickle.load(f, encoding='latin1')
        with open(path + 'cifar-100-python/train', 'rb') as f:
            train = cPickle.load(f, encoding='latin1')
        trainX = train['data'].reshape(-1, 32, 32, 3)
        testX = test['data'].reshape(-1, 32, 32, 3)
        if labels_type == 'fine':    
            trainY = np.array(train['fine_labels'])
            testY = np.array(test['fine_labels'])
        else:
            trainY = np.array(train['coarse_labels'])
            testY = np.array(test['coarse_labels'])

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
