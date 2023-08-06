import pandas as pd
import numpy as np
import pickle
import os
class dataset:
    def __init__(self, dataset_name, path):
        self.dataset_name = dataset_name
        self.path = path

    def get_dataset(self):
        if self.dataset_name == 'mnist':
            training_set = pd.read_csv(self.path+'/train.csv/mnist_train.csv')
            testing_set = pd.read_csv(self.path+'/test.csv/mnist_test.csv')
            training_set = np.array(training_set)
            testing_set = np.array(testing_set)
            training_labels = np.array(training_set[:, 0]) # all rows of first columns
            training_examples = np.array(training_set[:, 1:]) #all data except first column
            training_labels = np.atleast_2d(training_labels)
            testing_labels = np.array(testing_set[:, 0])
            testing_examples = np.array(testing_set[:, 1:])
            testing_labels = np.atleast_2d(testing_labels)

            return training_examples/255, training_labels,  testing_examples/255, testing_labels # X , Y
        elif self.dataset_name == 'cifar_10':
            training_examples = []
            training_labels = []
            names = os.listdir(self.path)
            for name in names:
                if '_batch' in name:
                    with open(self.path+'/'+name, 'rb') as f:
                        data = pickle.load(f, encoding='bytes')
                        if 'test' in name: #test_batch
                            testing_examples = data[b'data']
                            testing_labels = data[b'labels']
                        else:
                            training_examples.append(data[b'data'])
                            training_labels.append(data[b'labels'])
            training_examples = np.array(training_examples)
            training_labels = np.array(testing_labels)
            training_labels = training_labels.reshape((-1, 1))
            training_examples = training_examples.reshape((-1,3072))
            testing_labels = np.atleast_2d(testing_labels)
            training_labels = np.atleast_2d(training_labels.T) # onerow
            return training_examples/255, training_labels,  testing_examples/255, testing_labels


    def labels_to_onehot(self,labels):
        max = np.max(labels)
        enc = np.zeros((max + 1, labels.shape[1]))
        for i in range(labels.shape[1]):
            for j in range(max):
                enc[j][i] = (labels[0][i] == j)  ###hot encoding trainLabels
                if (labels[0][i] == 9):
                    enc[9][i] = 1
        onehot_labels = enc
        return onehot_labels












































'''files = [
    ['training set images', 'train-images-idx3-ubyte.gz'],
    ['test set images', 't10k-images-idx3-ubyte.gz'],
    ['training set labels', 'train-labels-idx1-ubyte.gz'],
    ['test set labels', 't10k-labels-idx1-ubyte.gz']
]


def download():
    url = 'http://yann.lecun.com/exdb/mnist/'
    for file in files:
        urllib.urlretrieve(url + str(file[1]), file[0])


def save():
    data = {}
    for file in files[:2]:
        with gzip.open(file[1], 'rb') as f:
            data[file[0]] = np.frombuffer(f.read(), np.uint8, count=-1, offset=16).reshape(-1, 784)

    for file in files[-2:]:
        with gzip.open(file[1], 'rb') as f:
            data[file[0]] = np.frombuffer(f.read(), np.uint8, count=-1, offset=8)

    with open('mnst.pkl', 'wb') as f:
        pickle.dump(data, f)


def load():
    with open('mnst.pkl', 'wb') as f:
        data = pickle.load(f, encoding="UTF-8")
    return data


def batch(num_of_batches):
    data = load()
    X = data['training set images']
    Y = data['training set labels']
    X = X.reshape(num_of_batches, (len(X)/num_of_batches), len(X[0]))
    Y = Y.reshape(num_of_batches, (len(X)/num_of_batches), len(X[0]))


save()
load()
'''



































'''files = [
    ['training set images', 'train-images-idx3-ubyte.gz'],
    ['test set images', 't10k-images-idx3-ubyte.gz'],
    ['training set labels', 'train-labels-idx1-ubyte.gz'],
    ['test set labels', 't10k-labels-idx1-ubyte.gz']
]


def download():
    url = 'http://yann.lecun.com/exdb/mnist/'
    for file in files:
        urllib.urlretrieve(url + str(file[1]), file[0])


def save():
    data = {}
    for file in files[:2]:
        with gzip.open(file[1], 'rb') as f:
            data[file[0]] = np.frombuffer(f.read(), np.uint8, count=-1, offset=16).reshape(-1, 784)

    for file in files[-2:]:
        with gzip.open(file[1], 'rb') as f:
            data[file[0]] = np.frombuffer(f.read(), np.uint8, count=-1, offset=8)

    with open('mnst.pkl', 'wb') as f:
        pickle.dump(data, f)


def load():
    with open('mnst.pkl', 'wb') as f:
        data = pickle.load(f, encoding="UTF-8")
    return data


def batch(num_of_batches):
    data = load()
    X = data['training set images']
    Y = data['training set labels']
    X = X.reshape(num_of_batches, (len(X)/num_of_batches), len(X[0]))
    Y = Y.reshape(num_of_batches, (len(X)/num_of_batches), len(X[0]))


save()
load()
'''