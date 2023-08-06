import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def plotDataset(x, dataset, index=0, n=9):
    '''
    Function to visualize MNIST data set
    Parameters
    ----------
    x : multi-dimensional array
    index : integer
            plot figure i
    n : integer
        plot n figures 
    Returns
    -------
    None.
    '''
    num = range(index, index+n)
    counter=0
    if dataset is 'CIFAR10':
        for i in num:
            # define subplot
            plt.subplot(330 + 1 + counter)
            # reshape array and define rgb values
            im_r = x[i][0:1024].reshape(32, 32)
            im_g = x[i][1024:2048].reshape(32, 32)
            im_b = x[i][2048:].reshape(32, 32)
            # reconnect rgb arrays
            img = np.dstack((im_r, im_g, im_b))   
            # plot raw pixel data
            plt.imshow(img)
            # increment counter to draw multiple images in same plot
            counter = counter+1
    else:
        for i in num:
            # define subplot
            plt.subplot(330 + 1 + counter)
            im1 = x[i][0:784].reshape(28,28)
            # reshape image and plot raw pixel data
            plt.imshow(x[i].reshape(28,28), cmap=plt.get_cmap('gray'))
            # increment counter to draw multiple images in same plot
            counter = counter+1
    # show the figure
    plt.show()
    

    
def visualizeMetrics(metrics_output, ep):
    epochs = range(1,ep+1,1)
    loss_train = []
    acc_train =[]
    f1_train=[]
    p_train=[]
    r_train=[]
    
    for key,val in metrics_output.items():
        if key.startswith("loss"):
            loss_train.append(val)
        elif key.startswith("accuracy"):
            acc_train.append(val)
        elif key.startswith("f1"):
            f1_train.append(val)
        elif key.startswith("precision"):
            p_train.append(val)
        elif key.startswith("recall"):
            r_train.append(val)
    
    if len(loss_train) == ep:
        plt.plot(epochs, loss_train, label='Training Loss')
        plt.title('Training loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.show()
    if len(acc_train) == ep:
        plt.plot(epochs, acc_train, label='Training Accuracy')
        plt.title('Training Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.show()
    if len(f1_train) == ep:
        plt.plot(epochs, f1_train, label='Training F1 score')
        plt.title('Training F1 score')
        plt.xlabel('Epochs')
        plt.ylabel('F1 score')
        plt.show()
    if len(p_train) == ep:
        plt.plot(epochs, p_train, label='Training Precision')
        plt.title('Training Precision')
        plt.xlabel('Epochs')
        plt.ylabel('Precision')
        plt.show()
    if len(r_train) == ep:
        plt.plot(epochs, r_train, label='Training Recall')
        plt.title('Training Recall')
        plt.xlabel('Epochs')
        plt.ylabel('Recall')
        plt.show()
