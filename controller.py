'''
Created on Jan 25, 2012

@author: yati
'''
import pygame
from geom2D import Vector2D, PointList
from genetic_algorithm import GenAlg, Genome
from settings import *
from minesweeper import Mine, MineSweeper
from random import random


pygame.init()

# This is is the geometry of a minesweeper about the origin. Easy to trace out with
# a pen and a paper, and easier to see if you run the code :)
MINESWEEPER_VERTICES = PointList(
                                (
                                  (-1, -1),
                                  (-1,  1),
                                  (-0.5, 1),
                                  (-0.5, 0.5),
                                  (-0.25, 0.5),
                                  (-0.25, 1.75),
                                  (0.25, 1.75),
                                  (0.25, 0.5),
                                  (0.5, 0.5),
                                  (0.5, 1),
                                  (1, 1),
                                  (1, -1),
                                  (0.5, -1),
                                  (0.5, -0.5),
                                  (-0.5, -0.5),
                                  (-0.5, -1)
                                )
                            )
# And, of course, the mines.
MINE_VERTICES = PointList((
                          (-1, -1),
                          (-1,  1),
                          ( 1,  1),
                          ( 1, -1),
                 )) 

# Do I really miss "pure" abstract classes in PythonLand? Don't think so.
class BaseShape(object):
    def draw(self, screen):
        return pygame.draw.aalines(screen,
                                   self.color,
                                   True,
                                   self.vertices.points())
        
class MineSweeperFigure(BaseShape):
    def __init__(self, minesweeper, color=None):
        self.vertices = (MINESWEEPER_VERTICES
                         .scale((SWEEPER_SCALE, SWEEPER_SCALE))
                         .rotate(minesweeper.rotation)
                         .translate(translation=(minesweeper.position.x, 
                                                 minesweeper.position.y)))
    
        if not color:
            self.color = (0, 0, 255) # blue
        else:
            self.color = color

class MineFigure(BaseShape):
    def __init__(self, mine, color=None):
        self.vertices = (MINE_VERTICES
                         .scale((MINE_SCALE, MINE_SCALE))
                         .translate((mine.x, mine.y)))
        
        if not color:
            self.color = (255, 0, 0) # red 
        else:
            self.color = color

class Controller(object):
    '''
    The controller class.
    This class would rather be a module with the related functions.
    Controller syncs the `MineSweeper`s and the `GenAlg` objects to produce
    actual meaningful simulations.
    '''
    def __init__(self, pygame_screen):
        self.ticks = 0
        self.num_sweepers = NUM_SWEEPERS
        self.num_mines = NUM_MINES
        self.screen = pygame_screen
        self.generations = 0
        self.sweepers = [MineSweeper() for i in xrange(self.num_sweepers)]
        self.num_weights = self.sweepers[0].get_num_weights()
        self.GA = GenAlg(NUM_SWEEPERS,
                         MUTATION_RATE,
                         CROSSOVER_RATE,
                         self.num_weights)
        
        self.population = self.GA.get_population()
        for i in xrange(self.num_sweepers):
            self.sweepers[i].put_weights(self.population[i].weights)
            
        self.mines = []
        for i in xrange(self.num_mines):
            self.mines.append(Mine(random() * WINDOW_WIDTH, 
                                   random() * WINDOW_HEIGHT))
        
    
    def update(self):
        if self.ticks < NUM_TICKS:
            self.ticks += 1
            for i in xrange(self.num_sweepers):
                self.sweepers[i].update(self.mines)
                
                grab_hit = self.sweepers[i].check_for_mine(self.mines, 
                                                           MINE_SCALE)
                if grab_hit >= 0:
                    self.sweepers[i].inc_fitness()
                    self.mines[grab_hit].position = Vector2D(random() * WINDOW_WIDTH,
                                                             random() * WINDOW_HEIGHT)
                    self.population[i].fitness = self.sweepers[i].fitness
                
        else:
            self.generations += 1
            self.ticks = 0
            self.population = self.GA.epoch()
            
            for i in xrange(self.num_sweepers):
                self.sweepers[i].put_weights(self.population[i].weights)
                self.sweepers[i].reset()

    def render(self):
        fs = map(MineSweeperFigure, self.sweepers)
        fs = []
        i = 0
        for sweeper in self.sweepers:
            color = (0,255,0) if i < NUM_ELITE else None
            fs.append(MineSweeperFigure(sweeper, color))
            i += 1
         
        fm = map(MineFigure, self.mines)
        self.screen.fill((0,0,0))
        map(lambda x: x.draw(self.screen), fs)
        map(lambda x: x.draw(self.screen), fm)
        pygame.display.flip()
            
            
                         
                         
