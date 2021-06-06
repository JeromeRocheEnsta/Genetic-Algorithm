#coding=utf-8
from main import Individual, Population
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def main(input_array, pop_size, selection_method, renew_rate, win_rate, MAX_GEN=1000):
    """
    Main algorithm to seek the solution: the longest zero-sum subset
    """
    print('\n\n---- GENETIC ALGORITHM ----')
    print('\nloading...\n')

    start = time.time()

    # First we test if the input_array is already a solution (Just in case !)
    if sum(input_array) == 0:
        print("The initial array is already of sum zero")
        return None

    pop = Population(input_array, pop_size=pop_size, selection_method=selection_method)
    solution = []
    
    while pop.generation < MAX_GEN:
        pop.evolve()
        
        fittest = pop.get_fittest()


        if sum([ input_array[i] for i in range(len(input_array)) if fittest.genes[i] ]) == 0:
            if fittest != solution:
                print('\nSubset of zero sum found!')
                print('Subset length: ', sum(fittest.genes), ' | Array length', len(fittest.genes), ' | Fitness', fittest.fitness)
                print('Generation: ', pop.generation)
                print(time.time()-start, 'seconds')
                print('\nloading...\n')
            
            if not solution: solution = fittest

            elif fittest.fitness > solution.fitness:
                solution = fittest
    
    end = time.time()
    print("\nTime {}s".format(end-start))

    if solution:
        print("\nBest solution found:")
        print("Sum {} | Length {} | Fitness {}".format(sum([ input_array[i] for i in range(len(input_array)) if fittest.genes[i] ]), sum(solution.genes), solution.fitness))
    else:
        print('No solution found.')

#### to plot the fitness.
def f(x, y):
    return (1000)*(y)/((100)+(x**2))


def get_data_sample(filename):
    file = open("data/"+filename+'.txt', 'r')
    array_size = file.readline()
    data = file.readline().split(sep=', ')
    data = list(map(int, data))
    file.close()
    return np.array(data), array_size

#################################
###### Main Programme ######
#################################
if __name__ == "__main__":

    DATA_FILES = ["extraLarge", "extraLargeRand", "large", "largeRand", "medium", "mediumRand", "small", "smallRand"]
    
    for filename in DATA_FILES:
        print(filename, "| size: ", get_data_sample(filename)[1])
    
    filename=input('Choose a data file: ')
    
    input_array=get_data_sample(filename)[0]

    pop_size=int(input('\nPopulation size: '))

    method=input('\nChoose a selection method: roulette or tournament\n')

    renew_rate=0.1
    win_rate=0.9

    main(input_array, pop_size=pop_size, selection_method=method, renew_rate=renew_rate, win_rate=win_rate)

    # Plotting fitness functions
    # ax= Axes3D(plt.figure())
    # f=np.vectorize(f)
    # X=np.linspace(0,1000,1000)
    # Y=np.linspace(0,1000,1000)
    # X, Y= np.meshgrid(X,Y)
    # Z=f(X,Y)
    # ax.plot_surface(X,Y,Z)
    # plt.show()