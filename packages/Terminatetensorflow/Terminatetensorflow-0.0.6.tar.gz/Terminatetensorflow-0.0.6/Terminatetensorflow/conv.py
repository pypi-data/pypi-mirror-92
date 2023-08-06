import numpy as np
from Terminatetensorflow.actvfn import *

def get_indices(X_shape, HF, WF, stride, pad):
    """
        Returns index matrices in order to transform our input image into a matrix.
        Parameters:
        -X_shape: Input image shape.
        -HF: filter height.
        -WF: filter width.
        -stride: stride value.
        -pad: padding value.
        Returns:
        -i: matrix of index i.
        -j: matrix of index j.
        -d: matrix of index d. 
            (Use to mark delimitation for each channel
            during multi-dimensional arrays indexing).
    """
    # get input size
    m, n_C, n_H, n_W = X_shape

    # get output size
    out_h = int((n_H + 2 * pad - HF) / stride) + 1
    out_w = int((n_W + 2 * pad - WF) / stride) + 1
  
    # ----Compute matrix of index i----

    # Level 1 vector.
    level1 = np.repeat(np.arange(HF), WF)
    # Duplicate for the other channels.
    level1 = np.tile(level1, n_C)
    # Create a vector with an increase by 1 at each level.
    everyLevels = stride * np.repeat(np.arange(out_h), out_w)
    # Create matrix of index i at every levels for each channel.
    i = level1.reshape(-1, 1) + everyLevels.reshape(1, -1)

    # ----Compute matrix of index j----
    
    # Slide 1 vector.
    slide1 = np.tile(np.arange(WF), HF)
    # Duplicate for the other channels.
    slide1 = np.tile(slide1, n_C)
    # Create a vector with an increase by 1 at each slide.
    everySlides = stride * np.tile(np.arange(out_w), out_h)
    # Create matrix of index j at every slides for each channel.
    j = slide1.reshape(-1, 1) + everySlides.reshape(1, -1)

    # ----Compute matrix of index d----

    # This is to mark delimitation for each channel
    # during multi-dimensional arrays indexing.
    d = np.repeat(np.arange(n_C), HF * WF).reshape(-1, 1)

    return i, j, d

def im2col(X, HF, WF, stride, pad):
    """
        Transforms our input image into a matrix.
        Parameters:
        - X: input image.
        - HF: filter height.
        - WF: filter width.
        - stride: stride value.
        - pad: padding value.
        Returns:
        -cols: output matrix.
    """
    # Padding
    X_padded = np.pad(X, ((0,0), (0,0), (pad, pad), (pad, pad)), mode='constant')
    i, j, d = get_indices(X.shape, HF, WF, stride, pad)
    # Multi-dimensional arrays indexing.
    cols = X_padded[:, d, i, j]
    cols = np.concatenate(cols, axis=-1)
    return cols

def col2im(dX_col, X_shape, HF, WF, stride, pad):
    """
        Transform our matrix back to the input image.
        Parameters:
        - dX_col: matrix with error.
        - X_shape: input image shape.
        - HF: filter height.
        - WF: filter width.
        - stride: stride value.
        - pad: padding value.
        Returns:
        -x_padded: input image with error.
    """
    # Get input size
    N, D, H, W = X_shape
    # Add padding if needed.
    H_padded, W_padded = H + 2 * pad, W + 2 * pad
    X_padded = np.zeros((N, D, H_padded, W_padded))
    
    # Index matrices, necessary to transform our input image into a matrix. 
    i, j, d = get_indices(X_shape, HF, WF, stride, pad)
    # Retrieve batch dimension by spliting dX_col N times: (X, Y) => (N, X, Y)
    dX_col_reshaped = np.array(np.hsplit(dX_col, N))
    # Reshape our matrix back to image.
    # slice(None) is used to produce the [::] effect which means "for every elements".
    np.add.at(X_padded, (slice(None), d, i, j), dX_col_reshaped)
    # Remove padding from new image if needed.
    if pad == 0:
        return X_padded
    elif type(pad) is int:
        return X_padded[pad:-pad, pad:-pad, :, :]

class Conv():
    
    def __init__(self, nb_filters, filter_size, nb_channels, stride=1, padding=0):
        self.n_F = nb_filters
        self.f = filter_size
        self.n_C = nb_channels
        self.s = stride
        self.p = padding
        # Xavier-Glorot initialization - used for sigmoid, tanh.
        self.W = {'val': np.random.randn(self.n_F, self.n_C, self.f, self.f)*np.sqrt(1./self.f) ,
                  'grad': np.zeros((self.n_F, self.n_C, self.f, self.f))}  
        self.b = {'val': np.random.randn(self.n_F), 'grad': np.zeros((self.n_F))}
        
        self.v_w = np.zeros((self.n_F, self.n_C, self.f, self.f)) 
        self.v_b = np.zeros((self.n_F))
        self.s_w = np.zeros((self.n_F, self.n_C, self.f, self.f)) 
        self.s_b = np.zeros((self.n_F))
        self.w_squared = np.zeros((self.n_F, self.n_C, self.f, self.f)) 
        
        self.cache = None

    def conv_single_step(self, X_slice_prev, W, b):
        s = np.multiply(X_slice_prev, W) + float(b)
        # Sum over all entries of the volume s.
        Z = np.sum(s)
        
        return Z
    
    def zero_pad(self, X, P):
        return np.pad(X, ((0,0), (P,P),(P,P), (0,0)), mode='constant', constant_values = (0,0))
    
    def fprop_slow(self,X):
        X =  self.zero_pad(X , self.padding)
        
        m = X.shape[0]    
        FH = self.filters.shape[0]
        FW = self.filters.shape[1]
        
        # output array
        Z = np.zeros((m, self.n_H, self.n_W, self.n_C)) 
        
        for i in range(m):                      # loop over the batch of training examples
            X_prev = X[i,:,:,:]               # Select ith training example's padded activation
            for h in range(self.n_H):           # loop over vertical axis of the output volume
                # Find the vertical start and end of the current "slice" 
                vert_start = h * self.stride
                vert_end = vert_start + FH
                for w in range(self.n_W):       # loop over horizontal axis of the output volume
                    # Find the horizontal start and end of the current "slice"
                    horiz_start = w * self.stride
                    horiz_end = horiz_start + FW
                    for c in range(self.n_C):   # loop over channels (= #filters) of the output volume                      
                        X_slice_prev = X_prev[vert_start:vert_end,horiz_start:horiz_end,:]
                        # Convolve the (3D) slice with the correct filter W and bias b, to get back one output neuron.
                        Z[i, h, w, c] = self.conv_single_step(X_slice_prev, self.filters[:,:,:,c], self.b[:,:,:,c])
        
        if self.act_fn == "sigmoid":
            A = sigmoid(Z)
        elif self.act_fn == "relu":
            A = relu(Z)
        elif self.act_fn == "tanh":
            A = tanh(Z)
        elif self.act_fn == "linear":
            A = linear(Z)
        elif self.act_fn == "softmax":
            A = softmax(Z)
            
        self.cache = X
        
        return out    

    def forward(self, X):

        m, n_C_prev, n_H_prev, n_W_prev = X.shape

        n_C = self.n_F
        n_H = int((n_H_prev + 2 * self.p - self.f)/ self.s) + 1
        n_W = int((n_W_prev + 2 * self.p - self.f)/ self.s) + 1
        
        X_col = im2col(X, self.f, self.f, self.s, self.p)
        w_col = self.W['val'].reshape((self.n_F, -1))
        b_col = self.b['val'].reshape(-1, 1)
        # Perform matrix multiplication.
        out = w_col @ X_col + b_col
        # Reshape back matrix to image.
        out = np.array(np.hsplit(out, m)).reshape((m, n_C, n_H, n_W))
        self.cache = X, X_col, w_col
        return out

    def backward(self, dout):

        X, X_col, w_col = self.cache
        m, _, _, _ = X.shape
        # Compute bias gradient.
        self.b['grad'] = np.sum(dout, axis=(0,2,3)) 
        # Reshape dout properly.
        dout = dout.reshape(dout.shape[0] * dout.shape[1], dout.shape[2] * dout.shape[3])
        dout = np.array(np.vsplit(dout, m))
        dout = np.concatenate(dout, axis=-1)
        # Perform matrix multiplication between reshaped dout and w_col to get dX_col.
        dX_col = w_col.T @ dout
        # Perform matrix multiplication between reshaped dout and X_col to get dW_col.
        dw_col = dout @ X_col.T
        # Reshape back to image (col2im).
        dX = col2im(dX_col, X.shape, self.f, self.f, self.s, self.p)
        # Reshape dw_col into dw.
        self.W['grad'] = dw_col.reshape((dw_col.shape[0], self.n_C, self.f, self.f)) 
                
        return dX, self.W['grad'], self.b['grad']

    def bprop_slow(self, dZ):
        (m, n_H_prev, n_W_prev, n_C_prev) = self.A_prev.shape
        
        dA_prev = np.zeros((m, n_H_prev, n_W_prev, n_C_prev))                           
        self.dW = np.zeros((self.f, self.f, n_C_prev, self.n_C))
        self.db = np.zeros((1, 1, 1, self.n_C))
        
        A_prev_pad = np.pad(self.A_prev, ((0, 0), (self.pad, self.pad), (self.pad, self.pad), (0, 0)), 'constant', constant_values=0)
        dA_prev_pad = np.pad(dA_prev, ((0, 0), (self.pad, self.pad), (self.pad, self.pad), (0, 0)), 'constant', constant_values=0)
    
        if self.act_fn == "sigmoid":
            dZ = derivative_sigmoid(dZ)
        elif self.act_fn == "tanh":
            dZ = derivative_tanh(dZ)
        elif self.act_fn == "relu":
            dZ = d_relu(dZ)
        elif self.act_fn == "linear":
            dZ = d_linear(dZ)    
    
        for i in range(m):                       # loop over the training examples
            
            # select ith training example from A_prev_pad and dA_prev_pad
            a_prev_pad = A_prev_pad[i]
            da_prev_pad = dA_prev_pad[i]
            
            for h in range(self.n_H):                   # loop over vertical axis of the output volume
                for w in range(self.n_W):               # loop over horizontal axis of the output volume
                    for c in range(self.n_C):           # loop over the channels of the output volume
                    
                        # Find the corners of the current "slice"
                        vert_start = h * self.stride
    
                        vert_end = vert_start + self.f
                        horiz_start = w * self.stride
    
                        horiz_end = horiz_start + self.f
                        
                        # Use the corners to define the slice from a_prev_pad
                        a_slice = a_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :]
    
                        # Update gradients for the window and the filter's parameters using the code formulas given above
                        da_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :] += self.W[:,:,:,c] * dZ[i, h, w, c]
                        self.dW[:,:,:,c] += a_slice * dZ[i, h, w, c]
                        self.db[:,:,:,c] += dZ[i, h, w, c]
                        
            dA_prev[i, :, :, :] = da_prev_pad[self.pad:-self.pad, self.pad:-self.pad, :]
        

        assert(dA_prev.shape == (m, n_H_prev, n_W_prev, n_C_prev))
        
        return dA_prev
