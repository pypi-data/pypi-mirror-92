import numpy as np

# def log(X): #replace log(0)=-9999999 instead of -inf
#     with np.errstate(divide='ignore'):
#         res = np.log(X)
#     res[np.isneginf(res)]=-9999999
#     return res

def compute_multiclass_loss(Y, Y_hat):
    L_sum = np.sum(np.multiply(Y, np.log(Y_hat + 1e-9)))
    m = Y.shape[1]
    L = -(1/m) * L_sum

    return L

def compute_mse_loss(Y, Y_hat):
    m = Y_hat.shape[1]              
    cost= (1 / m) * np.sum(np.sqrt(np.square(np.subtract(Y,Y_hat))))
    
    return cost