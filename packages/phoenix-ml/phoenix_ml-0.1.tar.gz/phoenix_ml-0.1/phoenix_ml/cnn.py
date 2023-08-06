from init import X_train, Y_train, X_test, Y_test 
import numpy as np
import matplotlib.pyplot as plt
import math
def zero_pad(X, pad):
    X_pad = np.pad(X, ((0,0), (pad, pad), (pad, pad), (0,0)), mode='constant', constant_values = (0,0))
    return X_pad

def conv_single_step(a_slice_prev, W, b):

    s = np.multiply(a_slice_prev, W)
    Z = np.sum(s)
    Z = Z + float(b)
    return Z

def conv(A_prev, W, b, stride,pad):
    (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape[0], A_prev.shape[1], A_prev.shape[2], A_prev.shape[3]
    (f, f, n_C_prev, n_C) = W.shape[0], W.shape[1], W.shape[2], W.shape[3] 
    n_H = int(int(n_H_prev + 2*pad - f)/stride + 1)
    n_W = int(int(n_W_prev + 2*pad - f)/stride + 1)
    Z = np.zeros([m, n_H, n_W, n_C])
    A_prev_pad = zero_pad(A_prev, pad)
    
    for i in range(m):                  
        a_prev_pad = A_prev_pad[i]      
        for h in range(n_H):           
            vert_start = stride * h
            vert_end = vert_start + f
            
            for w in range(n_W):       
              
                horiz_start = stride * w
                horiz_end = horiz_start + f
                
                for c in range(n_C):   
               
                    a_slice_prev = A_prev_pad[i, vert_start:vert_end, horiz_start:horiz_end, :]
                  
                    weights = W[:, :, :, c]
                    biases = b[:, :, :, c]
                    Z[i, h, w, c] = conv_single_step(a_slice_prev, weights, biases)
   
    assert(Z.shape == (m, n_H, n_W, n_C))
    
    return Z

def pool(A_prev, f,stride, mode = "max"):
    
    (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape
    
    n_H = int(1 + (n_H_prev - f) / stride)
    n_W = int(1 + (n_W_prev - f) / stride)
    n_C = n_C_prev
    
    A = np.zeros((m, n_H, n_W, n_C))              
    
    for i in range(m):                         
        for h in range(n_H):                     
            vert_start = stride * h 
            vert_end = vert_start + f
            
            for w in range(n_W):                 
                horiz_start = stride * w
                horiz_end = horiz_start + f
                
                for c in range (n_C):            
                    
                    a_prev_slice = A_prev[i]
                    
                    if mode == "max":
                        A[i, h, w, c] = np.max(a_prev_slice[vert_start:vert_end, horiz_start:horiz_end, c])
                    elif mode == "average":
                        A[i, h, w, c] = np.mean(a_prev_slice[vert_start:vert_end, horiz_start:horiz_end, c])
    
    
    return A
#w1=np.array([[1, 1,1],[0, 0,0], [-1,-1,-1]])
#w1=np.reshape(w1,(3,3,1,1))
#x =np.array([[10,10,10,0,0,0],[10,10,10,0,0,0],[10,10,10,0,0,0],[0,0,0,10,10,10],[0,0,0,10,10,10],[0,0,0,10,10,10]])
#x=np.reshape(x,(1,6,6,1))
#print(x)
#b=np.array([[0]])
#b=np.reshape(b,(1,1,1,1))
#A=  conv(x, w1, b,1,0)
#A.reshape(A.shape[0],-1)
A=np.array([[1,3,2,1],[2,9,1,1],[1,3,2,3],[5,6,1,2]])
A=np.reshape(A,(1,4,4,1))
A=pool(A, 2,2)
print(A)
A=A.reshape(2,2)
print(A)


#print(w1.shape)
#print (X_train.shape[0])
#print(X_train.shape[1])
#first=int(math.sqrt(X_train.shape[1]))
#print (X_train[1][:])
#print (X_train.shape[0])
#print (X_train.shape[1])
#X_train=X_train.reshape(X_train.shape[0],first,first,1) 
#print (X_train.shape[0])
#print (X_train.shape[1])
#print (X_train.shape[2])
#print (X_train.shape[3])
#print (X_train[:][:][:][1])
#b=np.array([[1]])
#b=np.reshape(b,(1,1,1,1))
#A=  conv(X_train, w1, b,4,0)
#A=pool(A, 2,2)
#print (X_train[:][:][:][1])

#second=A.shape[1]
#print(A.shape[0])
#print(A.shape[1])
#print(A.shape[2])
#print(A.shape[3])
#x_train =X_train.reshape(X_train.shape[0],-1)
#X_train = X_train . reshape (  X_train.shape[0] , second*second )
#print(X_train.shape[0])
#print(X_train.shape[1])

