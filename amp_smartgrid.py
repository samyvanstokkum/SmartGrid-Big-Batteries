# Classes
from house import House
from battery import Battery

# from random_route import Route
# from reverse_route import Route
# from non_reverse_route import Route

from route import Route

# Functions
from import_csv import import_district, import_batteries
from amp_grid import create_grid, hill_climbing, swap


def main():
    # set some values to true or false, based on what you want to run
    district_nr = 1 # 2,3 

    # decide which algorithm type you want for first try
    algorithm_type = "old"
    # algorithm_type = "reverse"
    # algorithm_type = "non_reverse" 
    # algorithm_type = "random"

    # decide which optimization type
    # optimization_type = "none"
    # optimization_type = "stochastic_hill_climber"  # this would be just "random swaps and pick better one"
    optimization_type = "steepest_ascent_hill_climber"  # check all options and choose best one
    # optimization_type = "simulated_annealing"

    # combine with somethings else??
    extra_optimzation = "Prim"
    random_swaps = True

    if optimization_type == "simulated_annealing":
        temperature = [40,60,70] # maybe a list and try all of them oid?

    # other variables needed (when optimization_type is not "none")
    iterations = 1000  # = number of swaps

    # put random_swap_every_x to zero when you don't want any random swaps
    random_swap_every_x = 100

    # when you don't want random swaps
    if not random_swaps:
        random_swap_every_x = iterations

    # change if want to plot
    plot_costs = True
    plot_grid = True

    # load houses from district and get house coordinates
    district, x_houses, y_houses = import_district(district_nr)

    # load batteries from district and get battery coordinates
    batteries = import_batteries(district_nr)

    # calculates and stores the routes
    r = Route()
    routes = r.import_routes(district, batteries)
        
    # get distance from every house to battery
    house_to_battery_distance = r.get_house_to_batteries_distances(district, batteries)

    # based on the algorithms and optimization methods above, run different functions
    if algorithm_type == "random":
        create_random_grid (district, x_houses,y_houses,batteries,routes, optimization_type)
    
    if algorithm_type == "stochastic_hill_climber" or algorithm_type == "steepest_ascent_hill_climber":
        hill_climber(district, x_houses,y_houses,batteries,routes, house_to_battery_distance,
         optimization_type, iterations, random_swap_every_x, plot_costs, plot_grid)
    
    if algorithm_type == "simulated_annealing":
        hill_climber(district, x_houses,y_houses,batteries,routes, house_to_battery_distance,
         optimization_type, iterations, temperature, plot_costs, plot_grid)

    # plots the district and batteries in a grid
    if algorithm_type == "old":
        create_grid(district, x_houses, y_houses, batteries, routes, house_to_battery_distance,
        optimization_type, iterations, random_swap_every_x, plot_costs, plot_grid)

# TODO: create different route files (random + reverse and non_reverse)
# TODO: adjust placement of last house in route file so it will search in different batteries when last house cannot be placed
# TODO: add 3D cost plot (cost, iterations, random_swap_x) -> 
# TODO: make figures for all different options and compare
# TODO: add simulated_annealing combination
# TODO: add sharing grids/cables
# TODO: save good options, can't go back to them right now (when you do bad random swap, it's gone)
# TODO: add only good swaps 

if __name__ == "__main__":
    main()
