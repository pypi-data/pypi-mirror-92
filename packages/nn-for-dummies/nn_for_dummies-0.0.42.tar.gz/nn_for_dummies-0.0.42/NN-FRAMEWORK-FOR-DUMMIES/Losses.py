import numpy as np

def mse(A,Y):
    '''
        Calculate the mean square loss and derivative of the mean sqaure loss between label and prediction :
        based on the formulas:
            Loss = (1/2m)*(sum((A-Y)^2))
            Loss_dash = (1/m)* (A-Y)
        Args:
            A: the activation output of the output layer
            Y: labels of the examples

        Return:
            Loss: The values of loss of the inputs
            Loss_dash:The values of the derivative of the loss related to the inputs
        
        Shape:
            - Input: A (m, k) m: number of samples , k: number of neurons in current layer,
                     Y (m, k) m: number of samples , k: number of neurons in current layer
            - Output: Loss,Loss_dash(m,k) m: number of samples , k: number of neurons in current layer

        Examples:
            result,result_der = mse(np.array([4,1,-5,3]),np.array([0,0,1,0]))
    '''
    m = A.shape[0]
    Loss = (1/(2*m))*np.sum(np.power(A-Y,2))
    Loss_dash = np.multiply((1/m),A-Y)
    return Loss,Loss_dash

def nll(A,Y):
    '''
        Calculate the negative log likelihood loss and derivative of negative log likelihood loss between label and prediction :
        based on the formulas:
            Loss = -log(prediction[yi]),yi is the index of the correct label
            Loss_dash = -1/Y
        Args:
            A: the activation output of the output layer
            Y: labels of the examples

        Return:
            Loss: The values of loss of the inputs
            Loss_dash:The values of the derivative of the loss related to the inputs
        
        Shape:
            - Input: A (m, k) m: number of samples , k: number of neurons in current layer,
                     Y (m, k) m: number of samples , k: number of neurons in current layer
            - Output: Loss,Loss_dash(m,k) m: number of samples , k: number of neurons in current layer

        Examples:
            result,result_der = nll(np.array([4,1,-5,3]),np.array([0,0,1,0]))
    '''
    Loss  = np.sum(-np.log(np.sum(np.multiply(A,Y),axis = 1,keepdims=True)))
    Loss_dash = np.divide(-1,Y)
    return Loss, Loss_dash

def l1(A,Y):
    '''
        Calculate the mean absolute loss and derivative of the mean absolute loss between label and prediction :
        based on the formulas:
            Loss = (1/m)*sum(|A-Y|)
            Loss_dash = 1 if A-Y > 0 otherwise -1
        Args:
            A: the activation output of the output layer
            Y: labels of the examples

        Return:
            Loss: The values of loss of the inputs
            Loss_dash:The values of the derivative of the loss related to the inputs
        
        Shape:
            - Input: A (m, k) m: number of samples , k: number of neurons in current layer,
                     Y (m, k) m: number of samples , k: number of neurons in current layer
            - Output: Loss,Loss_dash(m,k) m: number of samples , k: number of neurons in current layer

        Examples:
            result,result_der = l1(np.array([4,1,-5,3]),np.array([0,0,1,0]))
    '''
    m = A.shape[0]
    Loss = (1/(m))*np.sum(np.abs(A-Y))
    vf =  np.vectorize(lambda x: 1 if x > 0 else -1)
    Loss_dash = (1/(m))*vf(A-Y)
    return Loss,Loss_dash

def softmax(A,Y):
    '''
        Calculate the softmax loss and derivative of the softmax between label and prediction :
        based on the formulas:
            Loss = -log(prediction[yi]),yi is the index of the correct label
            Loss_dash[r] = -(1-yi) if r= yi otherwise yi
        Args:
            A: the activation output of the output layer
            Y: labels of the examples

        Return:
            Loss: The values of loss of the inputs
            Loss_dash:The values of the derivative of the loss related to the inputs
        
        Shape:
            - Input: A (m, k) m: number of samples , k: number of neurons in current layer,
                     Y (m, k) m: number of samples , k: number of neurons in current layer
            - Output: Loss,Loss_dash(m,k) m: number of samples , k: number of neurons in current layer

        Examples:
            result,result_der = softmax(np.array([4,1,-5,3]),np.array([0,0,1,0]))
    '''
    y = np.argmax(Y,axis = 1)
    Loss = -np.log([(A[i, y[i]]+1e-10) for i in range(len(A))])
    Loss[np.isnan(Loss)] = 1e-10
    Loss = np.mean(Loss)
    Loss_dash = (A - Y)/float(len(A))
    Loss_dash[np.isnan(Loss_dash)] = 1e-10
    return Loss,Loss_dash

