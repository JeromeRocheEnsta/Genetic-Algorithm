# coding=utf-8
import unittest
import shape


indiv_length = 50
pop_size = 200
input_array = nb.random.randint(-1000,1000,size=(1000,1).flatten()
#input_array = [(-2)**i for i in range(201)]
mutation_rate = 1/indiv_length

indiv = shape.Individual(input_array, indiv_length)

population = shape.Population(input_array,indiv_length)


class TestStringMethods(unittest.TestCase):

    # Tests sur les méthodes de la classe individu
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_individual(self):
        self.assertEqual(len(indiv.set), 50)
        for i in range(indiv_length):
            for j in range(indiv_length):
                if i != j:
                    self.assertNotEqual(indiv.indexes[i], indiv.indexes[j])

    def test_fitness(self):
        a = 1/(1+sum(indiv.set)**2)
        self.assertEqual(indiv.calc_fitness(), a)

    def test_crossover(self):
        par1 = shape.Individual(input_array, indiv_length)
        par2 = shape.Individual(input_array, indiv_length)
        child = shape.Individual(input_array, indiv_length)

        child.crossover(par1, par2)
        # vérifie qu'on a pas créer un trisomique avec un gène en trop
        self.assertEqual(len(child.set), indiv_length)

        for i in range(indiv_length):
            code = 0
            if child.set[i] not in par1.set:
                if child.set[i] not in par2.set:
                    code = +1
        # vérifie que ses gènes viennent bien toujours d'un de ses deux parents
        self.assertEqual(code, 0)
        # système de bledard pcq flemme de définir une erreur juste pour ça du coup jle fais avec un assertEqual ca marche tout pareil :)

        for i in range(indiv_length):
            for j in range(indiv_length):
                if i != j:
                    # vérifie que dans le cas ou les deux parents possedaient une valeur en commun, l'enfant ne l'a pas prise des deux simultanément auquel cas il aurait 2 fois la même valeur ce qui doit être exclus
                    self.assertNotEqual(child.indexes[i], child.indexes[j])

    def test_mutation(self):
        initialSet = indiv.set
        initialIndexes = indiv.indexes
        indiv.mutation(input_array)

        compteur = 0
        i0 = 0
        for i in range(indiv_length):
            if initialSet[i] != indiv.set[i]:
                compteur = compteur+1
        # on vérifie que bien une seul valeur à été modifié
        self.assertNotEqual(compteur, 1)

        for i in range(indiv_length):
            for j in range(indiv_length):
                if i != j:
                    # on vérifie qu'on a bien pris une valeur qui n'était pas de base dans le chromosome
                    self.assertNotEqual(indiv.indexes[i], indiv.indexes[j])

    def test_NotEnoughDiversity(self):
        array = [1, -2, 3, -4, 5, -6]
        # vérifie si on lève bien une exception dans la méthode mutation
        self.assertRaises(shape.MutateError, indiv.mutation, array)

    def test_partitionIndiv(self):
        low = 20
        high = 10
        self.assertRaises(shape.RangeError, indiv.partition_indiv, low, high)


# Tests sur les méthodes de la classe population
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def test_population(self):
        self.assertEqual(len(population.set), pop_size)

    def test_evolve(self):
        A = population.set
        population.evolve()
        B = population.set
        self.assertNotEqual(A, B)

    def test_partitionPop(self):
        low = 20
        high = 10
        self.assertRaises(shape.RangeError,
                          population.partition_pop, low, high)


if __name__ == '__main__':
    unittest.main()
