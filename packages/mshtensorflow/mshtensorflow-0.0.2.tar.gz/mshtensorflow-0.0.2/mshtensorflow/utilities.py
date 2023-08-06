# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 04:01:48 2021

@author: Adham
"""
from .Model import model 
import numpy as np
import pickle

def hot_one(labels, num_classes):
    num_of_examples = labels.shape[0]
    hot_one = np.zeros((num_classes, num_of_examples))
    for i in range(num_of_examples):
        hot_one [int(labels[i])] [i] = 1
    return hot_one

def store(Model, filename):
    if not filename.endswith(".dat"): 
        filename+=".dat"        
    with open('models\\'+filename, "wb") as f:
        pickle.dump(Model.getParams(), f)

def load(filename):
    Model = model()
    if not filename.endswith(".dat"): 
        filename+=".dat"        
    try:
        with open('models\\'+filename,"rb") as f:
            layers = pickle.load(f)
            Model.setParams(layers)
    except:
        try:
            with open(filename,"rb") as f:
                layers = pickle.load(f)
                Model.setParams(layers)
        except:
            print ("file not found")
      
    return Model