# Classes
from house import House
from battery import Battery
from route import Route

# Functions
from import_csv import import_district, import_batteries
from grid import optimize, hill_climbing, swap


def main():

    # possible district, algorithm and optimization options 
    district_options = [1, 2, 3]
    algorithm_types = ["reverse", "non_reverse", "random"]
    optimization_types = ["none", "stochastic_ascent_hill_climber", "steepest_ascent_hill_climber", "simulated_annealing"]

    # choose which option to use
    district_nr = district_options[0] 
    algorithm_type = algorithm_types[0]
    optimization_type = optimization_types[2]
    extra_optimzation = "Prim"

    # other variables needed (when optimization_type is not "none")
    iterations = 1000  # = number of swaps
    random_swap_every_x = 100

    # change if want to plot
    plot_costs = True
    plot_grid = True
    random_swaps = True

    # when you don't want random swaps
    if not random_swaps:
        random_swap_every_x = iterations
    
    # parameters for simulated_annealing
    if optimization_type == "simulated_annealing":
        temperature = 90
        cooling_factor = 0.03

    # load houses from district and get house coordinates
    district, x_houses, y_houses = import_district(district_nr)

    # load batteries from district and get battery coordinates
    batteries = import_batteries(district_nr)

    # based on the algorithms and optimization methods above, run different functions
    if algorithm_type == "random":
        pass
        # import random_routes
        # TODO: create function for random route
        r = Route()
        routes = r.import_routes(district, batteries) 
        optimize(batteries, routes, optimization_type, iterations, random_swap_every_x, plot_costs, plot_grid)    
    
    # when not random algorithm_type 
    else:
        r = Route()
        routes = r.import_routes(district, batteries) # add algorithm_type, so will 
        optimize(batteries, routes, optimization_type, iterations, random_swap_every_x, plot_costs, plot_grid)

# TODO: create different route files (random + reverse and non_reverse)
# TODO: adjust placement of last house in route file so it will search in different batteries when last house cannot be placed
# TODO: add simulated_annealing combination
# TODO: add sharing grids/cables (Prims)
# TODO: save good options, can't go back to them right now (when you do bad random swap, it's gone)

if __name__ == "__main__":
    main()
