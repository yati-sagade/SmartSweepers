'''
Created on Jan 23, 2012

@author: yati
'''
import math
from random import random

def sigmoid(a, p=1.0):
    return (1.0 / (1 + math.exp(-a/p)))

def clamped_rand():
    return random() - random()

def clamp(x, low, hi):
    ret = x
    if x < low:
        ret = low
    elif x > hi:
        ret = hi
    
    return ret

    

INFINITY = math.tan(math.pi/2)


    
    
    
        