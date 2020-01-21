# Libraries
import matplotlib.pyplot as plt
import random
import numpy as np
from route import get_coordinates
import math



def optimize(batteries, routes, optimization_type, iterations, random_swap_every_x, plot_costs,
 plot_grid, temperature, cooling_rate, markov):

    if optimization_type == "none":
        iterations = 1

    all_costs = hill_climbing(batteries, routes, optimization_type, iterations, random_swap_every_x, plot_grid, 
    temperature, cooling_rate, markov)
    print(min(all_costs))

    if plot_costs:
        plt.figure()
        plt.title(f"min_costs:{min(all_costs)}")
        plt.xlabel("iteration")
        plt.ylabel("costs (distance * 9)")
        plt.plot(all_costs)
        plt.show()
        # plt.savefig(f"{optimization_type}")

