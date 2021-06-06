# coding=utf-8
import unittest
import numpy as np
from main import Population, Individual

data = [np.random.randint(-200, 200, size=(i, 1)).flatten()
        for i in range(100, 1000, 50)]


class TestIndividual(unittest.TestCase):
    '''Tests the Individual class'''

    def test_individual(self):
        '''Tests individual class constructor'''
        for array in data:
            indiv = Individual(array)
            for i in range(len(array)):
                self.assertIn(indiv.genes[i], [0, 1])

    def test_fitness(self):
        '''Tests fitness function'''
        for array in data:
            indiv = Individual(array)
            
            s = sum([array[i] for i in range(len(array)) if indiv.genes[i]])
            
            fitness = sum(indiv.genes)/len(array) / (1 + abs(s))
            
            self.assertEqual(indiv.evaluate_fitness(), fitness)


class TestPopulation(unittest.TestCase):
    '''Tests population class'''

    def test_population(self):
        '''Tests population class constructor'''
        for array in data:
            pop_size = np.random.randint(low=len(array)/100, high=len(array))
            population = Population(array, pop_size)
            self.assertEqual(len(population.population), pop_size)
            for i in range(len(population.population)):
                self.assertIsInstance(population.population[i], Individual)

    def test_evolve_roulette(self):
        '''Tests evolve method'''
        for array in data:
            pop_size = np.random.randint(low=len(array)/100, high=len(array))
            population = Population(array, pop_size)
            A = population.population
            population.evolve('roulette')
            B = population.population
            self.assertNotEqual(A, B)
            self.assertEqual(len(A), len(B))

            with self.assertRaises(ValueError):
                population.evolve('roulette', renew_rate=0.6)
        
    def test_evolve_tournament(self):
        '''Tests evolve method'''
        for array in data:
            pop_size = np.random.randint(low=len(array)/100, high=len(array))
            population = Population(array, pop_size)
            A = population.population
            population.evolve('tournament')
            B = population.population
            self.assertNotEqual(A, B)
            self.assertEqual(len(A), len(B))

            with self.assertRaises(ValueError):
                population.evolve('tournament', renew_rate=0.6)



if __name__ == '__main__':
    unittest.main()
