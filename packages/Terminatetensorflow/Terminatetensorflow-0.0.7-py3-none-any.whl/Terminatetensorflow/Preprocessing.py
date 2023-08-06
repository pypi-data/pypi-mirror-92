import requests
import numpy as np
import pandas as pd
import os
import pickle
import gzip
import struct
import tarfile


def preprocessing_online(datasetName):
    if datasetName == 'MNIST':
        MNIST_trainFeatures = 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'
        MNIST_trainLabels = 'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz'
        MNIST_testFeatures = 'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz'
        MNIST_testLabels = 'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
        
        R1 = requests.get(MNIST_trainFeatures, allow_redirects=True)
        R2 = requests.get(MNIST_trainLabels, allow_redirects=True)
        R3 = requests.get(MNIST_testFeatures, allow_redirects=True)
        R4 = requests.get(MNIST_testLabels, allow_redirects=True)
        
        open('trainFeaturesMNIST.gz', 'wb').write(R1.content)
        open('trainLabelsMNIST.gz', 'wb').write(R2.content)
        open('testFeaturesMNIST.gz', 'wb').write(R3.content)
        open('testLabelsMNIST.gz', 'wb').write(R4.content)
        
            
        filenames = os.listdir(os.getcwd())
        for file in filenames:
            if 'MNIST.gz' in file:
                if file == 'trainFeaturesMNIST.gz':
                    with gzip.open('trainFeaturesMNIST.gz', 'rb') as f_in:
                        zero, data_type, dims = struct.unpack('>HBB', f_in.read(4))
                        shape = tuple(struct.unpack('>I', f_in.read(4))[0] for d in range(dims))
                        trainFeatures = np.frombuffer(f_in.read(), dtype=np.uint8).reshape(shape)
                if file == 'trainLabelsMNIST.gz':
                    with gzip.open('trainLabelsMNIST.gz', 'rb') as f_in:
                        zero, data_type, dims = struct.unpack('>HBB', f_in.read(4))
                        shape = tuple(struct.unpack('>I', f_in.read(4))[0] for d in range(dims))
                        trainLabels = np.frombuffer(f_in.read(), dtype=np.uint8).reshape(shape)
                if file == 'testFeaturesMNIST.gz':
                    with gzip.open('testFeaturesMNIST.gz', 'rb') as f_in:
                        zero, data_type, dims = struct.unpack('>HBB', f_in.read(4))
                        shape = tuple(struct.unpack('>I', f_in.read(4))[0] for d in range(dims))
                        testFeatures = np.frombuffer(f_in.read(), dtype=np.uint8).reshape(shape)
                if file == 'testLabelsMNIST.gz':
                    with gzip.open('testLabelsMNIST.gz', 'rb') as f_in:
                        zero, data_type, dims = struct.unpack('>HBB', f_in.read(4))
                        shape = tuple(struct.unpack('>I', f_in.read(4))[0] for d in range(dims))
                        testLabels = np.frombuffer(f_in.read(), dtype=np.uint8).reshape(shape)
        
        testLabels = np.atleast_2d(testLabels)
        trainLabels= np.atleast_2d(trainLabels.T)
        testFeatures = testFeatures.reshape(-1,784)
        trainFeatures = trainFeatures.reshape(-1,784)
        trainFeatures = trainFeatures/255
        testFeatures = testFeatures/255 
        idx = np.random.permutation(len(trainFeatures))
        trainFeatures = trainFeatures[idx]
        TrainLabels = trainLabels.T[idx]
        trainLabels = TrainLabels.T
        Dataset = 'MNIST'
    
    elif datasetName == 'CIFAR10':
        CIFAR10 = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
        R = requests.get(CIFAR10, allow_redirects=True)
        open('cifar-10-python.tar.gz', 'wb').write(R.content)
        
        trainLabels = []
        trainFeatures = []
        Dataset = 'CIFAR10'
        tarfile.open('cifar-10-python.tar.gz', 'r:gz').extractall(os.getcwd())    
        path = os.getcwd()+'\cifar-10-batches-py'
        filenames = os.listdir(path)
        
        for file in filenames:
            if '_batch' in file:
                with open(path+'\\'+file, 'rb') as fo:
                    dict = pickle.load(fo, encoding='bytes')
                    if 'test' in file:
                        testLabels = dict[b'labels']
                        testFeatures = dict[b'data']
                    else:
                        trainLabels.append(dict[b'labels'])
                        trainFeatures.append(dict[b'data'])
            
        trainLabels = np.array(trainLabels)
        trainFeatures = np.array(trainFeatures)
        trainLabels = trainLabels.reshape((-1,1))
        trainFeatures = trainFeatures.reshape((-1,3072))
        testLabels = np.array(testLabels)
        testLabels =np.atleast_2d(testLabels)
        trainLabels =np.atleast_2d(trainLabels.T)
        trainFeatures = trainFeatures/255
        testFeatures = testFeatures/255 
        idx = np.random.permutation(len(trainFeatures))
        trainFeatures = trainFeatures[idx]
        TrainLabels = trainLabels.T[idx]
        trainLabels = TrainLabels.T
    
    return trainFeatures, trainLabels, testFeatures, testLabels, Dataset



def preprocessing(path):

    #path = r'D:\Gam3a\Neural\Project\Datasets\CIFAR-10\cifar-10-batches-py'
    data_directory_path = path
    filenames = os.listdir(data_directory_path)

    #For CIFAR Dataset:

    if 'csv' not in filenames[0]:

        trainLabels = []
        trainFeatures = []
        Dataset = 'CIFAR10'
        for file in filenames:
            if '_batch' in file:
                with open(path+'/'+file, 'rb') as fo:
                    dict = pickle.load(fo, encoding='bytes')
                    if 'test' in file:
                        testLabels = dict[b'labels']
                        testFeatures = dict[b'data']
                    else:
                        trainLabels.append(dict[b'labels'])
                        trainFeatures.append(dict[b'data'])

        trainLabels = np.array(trainLabels)
        trainFeatures = np.array(trainFeatures)
        trainLabels = trainLabels.reshape((-1,1))
        trainFeatures = trainFeatures.reshape((-1,3072))
        testLabels = np.array(testLabels)
        testLabels =np.atleast_2d(testLabels)
        trainLabels =np.atleast_2d(trainLabels.T)
        trainFeatures = trainFeatures/255
        testFeatures = testFeatures/255 
        idx = np.random.permutation(len(trainFeatures))
        trainFeatures = trainFeatures[idx]
        TrainLabels = trainLabels.T[idx]
        trainLabels = TrainLabels.T
        

    #For MNIST Dataset:

    else:
        trainData = pd.read_csv(path+'/train.csv')
        testData = pd.read_csv(path+'/test.csv')
        trainData = np.array(trainData)
        testData = np.array(testData)
        trainLabels = np.array(trainData[:,0])
        trainFeatures = np.array(trainData[:,1:])
        testFeatures = np.array(testData[:,1:])
        testLabels = np.array(testData[:,0])
        testLabels =np.atleast_2d(testLabels)
        trainLabels =np.atleast_2d(trainLabels.T)
        trainFeatures = trainFeatures/255
        testFeatures = testFeatures/255 
        idx = np.random.permutation(len(trainFeatures))
        trainFeatures = trainFeatures[idx]
        TrainLabels = trainLabels.T[idx]
        trainLabels = TrainLabels.T
        Dataset = 'MNIST'
        
    return trainFeatures, trainLabels, testFeatures, testLabels, Dataset



def labels_to_onehot(labels):
    b = np.zeros((labels.size, labels.max()+1))
    b[np.arange(labels.size),labels] = 1
    b = b.T
    
    return b



#'D:\Gam3a\Neural\Project\Datasets\CIFAR-10\cifar-10-batches-py'
