# coding=utf-8
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from main import Population, Individual
import time


def create_simulation():
    root = tk.Tk()
    root.title('Genetic Algorithm')

    container = tk.Frame(root)
    container.pack(padx=10, pady=10)

    label = tk.Label(
        container, font=("Verdana", 16, "bold"), text='Welcome to Genetic Algorithm \nwith Python')
    label.grid(pady=10, columnspan=2)

    start_button = tk.Button(
        container, text='Start Simulation', bg='lightblue')
    start_button.grid(row=1, column=0, sticky='e')
    quit_button = tk.Button(
        container, text='Exit', bg='red', command=quit)
    quit_button.grid(pady=10, row=1, column=1, sticky='w')

    lowest_sum = tk.StringVar()
    avg_sum = tk.StringVar()
    worst_sum = tk.StringVar()
    generation = tk.StringVar()
    fittest_size = tk.StringVar()
    fittest_fitness = tk.StringVar()

    initial_array_size = tk.IntVar()
    pop_size = tk.IntVar()

    arraySizeLabel = tk.Label(container, text='Initial array size')
    arraySizeLabel.grid(row=2, column=0, sticky='E')
    arraySizeScale = tk.Scale(
        container, variable=initial_array_size, resolution=10, orient='horizontal', from_=1, to=100000)
    arraySizeScale.grid(row=2, column=1)

    popSizeLabel = tk.Label(container, text='Population size')
    popSizeLabel.grid(row=3, column=0, sticky='E')
    # popSizeScale = tk.Scale(container, orient='horizontal', variable=pop_size, resolution=10,
    #                         from_=1, to=initial_array_size.get())
    popSizeScale = tk.Scale(container, orient='horizontal', variable=pop_size, resolution=10,
                            from_=1, to=500)
    popSizeScale.grid(row=3, column=1)


    def update_scales(*args):
        if initial_array_size.get() > 200:
            popSizeScale.config(to=initial_array_size.get())
        else:
            popSizeScale.config(to=initial_array_size.get()*3)

    initial_array_size.trace(
        "w", update_scales)

    FILES = ["extraLarge", "extraLargeRand", "large",
             "largeRand", "medium", "mediumRand", "small", "smallRand"]

    filename = tk.StringVar()
    input_array = []

    tk.Label(container, text='Or choose a file:',
             font=('bold')).grid(rowspan=8, row=4, column=0, pady=10)

    row = 4
    for file in FILES:
        b = tk.Radiobutton(container, text=file, variable=filename, value=file)
        b.grid(column=1, row=row, sticky='W')
        row += 1


    def read_file():
        nonlocal input_array
        file = open("data/"+filename.get()+'.txt', 'r')
        initial_array_size.set(file.readline())
        data = file.readline().split(sep=', ')
        data = list(map(int, data))
        file.close()
        input_array = np.array(data)
        print("File loaded")

    tk.Button(container, text='choose file',
              command=read_file).grid(columnspan=2, pady=10)

    method = tk.StringVar()
    tk.Label(container, text='Choose a method').grid(rowspan=2, row=row+1, column=0)

    tk.Radiobutton(container, text='roulette', variable=method, value='roulette').grid(column=1, row=row+1, sticky='W')
    tk.Radiobutton(container, text='tournament', variable=method, value='tournament').grid(column=1, row=row+2, sticky='W')


    def run_simulation(event):
        style.use('ggplot')
        nonlocal input_array

        if len(input_array) == 0 or len(input_array) != initial_array_size.get():
            input_array = np.random.randint(-100,
                                            100, size=(initial_array_size.get(), 1)).flatten()
        pop = Population(input_array=input_array, pop_size=pop_size.get(), selection_method=method.get())

        # sum_values = [sum([pop.input_array[i]
        #                    for i in range(pop.pop_size) if indiv.genes[i]])
        #               for indiv in pop.population]

        # best_sums = [min(sum_values, key=abs)]
        # worst_sums = [max(sum_values, key=abs)]
        # avg_sums = [len(sum_values)/sum(sum_values)]
        # best_fitness = [max(pop.fitness)]
        best_sums = []
        best_fitness = []

        window = tk.Toplevel(root)
        window.title('Simulation')

        labelFrame = tk.Frame(window)
        labelFrame.grid(row=0, pady=10)

        label = tk.Label(labelFrame, text="Genetic Algo Simulation",
                         font=("sans serif", 16, "bold"))
        label.grid(
            columnspan=2, row=0, pady=10)

        # Display lowest sum of current population
        tk.Label(labelFrame, text="Fittest sum: ").grid(column=0, row=1, sticky='E')
        tk.Label(labelFrame, textvariable=lowest_sum).grid(column=1, row=1, sticky='W')

        # Display average sum of current population
        # tk.Label(labelFrame, text="Average sum: ").grid(column=0, row=2, sticky='E')
        # tk.Label(labelFrame, textvariable=avg_sum).grid(column=1, row=2, sticky='W')

        # Display worst sum of current population
        # tk.Label(labelFrame, text="Worst sum: ").grid(column=0, row=3, sticky='E')
        # tk.Label(labelFrame, textvariable=worst_sum).grid(column=1, row=3, sticky='W')

        # Display generation
        tk.Label(labelFrame, text="Generation: ").grid(column=0, row=4, sticky='E')
        tk.Label(labelFrame, textvariable=generation).grid(column=1, row=4, sticky='W')

        # Display solution size
        tk.Label(labelFrame, text="Fittest length: ").grid(column=0, row=5, sticky='E')
        tk.Label(labelFrame, textvariable=fittest_size).grid(column=1, row=5, sticky='W')

        # Display solution size
        tk.Label(labelFrame, text="Selection method: ").grid(column=0, row=6, sticky='E')
        tk.Label(labelFrame, textvariable=method).grid(column=1, row=6, sticky='W')


        fig = plt.Figure()
        ax = fig.add_subplot(211)
        ay = fig.add_subplot(212)

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().grid(row=1, padx=10, pady=10)


        def simulate(i):
            # if best_sums[-1] != 0 and pop.generation <= 3000:
            if i == 1 : start = time.time()

            if pop.generation <= 1000:
                pop.evolve()
                for indiv in pop.population:
                    if sum([pop.input_array[i] for i in range(len(pop.input_array)) if indiv.genes[i]]) == 0 and indiv.fitness > best_fitness[-1]:
                        print("Solution length: ", sum(indiv.genes),
                              " | ", "Array length: ", len(input_array))
                        print("Solution fitness: ", indiv.fitness)
                        print("Generation: ", pop.generation)
                        break

                # find fittest individual
                fittest = pop.get_fittest()
                fittest_size.set(sum(fittest.genes))
                fittest_fitness.set(fittest.fitness)

                # sum_values = [sum([pop.input_array[i]
                #                    for i in range(len(pop.input_array)) if indiv.genes[i]])
                #               for indiv in pop.population]

                best_fitness.append(fittest.fitness)

                best_sums.append(
                    sum([pop.input_array[i] for i in range(len(pop.input_array)) if fittest.genes[i]]))
                # worst_sums.append(max(sum_values, key=abs))
                # avg_sums.append(len(sum_values)/sum(sum_values))
                lowest_sum.set(best_sums[-1])
                # avg_sum.set(avg_sums[-1])
                # worst_sum.set(worst_sums[-1])
                generation.set(pop.generation)

            ax.clear()
            ay.clear()
            ax.plot(best_sums, color='g')
            # ax.plot(avg_sums, color='b')
            # ax.plot(worst_sums, color='r')
            ax.set_ylabel('Sum values')
            # ax.legend(['Fittest sum: ' + lowest_sum.get(), 'Average sum: ' +
            #            avg_sum.get()[:5]])
            ax.legend(['Fittest sum: ' + lowest_sum.get()])
            ay.plot(best_fitness, color='r')
            ay.set_xlabel('Generations')
            ay.set_ylabel('Fitness')
            ay.legend(['Best fitness: '+ fittest_fitness.get()])

            if i == 1: print(time.time() - start)

        ani = animation.FuncAnimation(
            fig, simulate, interval=150, blit=False, repeat=True)
        window.mainloop()

    start_button.bind('<Button-1>', run_simulation)
    root.mainloop()


if __name__ == '__main__':
    create_simulation()
