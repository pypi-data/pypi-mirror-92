import numpy as np
import os
import shutil
import gzip
import urllib.request
from time import sleep
import idx2numpy
from tqdm import tqdm
import easyDL

def load_data():
    """
    Loads mnist dataset.
    """
    names = ['trainX', 'trainY', 'testX', 'testY']
    data = []
    path = easyDL.__file__.split('__init__')[0] + 'preprocessing/datasets/__datasets__/mnist/'
    if not os.path.isdir(path):
        print('downloading...')
        os.mkdir(path)
        urls = ['http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',
                'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',
                'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',
                'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz']
        sleep(0.5)
        for i, _ in enumerate(urls):
            download_url(urls[i], path + names[i] + '.gz')
            with gzip.open(path + names[i] + '.gz', 'rb') as f_in:
                with open(path + names[i]  + '.idx', 'wb') as f_out:
                    shutil.copyfileobj(f_in,f_out)
            data.append(idx2numpy.convert_from_file(path + names[i] + '.idx'))
            os.remove(path + names[i] + '.gz')
        print('\nAll Done.')
    else:
        for name in names:
            data.append(idx2numpy.convert_from_file(path + name + '.idx'))
    
    trainX = data[0].reshape(-1, 28, 28, 1).astype(np.int32)
    testX = data[2].reshape(-1, 28, 28, 1).astype(np.int32)
    trainY = data[1].astype(np.int32)
    testY = data[3].astype(np.int32)
    
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
