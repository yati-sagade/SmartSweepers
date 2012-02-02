'''
Created on Jan 24, 2012
minesweeper.py
Defines the Mine and MineSweeper classes
@author: yati
'''
import math
import settings
from utils import clamped_rand, INFINITY, clamp
from geom2D import Vector2D
from neuralnet import NeuralNet
from genetic_algorithm import GenAlg
from random import random, randint

class Mine(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self._position = Vector2D(x,y)
    
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, pos):
        self._position = pos
        self.x, self.y = pos.x, pos.y
        
    
    def __repr__(self):
        return '<Mine: ({0}, {1})>'.format(self.x, self.y)
    

class MineSweeper(object):
    '''
    The minesweeper class.
    '''
    def __init__(self):
        self.brain = NeuralNet(settings.NUM_INPUTS,
                               settings.NUM_OUTPUTS,
                               settings.NUM_HIDDEN,
                               settings.NEURONS_PER_HIDDEN)
        
        self.position = Vector2D(random() * settings.WINDOW_WIDTH, 
                                 random() * settings.WINDOW_HEIGHT)
        
        self.look_at = Vector2D()
        self.rotation = random() * 2 * math.pi
        self.ltrack = 0.16
        self.rtrack = 0.16
        self.fitness = 0.0
        self.scale = settings.SWEEPER_SCALE
        self.closest_mine = 0
        self.speed = 0.0
    
    def reset(self):
        self.position = Vector2D(random() * settings.WINDOW_WIDTH, 
                                 random() * settings.WINDOW_HEIGHT)
        
        self.fitness = 0.0
        self.rotation = random() * 2 * math.pi
    
    def get_closest_mine(self, all_mines):
        '''
        finds and returns a Vector2D that is the position of the mine closest to
        this minesweeper. Expects an iterable of `Mine`s as the parameter
        `all_mines`.
        '''
        closest_so_far = INFINITY
        closest_object = Vector2D(0, 0)
        ctr = 0
        for mine in all_mines:
            l = (mine.position - self.position).length()
            if l < closest_so_far:
                closest_so_far = l
                closest_object = self.position - mine.position
                self.closest_mine = ctr
            
            ctr += 1
            
        return closest_object
     
    def update(self, all_mines):
        '''
        This is the real brains function. Takes an iterable of mines. It first
        takes sensor readings and feed these to the ANN of our minesweeper.
        The inputs are:
            1) A vector (Vector2D) to the closest mine,
            2) The "look at" vector (also a Vector2D).
        
        The brain(ANN) returns 2 outputs, ltrack and rtrack - which are forces
        applied on left and right tracks, respectively. Depending on these, the
        acceleration and/or the rotation is calculated and the position vector
        is updated accordingly.
        '''
        # Inputs to the brain.
        inputs = []
        # First input: vector to the closest mine.
        closest_mine = self.get_closest_mine(all_mines)
        closest_mine.normalize()
        # Place the inputs on the input list
        inputs.append(closest_mine.x)
        inputs.append(closest_mine.y)
        inputs.append(self.look_at.x)
        inputs.append(self.look_at.y)
        # Now, excite the brain and get the feedback
        output = self.brain.excite(inputs, settings.BIAS, filter_sigmoid=True)
        # Make sure we get back the expected number of outputs
        if len(output) != settings.NUM_OUTPUTS:
            raise Exception( 'An error occurred: The number of outputs from '
                            +'the ANN is not what was expected.')
        
        self.ltrack, self.rtrack = output
        
        rot_force = self.ltrack - self.rtrack
        rot_force = clamp(rot_force, 
                          -settings.MAX_TURN_RATE, 
                          settings.MAX_TURN_RATE)
        # New rotation and speed:
        self.rotation += rot_force
        self.speed = self.ltrack + self.rtrack
        # Get the new look at:
        self.look_at.x = -math.sin(self.rotation)
        self.look_at.y = math.cos(self.rotation)
        # Get the new position:
        self.position += (self.look_at * self.speed)
        # Wrap around the screen
        if self.position.x > settings.WINDOW_WIDTH:
            self.position.x = 0
        
        if self.position.x < 0:
            self.position.x = settings.WINDOW_WIDTH
            
        if self.position.y > settings.WINDOW_HEIGHT:
            self.position.y = 0
        
        if self.position.y < 0:
            self.position.y = settings.WINDOW_HEIGHT
        # End update()
    
    def check_for_mine(self, mines, size):
        '''
        checks for a collision with the closest mine.
        '''
        d = self.position - mines[self.closest_mine].position
        if d.length() < (size + 5):
            return self.closest_mine
        
        return -1
    
    def inc_fitness(self):
        self.fitness += 1
    
    def put_weights(self, weights):
        self.brain.put_weights(weights)
    
    def get_num_weights(self):
        return self.brain.get_num_weights()
    
    def __repr__(self):
        return '<MineSweeper: ({0}, {1})>'.format(self.position.x,
                                                 self.position.y)
    
        
            
        
        
        
        
                
        
        
        