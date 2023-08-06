import numpy as np
from Terminatetensorflow.dense import *
from Terminatetensorflow.loss import *
from Terminatetensorflow.metrics import *
from Terminatetensorflow.LiveAnimation import *
from PIL import Image , ImageOps
  


class Model:
    def __init__(self, layers_dims, activation_fns):
        self.layers = []
        self.num_of_layers = len(layers_dims)

        for i in range(1, self.num_of_layers):
            self.layers.append(layer(layers_dims[i], layers_dims[i-1], activation_fns[i-1]))
        
        self.loss = None
    
    def predict(self, X):
        output = X
        for layer in self.layers:
            output = layer.forward_prop(output)

        _pred = np.array(output[0])        
        pred = np.zeros((10,X.shape[1]))  
        pred = np.argmax(output,axis=0)
        
        return np.atleast_2d(pred)
        
    def predict_ext_image(self, path):
        
        px = Image.open(path)     
        gray_image = ImageOps.grayscale(px)    
        new_image = gray_image.resize((28, 28))   
        
        pix_val = np.array(list(new_image.getdata()))    
        pix_val =np.atleast_2d(pix_val)
        pix_val = pix_val/255
        pred = Model.predict(self,pix_val.T)
        print("Predicted val", pred)
    
    def fit(self, X, y, learning_rate, metrics, epochs, batch_size, costt, optimizer):
        y_class = np.zeros((10,y.shape[1]))  
        y_class = np.atleast_2d(np.argmax(y,axis=0))
        batch_number = int(-(-X.shape[1]/batch_size // 1))
        metrics_output = {}
        
        for i in range(epochs):
            file_name = "animation_loss.txt"
            file_name_2 = "animation_acc.txt"
            file = open(file_name,"a+")
            file_2 = open(file_name_2,"a+")
            
            for j in range(batch_number):
                if j == batch_number:
                        
                    output = X[:,batch_size*(j):]
                    A = []
                    A.append(output)
                    for layer in self.layers:
                        output = layer.forward_prop(output)
                        A.append(output)                
                    
                    if (costt == "multiclass"):
                        self.loss = compute_multiclass_loss(y[:,batch_size*(j):], output)
                    elif (costt == "mse"):
                        self.loss = compute_mse_loss(y[:,batch_size*(j):], output)
                        
                    output_layer = True
                    dA_prev = 0
                    k = self.num_of_layers - 1
                    for layer in reversed(self.layers):
                        dA_prev,_,_ = layer.backward_prop(A[k - 1], dA_prev, y[:,batch_size*(j):], output_layer)
                        output_layer = False
                        k = k - 1
                    
                    if optimizer == "momentum":
                        for layer in self.layers:
                            layer.update_parameters_momentum(learning_rate)
                    elif optimizer == "rmsprop":
                        for layer in self.layers:
                            layer.update_parameters_rmsprop(learning_rate)
                    elif optimizer == "adam":
                        for layer in self.layers:
                            layer.update_parameters_adam(learning_rate)
                    else:
                        for layer in self.layers:
                            layer.update_parameters(learning_rate)
                         
                         
                else:
                    
                    output = X[:,batch_size*(j):batch_size*(j+1)]
                    A = []
                    A.append(output)
                    for layer in self.layers:
                        output = layer.forward_prop(output)
                        A.append(output)                
                    
                    if (costt == "multiclass"):
                        self.loss = compute_multiclass_loss(y[:,batch_size*(j):batch_size*(j+1)], output)
                    elif (costt == "mse"):
                        self.loss = compute_mse_loss(y[:,batch_size*(j):batch_size*(j+1)], output)
                        
                    output_layer = True
                    dA_prev = 0
                    k = self.num_of_layers - 1
                    for layer in reversed(self.layers):
                        dA_prev,_,_ = layer.backward_prop(A[k - 1], dA_prev, y[:,batch_size*(j):batch_size*(j+1)], output_layer)
                        output_layer = False
                        k = k - 1
                    
                    if optimizer == "rmsprop":
                        for layer in self.layers:
                            update_parameters_rmsprop(learning_rate)
                    elif optimizer == "adam":
                        for layer in self.layers:
                            update_parameters_adam(learning_rate)
                    elif optimizer == "momentum":
                        for layer in self.layers:
                            layer.update_parameters_momentum(learning_rate)
                    else:
                        for layer in self.layers:
                            layer.update_parameters(learning_rate)
                        
            print("Epoch", i, "->")
            print("\t\tLoss =", ("%.4f" % self.loss ))
            metrics_output['loss'+str(i)] = self.loss
            pred = self.predict(X)
        
            file.write(f'{i},{self.loss}'+'\n')
            file.close()
            

            for j in range(len(metrics)-1):
                Type = metrics[len(metrics)-1]
                if metrics[j] == "accuracy":
                    acc = accuracy_metrics(pred.T, y_class.T) * 100
                    metrics_output["accuracy"+str(i)] = acc
                    print("\t\tAccuracy =", ("%.4f" % acc ))
                elif metrics[j] == "f1 score":
                    f1 = F1_score(pred.T, y_class.T,Type)
                    metrics_output["f1"+str(i)] = f1
                    print("\t\tF1 score =", ("%.4f" % f1 ))
                elif metrics[j] == "precision":
                    P = Precision(pred.T,y_class.T,Type)
                    metrics_output["precision"+str(i)] = P
                    print("\t\tPrecision =",("%.4f" % P))
                elif metrics[j] == "recall":
                    R = Recall(pred.T,y_class.T,Type)
                    metrics_output["recall"+str(i)] = R
                    print("\t\tRecall =",("%.4f" % R))                    
                elif metrics[j] == "confusion matrix":
                    np.set_printoptions(suppress=True)
                    conf_mat = confusion_matrix(pred.T,y_class.T)
                    print("\t\tConfusion Matrix : \n",conf_mat)
                    
                file_2.write(f'{i},{acc}'+'\n')
                file_2.close()
                
                
        # Loss GIF         
        draw_ = draw(epochs,file_name)
        draw_.save_gif()
        
        # ACC GIF
        draw_2 = draw(epochs,file_name_2)
        draw_2.save_gif()
        
        draw_.terminate()
        draw_2.terminate()

        print("\n___________________________________________________\n")
        print("Final cost:", ("%.5f" % self.loss ))
        
        for j in range(len(metrics)):
                if metrics[j] == "accuracy":
                    print("Final training accuracy:", ("%.5f" % acc ), "%")
                elif metrics[j] == "f1 score":
                     print("Final training value for F1 score:", ("%.5f" % f1 ))
                elif metrics[j] == "precision":
                    print("Final training value for Precision:", ("%.5f" % P ))
                elif metrics[j] == "recall":
                    print("Final training value for Recall:", ("%.5f" % R ))                    
                elif metrics[j] == "confusion matrix":
                    print("\t\tFinal training value for Confusion Matrix : \n", conf_mat)
        print("\n___________________________________________________\n")
        
        return metrics_output