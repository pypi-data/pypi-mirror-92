import numpy as np

def sigmoid(Z):
    '''
        Calculate the sigmoid values and derivative of the sigmoid of the inputs :
        based on the formulas:
            A = 1/(1+e^(-Z))
            A_dash = A(1-A)
        Args:
            Z: a numpy array or matrix

        Return:
            A: The values of sigmoid of the input
            A_dash:The values of the derivative of the sigmoid related to the input
        
        Shape:
            - Input: Z (m, k) m: number of samples , k: number of neurons in current layer
            - Output: A(m, k),A_dash(m,k) m: number of samples , k: number of neurons in current layer

        Examples:
            result,result_der = sigmoid(np.array([4,1,-5,3]))
    '''
    A = np.divide(1,1+np.exp(-Z))
    A[np.isnan(A)] = 1e-10
    A_dash = np.multiply(A,1-A)
    A_dash[np.isnan(A_dash)] = 1e-10
    return A,A_dash

def tanh(Z):
    '''
        Calculate the tanh values and derivative of the tanh of the inputs :
        based on the formulas:
            A = (e^(Z)-e^(-Z))/(e^(Z)+e^(-Z))
            A_dash = 1-A^2
        Args:
            Z: a numpy array or matrix

        Return:
            A: The values of tanh of the input
            A_dash:The values of the derivative of the tanh related to the input
        
        Shape:
            - Input: Z (m, k) m: number of samples , k: number of neurons in current layer
            - Output: A(m, k),A_dash(m,k) m: number of samples , k: number of neurons in current layer

        Examples:
            result,result_der = tanh(np.array([4,1,-5,3]))
    '''
    A = np.tanh(Z)
    A[np.isnan(A)] = 1e-10
    A_dash = 1-np.power(A,2)
    return A,A_dash

def relu(Z):
    '''
        Calculate the relu values and derivative of the relu of the inputs :
        based on the formulas:
            A = Z if Z >= 0 otherwise 0 
            A_dash = 1 if Z >= 0 otherwise 0
        Args:
            Z: a numpy array or matrix

        Return:
            A: The values of relu of the input
            A_dash:The values of the derivative of the relu related to the input
        
        Shape:
            - Input: Z (m, k) m: number of samples , k: number of neurons in current layer
            - Output: A(m, k),A_dash(m,k) m: number of samples , k: number of neurons in current layer

        Examples:
            result,result_der = relu(np.array([4,1,-5,3]))
    '''
    A = Z*(Z >=0)
    A[np.isnan(A)] = 1e-10
    A_dash = 1.*(Z>=0)
    return A,A_dash

def softmax(Z):
    '''
        Calculate the softmax values and derivative of the softmax of the inputs :
        based on the formulas:
            A[i] = e^(Z[i])/sum(e^(Z[j])) j: from 1 to number of neruons in output layer
            A_dash = 1 , as it is included in the softmax loss function 
        Args:
            Z: a numpy array or matrix

        Return:
            A: The values of softmax of the input
            A_dash: 1
        
        Shape:
            - Input: Z (m, k) m: number of samples , k: number of neurons in current layer
            - Output: A(m, k),A_dash(m,k) m: number of samples , k: number of neurons in current layer

        Examples:
            result,result_der = softmax(np.array([4,1,-5,3]))
    '''
    A = np.exp(Z)
    A[np.isnan(A)] = 1e-10
    A = A/(np.sum(A,axis = 1,keepdims=True)+1e-10)
    A[np.isnan(A)] = 1e-10
    return A,1

def leakyrelu(Z):
    '''
        Calculate the leaky relu values and derivative of the leaky relu of the inputs :
        based on the formulas:
            A = Z if Z>= 0 otherwise Z*0.01
            A_dash = 1 if Z>= 0 otherwise 0.01
        Args:
            Z: a numpy array or matrix

        Return:
            A: The values of leaky relu of the input
            A_dash:The values of the derivative of the leaky relu related to the input
        
        Shape:
            - Input: Z (m, k) m: number of samples , k: number of neurons in current layer
            - Output: A(m, k),A_dash(m,k) m: number of samples , k: number of neurons in current layer

        Examples:
            result,result_der = leakyrelu(np.array([4,1,-5,3]))
    '''
    A = np.where(Z > 0, Z, Z * 0.01)
    A[np.isnan(A)] = 1e-10
    A_dash = Z
    A_dash[A_dash >= 0] = 1
    A_dash[A_dash < 0] = 0.01
    return A,A_dash

def identity(Z):
    '''
        Calculate the identity values and derivative of the identity of the inputs :
        based on the formulas:
            A = Z
            A_dash = 1
        Args:
            Z: a numpy array or matrix

        Return:
            A: The values of identity of the input
            A_dash:The values of the derivative of the identity related to the input
        
        Shape:
            - Input: Z (m, k) m: number of samples , k: number of neurons in current layer
            - Output: A(m, k),A_dash(m,k) m: number of samples , k: number of neurons in current layer

        Examples:
            result,result_der = identity(np.array([4,1,-5,3]))
    '''
    A = Z
    A[np.isnan(A)] = 1e-10
    A_dash = np.ones_like(A)
    return A,A_dash