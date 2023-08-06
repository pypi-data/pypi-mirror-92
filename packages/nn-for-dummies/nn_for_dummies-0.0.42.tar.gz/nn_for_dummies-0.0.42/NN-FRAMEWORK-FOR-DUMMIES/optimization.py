'''
date:23 january
Author: mohamed emad and mohamed amr mansi
'''
import numpy as np
def sgd(model,alpha,sample,dloss,size):
    '''
        makes one iteration on the given model using online optimization:
        based on the Linear formula:
            dl/dweights = d(loss)/d(activation_function n) * d(activation_function n)/d(prediction n) 
                * d(prediction n)/d(Input n) ........* d(activation_function 1)/d(prediction 1)* d(prediction 1)/d(Input_dataset)

        Args:
            -model : the structured model to be trained
            -alpha : the learning rate
            -sample: One sample from the dataset
            -dloss : drivative of the loss function by the activation function of the last layer 

        Return:
           -the function updates the weights and biases of the layers but doesn't return any thing
        
        Shape:
            - model:  object from the model class
            - alpha: scalar value
            - sample: np.array of shape(1 x number of features)
            - dloss:  np.array of shape( the same shape of the weights of the last layer)
        Examples:
            sgd(model , 0.1 , np.array([1 , 2 , 3 , 4]) , np.array([6])) '''
    for i in range(len(model.layers)):
         n = len(model.layers) - i -1
         if(i == 0): #output layer ==> there is no saved drivative value
             dloss_dact = dloss            
             dl_dw=np.dot(np.multiply(np.transpose(dloss_dact) ,np.transpose(model.layers[n].Adash)),model.layers[n-1].A)
             model.layers[n].weights_Grad += dl_dw
             dl_db=np.multiply(np.transpose(dloss_dact) ,np.transpose(model.layers[n].Adash))
             model.layers[n].bias_Grad += np.transpose(dl_db)
             saved_drevative = np.dot(model.layers[n].weights.transpose(),dl_db)
         else:       #hidden layers
             dactivation = np.multiply(saved_drevative ,np.transpose(model.layers[n].Adash))
             if(n == 0):
                 dl_dw=np.dot(dactivation,sample)
             else:
                 dl_dw=np.dot(dactivation,model.layers[n-1].A)
             model.layers[n].weights_Grad += dl_dw
             dl_db=dactivation
             model.layers[n].bias_Grad += np.transpose(dl_db)             
             saved_drevative = np.dot(model.layers[n].weights.transpose(),saved_drevative)        
         model.layers[n].weights=model.layers[n].weights-alpha*dl_dw/size
         model.layers[n].bias=model.layers[n].bias-alpha*np.transpose(dl_db)/size
         #print(n , model.layers[n].weights)
        
def batch(model,sample,dloss):
    '''
        makes one iteration on the given model using batch optimization:
        based on the Linear formula:
            dl/dweights = d(loss)/d(activation_function n) * d(activation_function n)/d(prediction n) 
                * d(prediction n)/d(Input n) ........* d(activation_function 1)/d(prediction 1)* d(prediction 1)/d(Input_dataset)

        Args:
            -model : the structured model to be trained
            -sample: One sample from the dataset
            -dloss : drivative of the loss function by the activation function of the last layer 

        Return:
           -the function accumilates the gredient of the loss wrt. weights and biases 
        
        Shape:
            - model:  object from the model class
            - sample: np.array of shape(1 x number of features)
            - dloss:  np.array of shape( the same shape of the weights of the last layer)
        Examples:
            batch(model , np.array([1 , 2 , 3 , 4]) , np.array([6])) '''    
    
    for i in range(len(model.layers)):
        n = len(model.layers) - i -1
        if(i == 0): #output layer ==> there is no saved drivative value
            dloss_dact = dloss            
            dl_dw=np.dot(np.multiply(np.transpose(dloss_dact) ,np.transpose(model.layers[n].Adash)),model.layers[n-1].A)
            model.layers[n].weights_Grad += dl_dw
            dl_db=np.multiply(np.transpose(dloss_dact),np.transpose(model.layers[n].Adash))
            model.layers[n].bias_Grad += np.transpose(dl_db)
            saved_drevative = np.dot(model.layers[n].weights.transpose(),dl_db)
        else:       #hidden layers
            dactivation = np.multiply(saved_drevative ,np.transpose(model.layers[n].Adash))
            if(n == 0):
                dl_dw=np.dot(dactivation,sample)
            else:
                dl_dw=np.dot(dactivation,model.layers[n-1].A)
            model.layers[n].weights_Grad += dl_dw
            dl_db=dactivation
            model.layers[n].bias_Grad += np.transpose(dl_db)             
            saved_drevative = np.dot(model.layers[n].weights.transpose(),saved_drevative)


def norm(model, size_of_dataset):
    '''
    this function used in the FIT function to get the  norm of the LASTLAYER to campere to eipslon  to
    stop the  while loop
    Args:
        model: to get from it the weights_Grad(delta)  of each layer
        size_of_dataset: length of dateset to make normaliztion to data

    Returns: void

    '''
    norms_weights = 0.0
    norms_bias = 0.0
    norms_weights = np.linalg.norm(model.layers[len(model.layers)-1].weights_Grad / size_of_dataset)
    norms_bias = np.linalg.norm(model.layers[len(model.layers)-1].bias_Grad / size_of_dataset)
# =============================================================================
#     for i in range(len(model.layers)):
#         norms_weights += np.linalg.norm(model.layers[i].weights_Grad / size_of_dataset)
#         norms_bias += np.linalg.norm(model.layers[i].bias_Grad / size_of_dataset)
# =============================================================================
    return norms_weights + norms_bias


def init_delta(model):
    '''
    in this function  i make zeros of all weights_Grad(delta) matrix in begin of
     optimations of every layer
    Args:
        model: to get from it the weights_Grad(delta) of each layer

    Returns:void

    '''
    for i in range(len(model.layers)):
        model.layers[i].weights_Grad = np.zeros_like(model.layers[i].weights_Grad)
        model.layers[i].bias_Grad = np.zeros_like(model.layers[i].bias_Grad)


def update_weights_bias(model, alpha, size_of_dataset):
    '''
     tis function is rule  to update  weights of each layer  according to that rule --> Wi+1=Wi-Alpha*gard
    Args:
        model:to get from it the weights_Grad(delta) and weights  of each layer
        alpha:Constant ->> learing Constant
        size_of_dataset:length of date set

    Returns:Void

    '''
    for i in range(len(model.layers)):
        model.layers[i].weights = model.layers[i].weights - alpha * (model.layers[i].weights_Grad / size_of_dataset)
        model.layers[i].bias = model.layers[i].bias - alpha * (model.layers[i].bias_Grad / size_of_dataset)
