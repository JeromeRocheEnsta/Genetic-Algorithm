# coding=utf-8
"""
This is our 2nd attempt to modelise individual and population.
there is no more sort ! We gain in complexity.
"""


import time
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Individual:
    '''Class Individual: all information about a concrete solution.
    It includes: the genetic code for that solution and its fitness
    '''

    def __init__(self, input_array):
        self.input_array = input_array
        Individual = np.random.randint(
            0, 2, size=(len(input_array), 1)).flatten()
        self.genes = Individual
        self.fitness = self.evaluate_fitness()

    def evaluate_fitness(self):
        s = sum([self.input_array[i]
                 for i in range(len(self.input_array)) if self.genes[i]])

        # return sum(self.genes)/(0.1+abs(s))
        # return sum(self.genes)*len(self.input_array)/(0.1+(s/len(self.input_array))**2)
        # return sum(self.genes)/(1+s**2/len(self.input_array))
        # return sum(self.genes)*len(self.input_array)**2/(100+abs(s))
        return (sum(self.genes)/len(self.input_array))/(1+abs(s))

    def crossover_individuals(self, par1, par2, nb_crossover_points):
        """
        Input: 2 parents and the number of crossover summits
        Output: The child individual
        """

        #First we choose the crossover summits localisation
        crossover_points = random.sample(
            range(1, len(self.input_array)), nb_crossover_points)
        crossover_points.sort()

        #Genes is the child genes
        genes = np.zeros((len(self.genes),), dtype=int)

        #We alternate par1 genes and par2 genes betwenn the crossover points summits
        genes[:crossover_points[0]] = par1.genes[:crossover_points[0]]

        for i in range(0, nb_crossover_points):
            index = crossover_points[i]
            if i % 2:
                par = par1.genes
            else:
                par = par2.genes

            if i == nb_crossover_points-1:
                genes[index:] = par[index:]
            else:
                genes[index:crossover_points[i+1]
                      ] = par[index:crossover_points[i+1]]

        #We modify the child
        self.genes = genes
        self.fitness = self.evaluate_fitness()

    def mutate_individual(self):
        #We randomly choose the gene for mutation
        s = random.randint(0, len(self.input_array)-1)

        if self.genes[s] == 0:
            self.genes[s] = 1

        else:
            self.genes[s] = 0

        #Don't forget reevaluate the fitness
        self.fitness = self.evaluate_fitness()


class Population:
    '''
    Class Population: All informations about a population
    It includes: The population size, The mutation rate calculate with input_array,
    The individuals in the population, their fitness, the number of generation
    '''

    def __init__(self, input_array, pop_size, selection_method, renew_rate=0.3, win_rate=0.9, mutation_rate=-1):
        """ Create a population of random Individuals"""
        population = []
        fitness = []
        self.pop_size = pop_size
        self.input_array = input_array
        
        for _ in range(pop_size):
            A = Individual(self.input_array)
            population.append(A)
            fitness.append(A.fitness)

        self.population = population
        self.fitness = fitness
        self.generation = 1
        
        if mutation_rate == -1: self.mutation_rate = 1/len(input_array)
        else: self.mutation_rate = mutation_rate
        
        self.renew_rate = renew_rate
        self.selection_method = selection_method
        self.win_rate = win_rate

    def select_individuals(self):
        """
        Input: The name of our selection méthod, the rate of winning
        for the winner of our fight in the tournament méthod
        Output: One individual for the parents that will be engage in reproduction
        """
        if self.selection_method == 'roulette':
            #Classic method of the roulette to implement a naive probability low
            #based on the fitness
            roulette = [0] * self.pop_size
            norm = sum(self.fitness)
            roulette[0] = self.fitness[0]/norm
                
            for i in range(1, self.pop_size):
                roulette[i] = self.fitness[i]/norm + roulette[i-1]
            
            roulette[self.pop_size-1] = 1
            
            x = random.random()
            i = 0
            
            while x > roulette[i]:
                i += 1

            return self.population[i]
        
        elif self.selection_method == 'tournament':
            #Two random parents fights. The one with the best fitness have
            # win_rate pourcentage to be selected
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)
            win_rate=random.random()
            s= random.random()
            if parent1.fitness >= parent2.fitness:
                if s <= win_rate:
                    parent = parent1
                else:
                    parent = parent2
            else:
                if s <= win_rate:
                    parent = parent2
                else:
                    parent = parent1
            return parent


    def evolve(self):
        """Evolve population to next generation
        Use the roulette method to pick parents for crossover
        Or use the tournament method with his win_rate
        In Both cases: 
        --> We keep the fittest individual
        --> renew_rate pourcentage of old individual selected by the actual method
        --> approximatively renew_rate pourcentage of random new individual
        --> the remaining are created by crossover
        """
        if self.renew_rate > 0.5:
            raise ValueError("Renew rate must be between 0 and 0.5 (included)")
        #The fittest
        next_generation = [max(self.population, key=lambda indiv: indiv.fitness)]
        next_fitness = [max(self.fitness)]

        #s in the number associate to the renew_rate
        s = int(self.renew_rate*self.pop_size)
        

        #s old individuals
        for _ in range(s):
            selected_indiv = self.select_individuals()
            next_generation.append(selected_indiv)
            next_fitness.append(selected_indiv.fitness)

        # The remaining created by crossover
        for _ in range(self.pop_size - 2*s):
            #We randomly generate a number of crossover summits points
            nb_crossover_points = random.randint(
                1, int(len(self.input_array)/10))

            #We selecte parents
            parent1, parent2 = self.select_individuals(), self.select_individuals()

            #Create a child
            child = Individual(self.input_array)
            child.crossover_individuals(parent1, parent2, nb_crossover_points)
            
            #We submit the child to mutation
            if random.random() > self.mutation_rate:
                child.mutate_individual()

            next_generation.append(child)
            next_fitness.append(child.fitness)

        #We add s-1 random new individual
        for _ in range(s-1):
            A = Individual(self.input_array)
            next_generation.append(A)
            next_fitness.append(A.fitness)

        self.generation += 1
        self.population = next_generation
        self.fitness = next_fitness


    def get_fittest(self):
        """
        Returns fittest individual of the population
        """
        return max(self.population, key=lambda indiv: indiv.fitness)