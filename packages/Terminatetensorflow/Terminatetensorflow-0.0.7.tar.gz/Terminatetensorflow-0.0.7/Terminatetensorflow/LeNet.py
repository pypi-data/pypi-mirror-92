from Terminatetensorflow.conv import *
from Terminatetensorflow.pool import *
from Terminatetensorflow.dense import *
from Terminatetensorflow.actvfn import *
from Terminatetensorflow.loss import *


class LeNet():
    def __init__(self):
        self.conv1 = Conv(nb_filters = 6, filter_size = 5, nb_channels = 1)
        self.pool1 = AvgPool(filter_size = 2, stride = 2)
        self.conv2 = Conv(nb_filters = 16, filter_size = 5, nb_channels = 6)
        self.pool2 = AvgPool(filter_size = 2, stride = 2)
        self.pool2_shape = None
        self.fc1 = layer(128, 400, "tanh")
        self.fc2 = layer(84, 128, "tanh")
        self.fc3 = layer(10,84,"softmax")
        self.A = []
        self.actCache = []
        self.layers = [self.conv1, self.conv2, self.fc1, self.fc2, self.fc3]
        
        
    def forward(self, X):
        self.A = []
        conv1 = self.conv1.forward(X) #(6x28x28)
        self.actCache.append(conv1)
        act1 = tanh(conv1)
        pool1 = self.pool1.forward(act1) #(6x14x14)

        conv2 = self.conv2.forward(pool1) #(16x10x10)
        self.actCache.append(conv2)
        act2 = tanh(conv2)
        pool2 = self.pool2.forward(act2) #(16x5x5)
        
        self.pool2_shape = pool2.shape #Need it in backpropagation.
        pool2_flatten = pool2.reshape(self.pool2_shape[0], -1) #(1x400)
        self.A.append(pool2_flatten.T)
        fc1 = self.fc1.forward_prop(pool2_flatten.T) #(1x120) 
        self.A.append(fc1)
        fc2 = self.fc2.forward_prop(fc1) #(1x84)    
        
        # print(fc2.shape)
        self.A.append(fc2)
        fc3 = self.fc3.forward_prop(fc2) #(1x10)
        self.A.append(fc3)

        y_pred = fc3

        return y_pred
    
    def backward(self, y_pred, y):
        deltaL = y_pred - y
        #Compute gradient for weight/bias between fc3 and fc2.
        deltaL, dW5, db5= self.fc3.backward_prop(self.A[2],0,y,output_layer = True)
        #Compute error at fc2 layer.
        #deltaL = self.tanh4.backward(deltaL) #(1x84) 
        
        #Compute gradient for weight/bias between fc2 and fc1.
        deltaL, dW4, db4= self.fc2.backward_prop(self.A[1],deltaL,y,output_layer = False)
        #Compute error at fc1 layer.
       # deltaL = self.tanh3.backward(deltaL) #(1x120)
        
        #Compute gradient for weight/bias between fc1 and pool2 and compute 
        #error too (don't need to backpropagate through tanh here).
        deltaL, dW3, db3 = self.fc1.backward_prop(self.A[0],deltaL,y,output_layer = False) #(1x400)
        deltaL = deltaL.reshape(self.pool2_shape) #(16x5x5)
        
        
        #Distribute error through pool2 to conv2.
        deltaL = self.pool2.backward(deltaL) #(16x10x10)
        #Distribute error through tanh.
        deltaL = derivative_tanh(self.actCache[1]) * deltaL
        
        #Compute gradient for weight/bias at conv2 layer and backpropagate
        #error to conv1 layer.
        deltaL, dW2, db2 = self.conv2.backward(deltaL) #(6x14x14)

        #Distribute error through pool1 by creating a temporary pooling layer
        #of conv1 shape.
        deltaL = self.pool1.backward(deltaL) #(6x28x28)
        #Distribute error through tanh.
        deltaL = derivative_tanh(self.actCache[0]) * deltaL
    
        #Compute gradient for weight/bias at conv1 layer and backpropagate
        #error at conv1 layer.
        deltaL, dW1, db1 = self.conv1.backward(deltaL) #(1x32x32)
    
        grads = { 
                'dW1': dW1, 'db1': db1,
                'dW2': dW2, 'db2': db2, 
                'dW3': dW3, 'db3': db3,
                'dW4': dW4, 'db4': db4,
                'dW5': dW5, 'db5': db5
        }

        return grads
    
    
    def get_params(self):
        params = {}
        for i, layer in enumerate(self.layers):
            try:
                params['W' + str(i+1)] = layer.W['val']
                params['b' + str(i+1)] = layer.b['val']
            except:
                  params['W' + str(i+1)] = layer.weights
                  params['b' + str(i+1)] = layer.biases            

        return params

    def set_params(self, params):
        for i, layer in enumerate(self.layers):
            try:
                layer.W['val'] = params['W'+ str(i+1)]
                layer.b['val'] = params['b' + str(i+1)]
            except:
                layer.weights = params['W'+ str(i+1)]
                layer.biases = params['b' + str(i+1)]
                
                
    def update_params(self,grads,learning_rate):
        for i, layer in enumerate(self.layers):       
            try:                
                layer.W['val'] = layer.W['val'] - learning_rate*grads['dW'+str(i+1)] 
                layer.b['val'] = layer.b['val'] - learning_rate*grads['db'+str(i+1)]
            except:
                    layer.weights = layer.weights - learning_rate*grads['dW'+str(i+1)]    
                    layer.biases = layer.biases - learning_rate*grads['db'+str(i+1)] 
                    
    def update_parameters_momentum(self, grads, learning_rate, gamma=0.9):
        
        for i, layer in enumerate(self.layers): 
            try:     
            
               layer.v_w = gamma * layer.v_w +  (1 - gamma)* grads['dW'+str(i+1)]
               layer.v_b = gamma * layer.v_b +  (1 - gamma)* grads['db'+str(i+1)]
               layer.W['val'] = layer.W['val'] - learning_rate * layer.v_w
               layer.b['val'] = layer.b['val'] - learning_rate * layer.v_b
                           
            except:
                
                layer.v_w = gamma*layer.v_w +  (1 - gamma)* layer.dW
                layer.v_b = gamma*layer.v_b +  (1 - gamma)* layer.db
                layer.weights = layer.weights - learning_rate * layer.v_w
                layer.biases = layer.biases -  learning_rate  *  layer.v_b
                
    def update_parameters_rmsprop(self, grads, learning_rate, beta=0.9):
        
        for i, layer in enumerate(self.layers): 
            try:     
            
               layer.s_w = beta * layer.s_w +  (1 - beta)* np.power(grads['dW'+str(i+1)],2)
               layer.s_b = beta * layer.s_b +  (1 - beta)* np.power(grads['db'+str(i+1)],2)
               layer.W['val'] = layer.W['val'] - learning_rate * np.divide(grads['dW'+str(i+1)],np.sqrt(layer.s_w))
               layer.b['val'] = layer.b['val'] - learning_rate * np.divide(grads['db'+str(i+1)],np.sqrt(layer.s_b))
                           
            except:
                
                layer.s_w = beta*layer.s_w +  (1 - beta)* np.power(grads['dW'+str(i+1)],2)
                layer.s_b = beta*layer.s_b +  (1 - beta)* np.power(grads['db'+str(i+1)],2)
                layer.weights = layer.weights - learning_rate * np.divide(grads['dW'+str(i+1)],np.sqrt(layer.s_w))
                layer.biases = layer.biases -  learning_rate  *  np.divide(grads['db'+str(i+1)],np.sqrt(layer.s_b))

                
    def update_parameters_adam(self, grads, learning_rate = 0.01, t = 2, beta1 = 0.9, beta2 = 0.999,  epsilon = 1e-8):
        for i, layer in enumerate(self.layers): 
            try:     
               layer.v_w = beta1 * layer.v_w +  (1 - beta1)* np.atleast_2d(grads['dW'+str(i+1)])
               layer.v_b = beta1 * layer.v_b +  (1 - beta1)* grads['db'+str(i+1)]
               v_wcorrected = layer.v_w / (1-np.power(beta1,t))
               v_bcorrected = layer.v_b / (1-np.power(beta1,t))
               layer.s_w = beta2*layer.s_w + (1-beta2)*np.power(grads['dW'+str(i+1)],2)
               layer.s_b = beta2*layer.s_b + (1-beta2)*np.power(grads['db'+str(i+1)],2)
               s_wcorrected = layer.s_w / (1-np.power(beta2,t))
               s_bcorrected = layer.s_b / (1-np.power(beta2,t))
               layer.W['val'] = layer.W['val'] - learning_rate*v_wcorrected / np.sqrt(s_wcorrected + epsilon)
               layer.b['val'] = layer.b['val'] - learning_rate*v_bcorrected / np.sqrt(s_bcorrected + epsilon)

            except:
                layer.v_w = beta1*layer.v_w +  (1 - beta1)* layer.dW
                layer.v_b = beta1*layer.v_b +  (1 - beta1)* layer.db
                v_wcorrected = layer.v_w / (1-np.power(beta1,t))
                v_bcorrected = layer.v_b / (1-np.power(beta1,t))
                layer.s_w = beta2*layer.s_w + (1-beta2)*np.power(layer.dW,2)
                layer.s_b = beta2*layer.s_b + (1-beta2)*np.power(layer.db,2)
                s_wcorrected = layer.s_w / (1-np.power(beta2,t))
                s_bcorrected = layer.s_b / (1-np.power(beta2,t))
                layer.weights = layer.weights - learning_rate*v_wcorrected / np.sqrt(s_wcorrected + epsilon)
                layer.biases = layer.biases - learning_rate*v_bcorrected / np.sqrt(s_bcorrected + epsilon)
                
                

    def predict(self, X):
        output = self.forward(X)

        _pred = np.array(output[0])        
        pred = np.zeros((10,X.shape[1]))  
        pred = np.argmax(output,axis=0)
        
        return np.atleast_2d(pred)

    def fit(self, X, Y, epochs, learning_rate, costt, batch_size, optimizer="adam"):
        Y_class = np.zeros((10,Y.shape[1]))  
        Y_class = np.atleast_2d(np.argmax(Y,axis=0))
                
        batch_number = int(-(-X.shape[0]/batch_size // 1))
        metrics_output = {}
        
        for i in range(epochs):
            
            current_batch=0
            print('\repoch:{}/{} [{}] {}%'.format(i+1, epochs, '.' * (50), 0), end='\r')
            for j in range(batch_number-1):

                current_batch += 1
                if j == batch_number-1:
                    
                    x = X[batch_size*(j):,:,:,:]
                    y = Y[:,batch_size*(j):]
                    
                else:
                    x = X[batch_size*(j):batch_size*(j+1),:,:,:]
                    y = Y[:,batch_size*(j):batch_size*(j+1)]
                    
                y_hat = self.forward(x)
                
                # acc = accuracy_metrics(y_hat.T, y.T) * 100
                
                
                if (costt == "multiclass"):
                    loss = compute_multiclass_loss(y, y_hat)
                elif (costt == "mse"):
                    loss = compute_mse_loss(y, y_hat)
                    
                grads = self.backward(y_hat, y)
                if optimizer == "adam":
                    self.update_parameters_adam(grads, learning_rate)
                    
                elif optimizer == "rmsprop":
                    self.update_parameters_rmsprop(grads, learning_rate)
                
                elif optimizer == "momentum":
                    self.update_parameters_momentum(grads, learning_rate)
                
                else:
                    self.update_params(grads, learning_rate)

                done = int(100*current_batch/batch_number)
                print('\repoch:{}/{} [{}{}] {}% '.format(i+1, epochs,'█' * int(done/2), '.' * int(50-int(done/2)), done, ), end='\r')
            
            print("Epoch", i+1, "->")
            print("\t\tLoss =", ("%.4f" % loss ))
            metrics_output["loss"+str(i)] = loss
            # print("\t\Acc =", ("%.4f" % acc ))
            
        return metrics_output
        


