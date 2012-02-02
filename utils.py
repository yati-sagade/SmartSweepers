'''
Created on Jan 23, 2012
utils.py
common utility functions
@author: yati
'''
import math
from random import random
#------------------------------------------------------------------------------ 
def sigmoid(a, p=1.0):
    '''
    The sigmoid response curve function.
    '''
    return (1.0 / (1 + math.exp(-a/p)))
#------------------------------------------------------------------------------ 
def clamped_rand():
    '''
    returns a random floating point number in [-1, 1]
    '''
    return random() - random()
#------------------------------------------------------------------------------ 
def clamp(x, low, hi):
    '''
    clamp a value too high or too low.
    ''' 
    ret = x
    if x < low:
        ret = low
    elif x > hi:
        ret = hi
    
    return ret
#------------------------------------------------------------------------------ 
INFINITY = math.tan(math.pi/2)
#------------------------------------------------------------------------------ 


    
    
    
        