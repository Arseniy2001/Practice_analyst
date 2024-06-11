# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 14:33:27 2020

@author: Alex
"""
import math
import keras
import tensorflow
import pandas_datareader

def Distanсe(list1, list2):
    return math.sqrt(sum((x-y)**2 for x,y in zip(list1,list2)))

def ListSplit(list, perc):
    index = int(len(list)*perc)
    return list[:index], list[index:]