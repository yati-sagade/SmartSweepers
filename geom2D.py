'''
Created on Jan 25, 2012

@author: yati
'''
import math
import copy
from math import sin, cos
#------------------------------------------------------------------------------ 
class Matrix2D(list):
    '''
    small, compact matrix class that implements the things needed for basic
    rendering.
    '''
    class MatrixError(Exception):
        pass
    
    def __init__(self, data):
        self.num_rows = len(data)
        self.num_cols = len(data[0])
        for row in data:
            self.append([copy.copy(item) for item in row])
    
    def is_compatible_with(self, other):
        return self.num_cols == other.num_rows
        
    def __mul__(self, other):
        if not self.is_compatible_with(other):
            raise self.MatrixError("Incompatible matrices")
        
        result = []
        for i in xrange(self.num_rows):
            result.append([])
            for j in xrange(other.num_cols):
                result[i].append(0)
                for k in xrange(self.num_cols):
                    result[i][j] += self[i][k] * other[k][j]
        
        return self.__class__(result)
    
#------------------------------------------------------------------------------ 
class Vector2D(object):
    '''
    A simple 2D vector class.
    '''
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        
    # Now, some operator overloading
    def __add__(self, another):
        '''
        vector addition
        '''
        return self.__class__(self.x + another.x, self.y + another.y)
    
    def __sub__(self, another):
        '''
        subtraction of two vectors
        '''
        return self.__class__(self.x - another.x, self.y - another.y)
    
    def __mul__(self, rhs):
        '''
        noncommutative multiplication with a scalar - the scalar must appear
        on the right hand side.
        '''
        return self.__class__(self.x * rhs, self.y * rhs)
    
    def __div__(self, rhs):
        '''
        overload the division operator '/' for division by a scalar
        '''
        return self.__class__(self.x / rhs, self.y / rhs)
    
    def length(self):
        '''
        returns the length of this vector using the 2 point distance formula
        '''
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def get_normalized(self):
        '''
        returns the normalized vector in this direction
        '''
        return self / self.length()
    
    def normalize(self):
        '''
        normalizes self - modifies the object!
        '''
        self.x /= self.length()
        self.y /= self.length()
        
    def dot(self, another):
        '''
        dot product with another vector.
        '''
        return self.x * another.x + self.y * another.y
    
    def sign(self, another):
        '''
        returns positive if another is clockwise of self, and negative o/w.
        '''
        if self.y * another.x > self.x * another.y:
            return 1
        
        return -1
    
    def __repr__(self):
        return '<{x}, {y}>'.format(x=self.x, y=self.y)
    
    def __str__(self):
        return self.__repr__()
#------------------------------------------------------------------------------ 
class PointList(Matrix2D):
    '''
    A class to represent a set of normalized co-ordinates as a matrix. For
    example, the points {(0,0), (1,2), (-1, 2.75)} are represented as
    
    /             \
    |  0   0   1  |
    |  1   2   1  |
    | -1  2.75 1  |
    \             /
    
    Where the 3rd element in every row is the h' parameter chosen be default
    to be 1.
    ''' 
    def __init__(self, points, hprime=1):
        '''
        ctor: takes a list of points - each of which is a tuple of the form 
        (x,y) and returns an object with each row representing each 
        *normalized* co-ordinate, of the form (x, y, 1) - where h' has been 
        chosen to be 1.
        '''
        if len(points[0]) == 2:
            p = [(h, k, hprime) for h, k in points]
        elif len(points[0]) == 3:
            p = points
            
        Matrix2D.__init__(self, p)
    
    def translate(self, translation):
        '''
        translates all the points by the given translation. translation must be
        a tuple representing translations in the X and Y directions, 
        respectively, i.e., of the form (Tx, Ty).
        *Returns the transformed PointList; Does NOT transform in place*
        '''
        tx, ty = translation
        T = Matrix2D([[1,  0,  0],
                    [0,  1,  0],
                    [tx, ty, 1]])
        
        return self * T
    
    def rotate(self, radians, about=None):
        '''
        rotates all the points by the given angle in rads. about, if given, 
        is a tuple representing the point about which the rotation is to be
        carried out. If about is not given, rotation is performed about (0,0).
        '''
        C, S = cos(radians), sin(radians)
        F = 1 - C
        if about:
            h, k = about
            R = Matrix2D([[ C,              S,                0],
                          [-S,              C,                0],
                          [(k * S + h * F), ( k * F - h * S), 1]])
        else:
            R = Matrix2D([[ C, S, 0],
                          [-S, C, 0],
                          [ 0, 0, 1]])
        
        return self * R
    
    def scale(self, scale_factors):
        '''
        2-D scaling.
        scale_factors should be a tuple of 2 elements of the form (sx, sy) where
        sx and sy represent the scale-factors in X and Y directions, 
        respectively.
        '''
        sx, sy = scale_factors
        S = Matrix2D([[sx,  0,  0],
                      [ 0, sy,  0],
                      [ 0,  0,  1]])
        
        return self * S 
    
    def points(self):
        '''
        returns a list of points, each represented as an (x,y) tuple. Note that
        internally, normalized co-ordinates of the form (x, y, 1) are used.
        '''  
        return [point[:2] for point in self]
    