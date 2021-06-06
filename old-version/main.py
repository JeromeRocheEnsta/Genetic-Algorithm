# coding=utf-8
"""It's our first code and we abondon it so it is difficult to read because
it isn't optimise....
"""
#############################
######## Importations #######
#############################

import time
import numpy as np
import random
import matplotlib.pyplot as plt


#############################
########### Code ###########
#############################


class ShapeError(Exception):
    pass


class MutateError(ShapeError):
    pass


class RangeError(ShapeError):
    pass


class Individual:
    """Class Individual: all information about a concrete solution.
    It includes: the size of the individual (not the same than the input_array),
    The array of integers, and the array of the indexes of these integers in
    the input_array (to find check that we don't have two times the samegene in our
    individuals)
    """

    def __init__(self, input_array, indiv_length):
        """
        Be carreful: we can't take the same antecedents two times
        """
        indexes = []
        individual = []
        
        #Don't take two times the same indexes
        for j in range(indiv_length):
            index = np.random.randint(0, len(input_array))
            while index in indexes:
                index = np.random.randint(0, len(input_array))
            individual.append(input_array[index])
            indexes.append(index)

        self.indexes = indexes
        self.length = indiv_length
        self.genes = individual

    def evaluate_fitness(self):
        """ Method that give a quotation to an Individual """
        #We choose a square to penalize more the big sums
        return 1/(1+sum(self.genes)**2)



    def crossover(self, par1, par2):
        """For every indexes we select randomly the gene from one parent or the other.
        If the gene selected is already in the child, we took the other.
        We can't have two tie the same indexe because the parents are sorted.
        """
        par1.quickSort(0, self.length-1)
        par2.quickSort(0, self.length-1)
        n = par1.length  # all individuals have same length
        self.indexes = [-1]*n
        for i in range(n):
            # random probability
            prob = random.random()
            # 50% from par1 and 50% from par2
            if prob < 0.5:  # we choose par1
                # if true then choose the other par
                if (verify_presence(self.indexes, par1.indexes[i])):
                    self.indexes[i] = par2.indexes[i]
                    self.genes[i] = par2.genes[i]
                else:
                    self.indexes[i] = par1.indexes[i]
                    self.genes[i] = par1.genes[i]
            else:
                # if true then choose the other par
                if (verify_presence(self.indexes, par2.indexes[i])):
                    self.indexes[i] = par1.indexes[i]
                    self.genes[i] = par1.genes[i]
                else:
                    self.indexes[i] = par2.indexes[i]
                    self.genes[i] = par2.genes[i]


    def mutation(self, initial_array):
        # We can't mutate if the size of the individual is the same as the initial_array
        self.quickSort(0, self.length-1)
        index_new_gene = np.random.randint(0, len(initial_array))
        # Check that we don't choose an index already in our individual
        count = 0
        # We add count in the case the method doesn't find any possible mutation
        while (index_new_gene in self.indexes) and (count <= len(initial_array)):
            index_new_gene = np.random.randint(0, len(initial_array))
            count += 1
        mutation_index = np.random.randint(0, self.length)
        self.genes[mutation_index] = initial_array[index_new_gene]
        self.indexes[mutation_index] = index_new_gene


####FUNCTIONS TO QUICK SORT
    def quickSort(self, low, high):
        if low < high:

            # pi is partitioning index, self.indexes[p] is now
            # at right place
            pi = self.partition_indiv(low, high)

            # Separately sort elements before
            # partition and after partition
            self.quickSort(low, pi-1)
            self.quickSort(pi+1, high)

    def partition_indiv(self, low, high):
        # high have to be greater than low
        if low > high:
            raise RangeError('Range error in partition_indiv')
        else:
            i = (low-1)  # index of smaller element
            pivot = self.indexes[high]     # pivot
            for j in range(low, high):
                # If current element is smaller than or
                # equal to pivot
                if self.indexes[j] <= pivot:
                    # increment index of smaller element
                    i = i+1
                    self.indexes[i], self.indexes[j] = self.indexes[j], self.indexes[i]
                    self.genes[i], self.genes[j] = self.genes[j], self.genes[i]
            self.indexes[i+1], self.indexes[high] = self.indexes[high], self.indexes[i+1]
            self.genes[i+1], self.genes[high] = self.genes[high], self.genes[i+1]
            return (i+1)




def verify_presence(array, test):
    # check if test is in array, true/false return
    for x in array:
        if x == test:
            return True
    return False


class Population:
    """
    Class Population: All informations about a population
    It includes: The population size, The mutation rate calculate with input_array,
    the length of every individuals
    """

    def __init__(self, input_array, indiv_length, pop_size):
        """ Create a M population of random Individual"""
        population = []
        fitness = []
        self.pop_size = pop_size
        self.input_array = input_array
        self.indiv_length = indiv_length
        self.mutation_rate = 1/self.indiv_length
        for i in range(pop_size):
            A = Individual(self.input_array, self.indiv_length)
            population.append(A)
            fitness.append(A.evaluate_fitness())
        self.population = population
        self.fitness = fitness
        self.generation = 1

    
#####FUNCTIONS TO QUICK SORT
    def sorted(self, low, high):
        if low < high:
            # pi is partitioning index, self.indexes[p] is now
            # at right place
            pi = self.partition_pop(low, high)
            # Separately sort elements before
            # partition and after partition
            self.sorted(low, pi-1)
            self.sorted(pi+1, high)

    def partition_pop(self, low, high):
        # high have to be greater than low
        if low > high:
            raise RangeError('Range error in partition_indiv')
        else:
            i = (low-1)         # index of smaller element
            pivot = self.fitness[high]     # pivot
            for j in range(low, high):

                # If current element is smaller than or
                # equal to pivot
                if self.fitness[j] <= pivot:

                    # increment index of smaller element
                    i = i+1
                    self.fitness[i], self.fitness[j] = self.fitness[j], self.fitness[i]
                    self.population[i], self.population[j] = self.population[j], self.population[i]

            self.fitness[i+1], self.fitness[high] = self.fitness[high], self.fitness[i+1]
            self.population[i+1], self.population[high] = self.population[high], self.population[i+1]
            return (i+1)
############################


## We have tried different method to evolve. But they are our first tries
    def evolve_1(self):
        """ Create next generation"""
        next_generation = []
        next_fitness = []
        s = int((10*self.pop_size)/100)
        # We keep the 10% best individues in our population
        self.sorted(0, self.pop_size-1)
        next_generation.extend(self.population[s:])
        next_fitness.extend(self.fitness[s:])
        # for the remaining we do crossover and mutation with two randoms parents
        for _ in range(self.pop_size-s):
            parent1 = random.choice(self.population[:50])
            parent2 = random.choice(self.population[:50])
            child = Individual(self.input_array, self.indiv_length)
            prob = random.random()
            if prob < (1-self.mutation_rate):
                child.crossover(parent1, parent2)
                next_generation.append(child)
                next_fitness.append(child.evaluate_fitness())
            else:
                parent1.mutation(self.input_array)
                next_generation.append(parent1)
                next_fitness.append(parent1.evaluate_fitness())
        self.generation += 1
        self.population = next_generation
        self.fitness = next_fitness

    def evolve_2(self):
        """ Create next generation"""
        """ We add a roulette method to choose our parents for cross-over"""
        next_generation = []
        next_fitness = []
        s = int((10*self.pop_size)/100)
        # We keep the 10% best individues in our population
        self.sorted(0, self.pop_size-1)
        next_generation.extend(self.population[:s])
        next_fitness.extend(self.fitness[:s])
        # for the remaining we do crossover and mutation with probability related to the fitness
        # using the roulette probability method
        # roulette selection: survival of the fittest
        roulette = [0] * self.pop_size
        roulette[0] = self.fitness[0]/sum(self.fitness)
        for i in range(1, self.pop_size):
            roulette[i] = self.fitness[i]/sum(self.fitness) + roulette[i-1]
        roulette[self.pop_size-1] = 1
        for _ in range(self.pop_size-s):
            x = random.random()
            y = random.random()
            i, j = 0, 0
            while x > roulette[i] or y > roulette[j]:
                if x > roulette[i]:
                    i += 1
                if y > roulette[j]:
                    j += 1
            parent1 = self.population[i]
            parent2 = self.population[j]
            child = Individual(self.input_array, self.indiv_length)
            prob = random.random()
            if prob < (1-self.mutation_rate):
                child.crossover(parent1, parent2)
                next_generation.append(child)
                next_fitness.append(child.evaluate_fitness())
            else:
                parent1.mutation(self.input_array)
                next_generation.append(parent1)
                next_fitness.append(parent1.evaluate_fitness())
        self.generation += 1
        self.population = next_generation
        self.fitness = next_fitness

    def evolve_3(self):
        """ Create next generation"""
        """ We add a roulette method to choose our parents for cross-over"""
        next_generation = []
        next_fitness = []
        s = int((10*self.pop_size)/100)
        # We keep the 10% best individues in our population
        self.sorted(0, self.pop_size-1)
        next_generation.extend(self.population[:s])
        next_fitness.extend(self.fitness[:s])
        for _ in range(s):
            A = Individual(self.input_array, self.indiv_length)
            next_generation.append(A)
            next_fitness.append(A.evaluate_fitness())
        # for the remaining we do crossover and mutation with probability related to the fitness
        # using the roulette probability method
        # roulette selection: survival of the fittest
        roulette = [0] * self.pop_size
        roulette[0] = self.fitness[0]/sum(self.fitness)
        for i in range(1, self.pop_size):
            roulette[i] = self.fitness[i]/sum(self.fitness) + roulette[i-1]
        roulette[self.pop_size-1] = 1
        for _ in range(self.pop_size-2*s):
            x = random.random()
            y = random.random()
            i, j = 0, 0
            while x > roulette[i] or y > roulette[j]:
                if x > roulette[i]:
                    i += 1
                if y > roulette[j]:
                    j += 1
            parent1 = self.population[i]
            parent2 = self.population[j]
            child = Individual(self.input_array, self.indiv_length)
            prob = random.random()
            if prob < (1-self.mutation_rate):
                child.crossover(parent1, parent2)
                next_generation.append(child)
                next_fitness.append(child.evaluate_fitness())
            else:
                parent1.mutation(self.input_array)
                next_generation.append(parent1)
                next_fitness.append(parent1.evaluate_fitness())
        self.generation += 1
        self.population = next_generation
        self.fitness = next_fitness

    def evolve_4(self):
        """ Create next generation"""
        """ We add a roulette method to choose our parents for cross-over"""
        next_generation = []
        next_fitness = []
        s = int((10*self.pop_size)/100)
        # We keep the 10% best individues in our population
        self.sorted(0, self.pop_size-1)
        next_generation.extend(self.population[:s])
        next_fitness.extend(self.fitness[:s])
        # for the remaining we do crossover and mutation with probability related to the fitness
        # using the roulette probability method
        

        # roulette selection: survival of the fittest
        roulette = [0] * self.pop_size
        roulette[0] = self.fitness[0]/sum(self.fitness)
        for i in range(1, self.pop_size):
            roulette[i] = self.fitness[i]/sum(self.fitness) + roulette[i-1]
        roulette[self.pop_size-1] = 1
        

        for _ in range(self.pop_size-2*s):
            x = random.random()
            y = random.random()
            i, j = 0, 0
            while x > roulette[i] or y > roulette[j]:
                if x > roulette[i]:
                    i += 1
                if y > roulette[j]:
                    j += 1
            parent1 = self.population[i]
            parent2 = self.population[j]
            child = Individual(self.input_array, self.indiv_length)
            child.crossover(parent1, parent2)

            if random.random() < self.mutation_rate:
                child.mutation(self.input_array)

            next_generation.append(child)
            next_fitness.append(child.evaluate_fitness())

        for _ in range(s):
            A = Individual(self.input_array, self.indiv_length)
            next_generation.append(A)
            next_fitness.append(A.evaluate_fitness())


        self.generation += 1
        self.population = next_generation
        self.fitness = next_fitness

    def get_data(self):
        """We have to choose what data we want on the population, for our graphics and to renew the variable found in the main() """
        population_sums = [sum(indiv.population) for indiv in self.population]
        return self.fitness, population_sums


#################################
######## DRIVER CODE ############
#################################
# Main pour trouver la solution au problème


def main4(input_array, MAX_GEN, pop_size):
    debut = time.time()
    Max_found = False
    # Enable us to change the individual length
    length = len(input_array)
    print("Départ: ", input_array)
    while not Max_found and length > 0:
        if length != len(input_array):
            pop = Population(input_array, length, pop_size)
            fitness_values, sum_values = pop.get_data()
            found = False
            while not found and pop.generation <= MAX_GEN:
                pop.evolve_4()
                for indiv in pop.population:
                    if sum(indiv.population) == 0:
                        found = True
                        Solution_array = indiv.population
            if (pop.generation > MAX_GEN):
                length = length - 1
            else:
                Max_found = True
        else:
            if sum(input_array) == 0:
                print("Cool")
                Solution_array = input_array
                Max_found = True
            else:
                length = length-1
    if length <= 0:
        print("On a pas trouvé de sous liste dont la somme fait 0")
    else:
        print("La solution est {} avec la liste:{}".format(length, Solution_array))
        print(sum(Solution_array))
    fin = time.time()
    print("Le programme a mis {}s".format(fin-debut))


def main3(input_array, MAX_GEN, pop_size):
    debut = time.time()
    Max_found = False
    # Enable us to change the individual length
    length = len(input_array)
    print("Départ: ", input_array)
    while not Max_found and length > 0:
        if length != len(input_array):
            pop = Population(input_array, length, pop_size)
            fitness_values, sum_values = pop.get_data()
            found = False
            while not found and pop.generation <= MAX_GEN:
                pop.evolve_3()
                for indiv in pop.population:
                    if sum(indiv.population) == 0:
                        found = True
                        Solution_array = indiv.population
            if (pop.generation > MAX_GEN):
                length = length - 1
            else:
                Max_found = True
        else:
            if sum(input_array) == 0:
                Solution_array = input_array
                Max_found = True
            else:
                length = length-1
    if length <= 0:
        print("On a pas trouvé de sous liste dont la somme fait 0")
    else:
        print("La solution est {} avec la liste:{}".format(length, Solution_array))
        print(sum(Solution_array))
    fin = time.time()
    print("Le programme a mis {}s".format(fin-debut))


#################################
###### Principle Programme ######
#################################
if __name__ == "__main__":
    pop_size = 20
    MAX_GEN = 1000
    #input_array = np.random.randint(-100, 100, size=(40, 1)).flatten()
    input_array=[-13,13,-13,13 ,13,-13,13,-13,13,-13,13,-13]
    #main(input_array, MAX_GEN, pop_size)
    main3(input_array, MAX_GEN, pop_size)

