import numpy as np
import pickle

def save_weights(model,path,csv_on= False):
    
    '''
        saves 2d array into csv file:
        Args:
            layer_arr: a 2d array holds numbers
        Shape:
            - Input: layer_arr (N, m) N: number of weights
            - Output: None
        Examples:
            save_weights(np.array([[1,2,3,4,56,9,7],[3,4,6,7,8]]))
        '''
    if csv_on:
        f = open('saved_weights.csv', 'w')
        for layer in model:
            f.write(",".join(str(x) for x in layer) + "\n")
    else:
        pickle.dump(model,open(path,'wb'))

def import_saved_weights(path,csv_on= False):
    
    '''
        import 2d array from csv file:
        Args: None
        Shape:
            - Input: None
            - Output: layer_arr (N, m) N: number of weights
        Examples:
            import_saved_weights()
    '''    
    if csv_on:
        all_of_the_weights = open(path, 'r').read()
        lines = all_of_the_weights.split('\n')
        layer_arr = []
        for line in lines:
            if len(line) > 1:
                x = line.split(',')
                xx = np.array(x)
                y = xx.astype(np.float)
                layer_arr.append(y)
        return layer_arr
    else:
        return pickle.load(open(path,'rb'))