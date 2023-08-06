# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 17:21:12 2021

@author: Mohamed Amr
"""

import pandas as pd
import math

class DataPreProcessing:
    
    def get_data(path, label_path = "", shuffle = False):
        '''
        Used to get feature matrix and label vector out of les.
        The feature matrix is a numpy array with dimensions (N X D), where N: number
        of samples and D: number of features in every sample.
        The label vector is a numpy array with dimensions (N X 1), where N: number
        of samples.

        • Parameters:
            1. path: {'string'} The path of the file that contains the features and
            labels.
            2. label path: {'string'} The path of labels file if label is not included
            in first path.
            3. shuffe: {'bool'} If True the rows will be rearranged randomly.
        • Return: {'tuple'} of 2 items
            1. Feature Matrix: {'numpy.array'}
            2. Label Vector: {'numpy.array'}
        • Limitations
            1. You must input label path if there are no labels data in first path.
            2. Label column name must be 'Label' and can't be anything else.
            '''
        df = pd.read_csv(path)
        df.columns = df.columns.map(str.lower)
        if(label_path != ""):
            df_temp = pd.read_csv(label_path)
            df_temp.columns = df_temp.columns.map(str.lower)
            df['label'] = df_temp['label']
        if(shuffle):
            df = df.sample(frac = 1)
        X = df.loc[:, df.columns != 'label'].to_numpy()
        label = df['label'].to_numpy()
        return (X, label)
        
    def normalize(matrix):
        '''
        Used to normalize input matrix, The returned matrix has the same dimen-
        sions as the input.
        • Parameters
            1. matrix: {'numpy.array'} Unormalized matrix.
        • Return: {'numpy.array'} normalized matrix.
        '''
        mean = matrix.mean()
        variance = matrix.var()
        return (matrix - mean)/math.sqrt(variance+0.0000001)
        
    def split_data(X, label):
        '''
        Used to split data into training data set with it's training labels and test
        data set with it's test labels.
        The data is split with splitting ratio 75% training data and 25% testing data.
        • Parameters
            1. X: {'numpy.array'} The feature matrix.
            2. label: {'numpy.array'} The labels vector.
        • Return: f'tuple'g of 4 items
            1. Training Feature Matrix: {'numpy.array'}
            2. Test Feature Matrix: {'numpy.array'}
            3. Training Label vector: {'numpy.array'}
            4. Test Label Vector: {'numpy.array'}
        '''
        ratio = int(len(label)*0.75)
        X_train = X[:ratio]
        X_test = X[ratio:]
        label_train = label[:ratio]
        label_test = label[ratio:]
        return (X_train, X_test, label_train, label_test)
    
################################################################################
        
#test cases:
#-----------
    
#data  = DataPreProcessing()
#X     = data.get_X('C:/Users/Mohamed Amr/Documents/Computer & Systems Engineering/4th CSE/First Term/Neural Networks/digit-recognizer/train.csv')
#label = data.get_label('C:/Users/Mohamed Amr/Documents/Computer & Systems Engineering/4th CSE/First Term/Neural Networks/digit-recognizer/train.csv')

# X, label = DataPreProcessing.get_data("C:/Users/Mohamed Amr/Documents/Computer & Systems Engineering/4th CSE/First Term/Neural Networks/digit-recognizer/train.csv", shuffle = True)
# X_train, X_test, label_train, label_test = DataPreProcessing.split_data(X, label)
# print("X_train: {}, Label_train: {}, X_test: {}, Label_test: {}".format(X_train.shape, X_test.shape, label_train.shape, label_test.shape))
# print(DataPreProcessing.normalize(X))
