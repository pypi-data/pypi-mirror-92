import numpy as np
import pandas as pd
import optimization as opt
import Activations as Act
import Losses as loss
from visualization import visualization as vis
from save_load import import_saved_weights,save_weights
import PIL, shutil, os


# encapsulate Layers parameters
class Layer:
    def __init__(self,size,activation='Identity'):
        '''
        Create a Layer with a specific size and activation function:

        Args:
            size: a tuble holds (input size, neuran count) respectively
            activation: specify the applied activation function on layer
                    avliable activations:
                        -Identity
                        -ReLU
                        -Sigmoid 
                        -Tanh 
                        -Softmax
                    Default: Identity

        Shape:
            - Input: size (N, m) N: number of features
            - Output: None

        Examples:
            layer1 = nn.Layer(size=(3,5), activation='ReLU')

        '''

        # check if the size forms of a tuple and activation as a string
        assert(type(size) == tuple)
        assert(type(activation) == str)

        self.inSize = size[0]
        self.outSize = size[1]
        # initialize weights and biases
        # weight of size (layer neurans no. , prev layer neurans no.)
        self.weights = np.random.randn(self.outSize,self.inSize) * np.sqrt( 2/(self.inSize+self.outSize) )
        # self.weights = np.random.randn(self.outSize,self.inSize)*0.01
        self.bias = np.zeros((1,self.outSize))

        # initialize weights and biases gradient
        self.weights_Grad = np.zeros_like(self.weights)
        self.bias_Grad = np.zeros_like(self.bias)

        # initialize A, Adash and Z where
        # Z:        linear output of layer
        # A:        layer output after activation 
        # Adash:   derivative of the layer output after activation
        self.Z = np.zeros_like(self.bias)
        self.A = np.zeros_like(self.bias)
        self.Adash = np.zeros_like(self.bias)

        self.activation = str.lower(activation)
    def forward(self,inputs):
        '''
        Calculate a forward propagation step:
        based on the Linear formula:
            Y = activation(X.W + b)

        Args:
            inputs: a numpy array with the previous layer values (or the network inputs)

        Return:
            a forward propagation step value after applying activation function

        Shape:
            - Input: inputs (1, N) N: number of features
            - Output: (1, m)

        Examples:
            layer = nn.Layer(size=(3,5), activation='ReLU')
            result = layer.forward(np.array([4,1,-5,3]))
        '''
        
        assert(type(inputs) == np.ndarray)
        assert(inputs.shape[1] == self.inSize)

        # linear w*x + b forward propagtion step
        self.Z = np.dot(inputs,self.weights.T) + self.bias
        # evaluate the results after the activation
        self.A, self.Adash = eval(f"Act.{self.activation}(Z = self.Z)")
        return self.A
        
    def __call__(self,inputs):
        '''
        Calculate a forward propagation step over one layer:
        based on the Linear formula:
            Y = activation(X.W + b)

        Args:
            inputs: a numpy array with the previous layer values (or the network inputs)

        Return:
            a forward propagation step value after applying activation function

        Shape:
            - Input: inputs (1, N) N: number of features
            - Output: (1, m)

        Examples:
            layer = nn.Layer(size=(3,5), activation='ReLU')
            result = layer(np.array([4,1,-5,3]))

        '''
        return self.forward(inputs)


# model class encapsulates Layers objects
class Model:
    def __init__(self,*layers):
        '''
        Create a Model with a specific number and type of Layers:

        Args:
            layers: multi-valued parameter that holds one or more Layer object

        Shape:
            - layers: (nn.Layer(N,m), nn.Layer(m,k), .... , nn.Layer(c,1))
            - Output: None

        Examples:
            model = nn.Model(
                Layer(size=(3,5), activation='ReLU'),
                Layer(size=(5,10), activation='ReLU'),
                Layer(size=(10,6), activation='ReLU'),
                Layer(size=(6,1), activation='ReLU')
                )

        '''

        assert(type(layers) == tuple)
        assert(type(layer) == "nn.Layer" for layer in layers)
        self.x = None
        self.y = None
        self.layers = list(layers)
    
    def forward(self,inputs):
        '''
        Calculate a forward propagation step over the whole model:
        based on the Linear formula:
            A = activation(Layer(x))
            B = activation(Layer(A))
            .
            .
            .
            Y = activation(Layer(F))

        Args:
            inputs: a numpy array with the network inputs

        Return:
            a forward propagation iteration value for the whole network
        
        Shape:
            - Input: inputs (1, N) N: number of features
            - Output: (1, m) m: number of nurans at output

        Examples:
            model = nn.Model(
                Layer(size=(3,5), activation='ReLU'),
                Layer(size=(5,1), activation='ReLU')
            )
            model.forward(np.array([1,6,-2]))
        '''
        
        assert(type(inputs) == np.ndarray)

        self.x = inputs
        for layer in self.layers:
            inputs = layer.forward(inputs)
        self.y = inputs
        return self.y

    def __call__(self,inputs):
        '''
        Calculate a forward propagation step over the whole model:
        based on the Linear formula:
            A = activation(Layer(x))
            B = activation(Layer(A))
            .
            .
            .
            Y = activation(Layer(F))

        Args:
            inputs: a numpy array with the network inputs

        Return:
            a forward propagation iteration value for the whole network
        
        Shape:
            - Input:  inputs (1, N) N: number of features
            - Output: (1, m) m: number of nurans at output

        Examples:
            model = nn.Model(
                Layer(size=(3,5), activation='ReLU'),
                Layer(size=(5,1), activation='ReLU')
            )
            model(np.array([1,6,-2]))
        '''

        return self.forward(inputs)


    def fit(self,dataset_input,label,optimization_type,loss_type,alpha,epoch,batch_size = 0 ,graph_on = False):
        '''
        Executing the learning process for a given dataset:
        Args:
            dataset_input: a numpy array with source inputs
            label: a numpy array with correct label for each example
            optimization_type: a string indicates the required learning optmization type
            loss_type: a string indicates the required output loss function to use
            alpha: a float number indicates the required learning rate
            epoch: an integer number required for number of iterations in learning process
            graph_on: a boolean typed value to visualize the process
        
        Return:
            None
        
        Shape:
            The shape has no changes, it just changes the current values for learning

        Examples:
            model.fit(X_train,label_train,'SGD','MSE',alpha = 0.0001,epoch = 50,graph_on = True)
        '''

        if(graph_on):
            self.graph = vis()
            if not os.path.exists('Loss'):
                os.mkdir("Loss")
        if len(label.shape) == 1:
            label = label.reshape(-1,1)
        if label.shape[1] == 1 and self.layers[-1].outSize != 1:
            tmp = np.zeros((dataset_input.shape[0],self.layers[-1].outSize))
            rows = np.arange(start = 0,stop = dataset_input.shape[0],step =1)
            label = np.squeeze(label)
            tmp[rows,label] = 1
            label = tmp
        counter = 0
        if(optimization_type == 'SGD'):
            while(True):
                counter += 1
                loss_acc = 0
                opt.init_delta(self)                                    
                for i in range(len(dataset_input)):
                    self.forward(dataset_input[i].reshape(1,-1))
                    loss_value , dloss =eval("loss."+str.lower(loss_type)+"(A = self.y , Y = label[i].reshape(1,-1))")
                    loss_acc += loss_value
                    opt.sgd(self,alpha,dataset_input[i].reshape(1,-1),dloss,len(dataset_input))
                if(graph_on):
                    self.graph.add_point_to_graph(loss_acc/len(dataset_input),counter,epoch)
                print(f"epoch: {counter},    Loss = {loss_acc/len(dataset_input)}")
                if(counter == epoch):
                    if(graph_on):
                        im = PIL.Image.open("Loss/0.png")
                        im.save('Loss.gif', save_all=True, append_images=[PIL.Image.open(f"Loss/{i}.png") for i in range(0,epoch)])
                        shutil.rmtree("Loss")
                    break
          #-------------------------------------------      
        elif(optimization_type == 'batch'):
              while(True):
                counter += 1
                loss_acc = 0
                opt.init_delta(self)
                for i in range(len(dataset_input)):
                    self.forward(dataset_input[i].reshape(1,-1))
                    loss_value , dloss = eval("loss."+str.lower(loss_type)+"(A = self.y , Y = label[i].reshape(1,-1))")
                    loss_acc += loss_value
                    opt.batch(self,dataset_input[i].reshape(1,-1),dloss)
                opt.update_weights_bias(self,alpha,len(dataset_input))
                if(graph_on):
                    self.graph.add_point_to_graph(loss_acc/len(dataset_input),counter,epoch)
                print(f"epoch: {counter},    Loss = {loss_acc/len(dataset_input)}")
                if(counter == epoch):
                    if(graph_on):
                        im = PIL.Image.open("Loss/0.png")
                        im.save('Loss.gif', save_all=True, append_images=[PIL.Image.open(f"Loss/{i}.png") for i in range(0,epoch)])
                        shutil.rmtree("Loss")
                    break
        #-------------------------------------------      
        elif(optimization_type == 'minibatch'):
            while(True):
                counter += 1
                loss_acc = 0
                opt.init_delta(self)
                for i in range(len(dataset_input)):
                    self.forward(dataset_input[i].reshape(1,-1))
                    loss_value , dloss = eval("loss."+str.lower(loss_type)+"(A = self.y , Y = label[i].reshape(1,-1))")
                    loss_acc += loss_value
                    opt.batch(self,dataset_input[i].reshape(1,-1),dloss)
                    if(i%batch_size == 0 or i == len(dataset_input)-1):
                        if(i != len(dataset_input)-1):
                            opt.init_delta(self)
                        opt.update_weights_bias(self,alpha,batch_size)                        
                if(graph_on):
                    self.graph.add_point_to_graph(loss_acc)
                print(f"epoch: {counter},    Loss = {loss_acc/len(dataset_input)}")
                if(counter == epoch):
                    if(graph_on):
                        im = PIL.Image.open("Loss/0.png")
                        im.save('Loss.gif', save_all=True, append_images=[PIL.Image.open(f"Loss/{i}.png") for i in range(0,epoch)])
                        shutil.rmtree("Loss")
                    break
                
            

    def evaluate(self,x,y,metric='Accuracy'):
        '''
        Calculate the evaluation matrices for the testing dataset
 
        Args:
            test_x: a numpy array with the network testing inputs
            test_y: a numpy array with the network testing true labels
            metric: metric name(s) as string or list of strings:
                    avliable metrics:
                        - Accuracy
                        - Confusion matrix
                        - Precision
                        - Recall
                        - F1 score
                Default: Accuracy
 
        Shape:
            - Input:
                test_x (K, N) K:number of testing samples, N: number of features
                test_y (K, m) K:number of testing samples, m: number of nurans at output
            - Output:
                the specified metric value(s)
                beside storing all metrics in model variables as follows:
                    self.accuracy [0-1] value
                    self.confusion_matrix (2,2) matrix
                    self.recall  [0-1] value
                    self.precision [0-1] value
                    self.f1_score [0-1] value
        Examples:
            P,R,F1 = model.evaluate(
                        np.array([[1,6,-2],[3,9,12],[7,-3,4]]),
                        np.array([[0],[1],[1]]),
                        metric=['Precision','Recall','F1_score']
                    )
        '''
        def HotForm(y,k):
            out = np.zeros((len(y),k))
            for i,e in enumerate(y):
                out[i][e] = 1
            return out
 
        assert(type(x) == np.ndarray)
        assert(type(y) == np.ndarray)
        assert(type(metric) == str or type(metric) == list)
 
        k = self.layers[-1].outSize
 
        # propagate in forward iteration over testing data
        y_tmp = self.forward(x)
        y_hat = np.array([np.argmax(t) for t in y_tmp])
 
        # convert a vector into a hot form
 
        TP = np.zeros((k))
        TN = np.zeros((k))
        FP = np.zeros((k))
        FN = np.zeros((k))
        y_hot = HotForm(y,k)
        y_hat_hot = HotForm(y_hat,k)
 
        for i in range(len(y)):
            for j in range(k):
                    TP[j] += (y_hot[i][j] == 1 and y_hat_hot[i][j] == 1)
                    FP[j] += (y_hot[i][j] == 0 and  y_hat_hot[i][j] == 1)
                    FN[j] += (y_hot[i][j] == 1 and  y_hat_hot[i][j] == 0)
                    TN[j] += (y_hot[i][j] == 0 and  y_hat_hot[i][j] == 0)
 
        percision = TP/(TP+FP+1e-9)
        recall = TP/(TP+FN+1e-9)
        f1_score = np.mean(2*(percision*recall)/(percision+recall+1e-9))
        percision = np.mean(percision)
        recall = np.mean(recall)
 
        confusion_matrix = np.zeros((k,k))
        for i,d in enumerate(y):
            confusion_matrix[y_hat[i],d] += 1
 
        accuracy = np.diag(confusion_matrix).sum()/confusion_matrix.sum()
 
        # return the targeted metric(s) 
        if type(metric) == str:
            metric = [metric]
        out = list()
        for m in metric:
            out.append(eval('_'.join(list(filter(lambda w: w != "" , str.lower(m).split(" "))))))
        return out

    def save(self,path = "model.NND"):
        '''
        Save model Object on Disk

        Args:
            Path to the model to be saved
                Default: "model.NND"

        Shape:
            - Input:
                path: string
            - Output:
                None
        Examples:
            model.save("my model.NND")
        '''
        save_weights(self,path)


def load(path):
    '''
    Import loaded model from Disk

    Args:
        Path to the model to be saved

    Shape:
        - Input:
            path: string
        - Output:
            model object loaded
    Examples:
        model = nn.load("my model.NND")
    '''
    return import_saved_weights(path)