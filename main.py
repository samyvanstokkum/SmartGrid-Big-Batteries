# Classes
from classes.house import House
from classes.battery import Battery
from route import *
from random_route import *


# Functions
from import_csv import import_district, import_batteries
from grid import optimize, hill_climbing, swap, SA


def main():
    #__________-
    # possible district, algorithm and optimization options 
    district_options = [1, 2, 3]
    algorithm_types = ["reverse", "random"]
    optimization_types = ["none", "stochastic_hill_climber", "steepest_ascent_hill_climber", "simulated_annealing"]

    # choose which option to use
    district_nr = district_options[0] 
    algorithm_type = algorithm_types[1]
    optimization_type = optimization_types[3]
    extra_optimzation = "Prim" # TODO 

    # other variables needed (when optimization_type is not "none")
    iterations = 1000  # = number of swaps
    random_swap_every_x = 100

    # change if want to plot
    plot_costs = True
    plot_grid = True
    random_swaps = False

    # when you don't want random swaps
    if not random_swaps:
        random_swap_every_x = iterations
    
    # parameters for simulated_annealing
    temperature = 100 #1, 100
    copy_temp = temperature
    cooling_rate = .003
    markov = 1 # set to one when want temp to decrease every iteration

    # calculate number of iterations possible 
    if optimization_type == "simulated_annealing":
        iterations = 0
        while copy_temp > 1:
            copy_temp *= 1 - cooling_rate
            iterations += 1

        iterations = iterations * markov

    # load houses from district and get house coordinates
    district, x_houses, y_houses = import_district(district_nr)

    # load batteries from district and get battery coordinates
    batteries = import_batteries(district_nr)

    # based on the algorithms and optimization methods above, run different functions
    if algorithm_type == "random":
        # import random_routes
        routes = rand_import_routes(district, batteries) 
        # optimize(batteries, routes, optimization_type, iterations, random_swap_every_x, 
        # plot_costs, plot_grid, temperature, cooling_rate, markov)    
    
    # when not random algorithm_type 
    elif algorithm_type == "reverse":
        routes = import_routes(district, batteries) # add algorithm_type
        optimize(batteries, routes, optimization_type, iterations, random_swap_every_x, plot_costs,
        plot_grid, temperature, cooling_rate, markov)

# TODO: create different route files (random + reverse and non_reverse)
# TODO: adjust placement of last house in route file so it will search in different batteries when last house cannot be placed
# TODO: add simulated_annealing combination
# TODO: add sharing grids/cables (Prims)
# TODO: save good options, can't go back to them right now (when you do bad random swap, it's gone)

if __name__ == "__main__":
    main()
