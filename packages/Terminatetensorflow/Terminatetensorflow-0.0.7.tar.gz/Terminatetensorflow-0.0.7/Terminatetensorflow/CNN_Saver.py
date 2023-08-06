import pickle
import os

class CNN_Saver():
     
    def save(self,LeNet):
        filename = 'saved_model_mnist.dat'
        pickle.dump(LeNet.get_params(), open(filename, 'wb'))
        print("file saved")
            
    def restore(self,filename):   
        with open(os.getcwd() +'\\' +filename, 'rb') as handle:
            unserialized_data = pickle.load(handle)
        return unserialized_data