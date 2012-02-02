'''
Created on Dec 30, 2011

genetic_algorithm.py
The Genetic Algorithm module. Implements the class GenAlg and supporting 
data structures.

@author: yati
'''
from utils import sigmoid, clamped_rand, INFINITY
from random import random, randint

import settings

class Genome(object):
    '''Simple class to hold a genome structure'''
    def __init__(self, weights=None, fitness=0.0):
        if weights is None:
            self.weights = []
        else:
            self.weights = weights[:]
        
        self.fitness = fitness
    
    def __cmp__(self, another):
        '''overloads the comparison operators for sorting'''
        return cmp(self.fitness, another.fitness)
    

class GenAlg(object):
    '''
    classdocs
    '''
    def __init__(self, popsize, mutrate, crossrate, numweights):
        '''
        Constructor
        '''
        self._population_size = popsize
        self._mutation_rate = mutrate
        self._crossover_rate = crossrate
        self._chromo_length = numweights
        self._total_fitness = 0.0
        self._generation_count = 0
        self._fittest_genome = 0
        self._best_fitness = 0.0
        self._worst_fitness = INFINITY
        self._average_fitness = 0.0
        
        self._population = []
        for i in xrange(popsize):
            weights = [clamped_rand() for j in xrange(numweights)]
            self._population.append(Genome(weights, 0.0))
    
    def mutate(self, genome):
        '''
        mutates a chromosome, based on the mutation_rate by perturbing 
        its weights by an amount not greater than max_perturbation.
        **This potentially modifies the argument passed and returns whether
        this mod took place.** 
        '''
        mutated = False
        for i in xrange(len(genome.weights)):
            if random() < settings.MUTATION_RATE:
                genome.weights[i] += (clamped_rand() * settings.MAX_PERTURBATION)
                mutated = True
        
        return mutated
        
    def crossover(self, g1, g2):
        '''
        crossover weights of g1 and g2 with probability settings.CROSSOVER_RATE
        and return the two crossed over offsprings.
        '''
        if (random() > settings.CROSSOVER_RATE) or (g1 is g2):
            return (g1, g2)
        # Get the crossover position cp and perform crossover
        cp = randint(0, self._chromo_length - 1)
        baby1, baby2 = Genome(g1.weights, g1.fitness), Genome(g2.weights, g2.fitness)
        baby1.weights[cp:], baby2.weights[cp:] = g2.weights[cp:], g1.weights[cp:]
        
        return (baby1, baby2)
    
    def roulette_select(self):
        '''
        selects and returns a chromosome based on the Roulette Selection Algorithm.
        '''
        _slice = random() * self._total_fitness
        fitness_so_far = 0.0
        the_chosen_one = None
        
        for genome in self._population:
            fitness_so_far += genome.fitness
            if fitness_so_far >= _slice:
                the_chosen_one = genome
                break
        
        return the_chosen_one
    
    def reset(self):
        '''
        resets all the relevant vars ready for a new generation.
        '''
        self._total_fitness = 0.0
        self._best_fitness = 0.0
        self._average_fitness = 0.0
        self._worst_fitness = INFINITY
    
    def _calculate_fitness_measures(self):
        '''
        calculates the best, worst, average and total fitnesses of the
        population.
        '''
        self._total_fitness = 0.0
        highest_so_far = 0.0
        lowest_so_far = INFINITY
        
        for i in xrange(self._population_size):
            f = self._population[i].fitness
            if f > highest_so_far:
                highest_so_far = f
                self._fittest_genome = i
                self._best_fitness = highest_so_far
            
            if f < lowest_so_far:
                lowest_so_far = f
                self._worst_fitness = lowest_so_far
            
            self._total_fitness += f
        
        self._average_fitness = self._total_fitness / self._population_size
    
    def get_best(self, nbest, ncopies):
        '''
        returns a list containing ncopies copies of the nbest fittest 
        chomosomes.
        '''
        ret = []
        for i in xrange(nbest):
            ret.extend((self._population[i-nbest] for j in xrange(ncopies)))
        
        return ret
     
    def epoch(self):
        '''
        breeds one generation of chromosomes, assigns it to _population and
        returns the same
        '''
        self._population.sort()
        self._calculate_fitness_measures()
        new_pop = []
        
        if not (settings.NUM_COPIES_ELITE * settings.NUM_ELITE % 2):
            new_pop = self.get_best(settings.NUM_ELITE, 
                                    settings.NUM_COPIES_ELITE)
        
        while len(new_pop) < self._population_size:
            mom = self.roulette_select()
            dad = self.roulette_select()
            
            baby1, baby2 = self.crossover(mom, dad)
            self.mutate(baby1)
            self.mutate(baby2)
            
            new_pop.extend((baby1, baby2))
        
        self._population = new_pop
        self._population_size = len(new_pop)
    
        return self._population
    
    def get_population(self):
        return self._population
    
         
                 