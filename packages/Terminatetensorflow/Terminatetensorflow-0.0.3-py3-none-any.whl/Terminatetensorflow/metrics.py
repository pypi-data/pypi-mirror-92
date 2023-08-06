import numpy as np
# from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, precision_score, recall_score
import pandas as pd


def accuracy_metrics(y_hat,y_label):
    count=0
    i=0
    while i<len(y_hat):
        if y_hat[i]==y_label[i] :
            count=count+1
        i=i+1
    accur=count/len(y_hat)
    return accur

def confusion_matrix(y_hat, y_label):

    classes = np.unique(y_label) # extract the different classes
    matrix = np.zeros((len(classes), len(classes))) # initialize the confusion matrix with zeros

    for i in range(len(classes)):
        for j in range(len(classes)):

            matrix[i, j] = np.sum((y_label == classes[i]) & (y_hat == classes[j]))

    return matrix


def TP(y_hat, y_label,Type):
    conf_mat = confusion_matrix(y_hat, y_label)
    if Type == 'micro':
        return sum(np.diag(conf_mat))
    elif Type == 'macro':
        return np.diag(conf_mat)

def FP(y_hat, y_label,Type):
    if Type == 'micro':
        fp=[]
        conf_mat = confusion_matrix(y_hat, y_label)
        for i in range(conf_mat.shape[1]):
            fp.append(sum(conf_mat[:,i]) - conf_mat[i,i])
        return sum(fp)
    elif Type == 'macro':
        conf_mat = confusion_matrix(y_hat, y_label)
        return np.sum(conf_mat, axis=0) - TP(y_hat, y_label,'macro')
        

def FN(y_hat, y_label , Type):
    if Type == 'micro':
        fn=[]
        conf_mat = confusion_matrix(y_hat, y_label)
        for i in range(conf_mat.shape[1]):
            fn.append(sum(conf_mat[i,:]) - conf_mat[i,i])
        return sum(fn)
    elif Type == 'macro':
        conf_mat = confusion_matrix(y_hat, y_label)
        return np.sum(conf_mat, axis=1) - TP(y_hat, y_label,'macro')
        

def Accuracy(y_hat, y_label, data_size):
    return np.sum(TP(y_hat, y_label)/data_size)

def Recall(y_hat, y_label,Type):
    if Type == 'micro':    
        tp = TP(y_hat, y_label,'micro')
        fp = FP(y_hat, y_label,'micro')
        return tp / (tp+fp)
    
    elif Type == 'macro':
        return np.mean(TP(y_hat, y_label,'macro') / (TP(y_hat, y_label,'macro') + FN(y_hat, y_label,'macro')))
        
    

def Precision(y_hat, y_label,Type):
    if Type == 'micro':       
        tp = TP(y_hat, y_label,'micro')
        fn = FN(y_hat, y_label,'micro')
        return tp / (tp+fn)
    elif Type == 'macro':
        return np.mean(TP(y_hat, y_label,'macro') / (TP(y_hat, y_label,'macro') + FP(y_hat, y_label,'macro')))

        
        
def F1_score(y_hat, y_label,Type):
    if TP(y_hat, y_label,'micro') > 0:
        P = Precision(y_hat, y_label,Type)
        R = Recall(y_hat, y_label,Type)
        return 2*((P*R)/(P+R)) 
    else:
        return 0


# a = confusion_matrix(trainLabels_.T,Y_hat.T)
# TP(Y_hat.T,trainLabels_.T,'macro')
# FP(Y_hat.T,trainLabels_.T,'macro')
# FN(Y_hat.T,trainLabels_.T,'macro')
# Precision(Y_hat.T,trainLabels_.T,'micro')
# Recall(Y_hat.T,trainLabels_.T,'micro')
# F1_score(Y_hat.T,trainLabels_.T,'macro')


# print (precision_score(y_class.T,pred.T,average='micro'))
# print (recall_score(y_class.T, pred.T, average='micro'))
# print (f1_score(y_class.T, pred.T, average='micro'))
# print(accuracy_score(y_class.T,predict.T))
