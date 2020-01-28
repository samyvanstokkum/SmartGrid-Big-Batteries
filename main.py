# add current structure to path
import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
results_directory = directory + '/results/'
sys.path.append(os.path.join(directory, "classes"))
sys.path.append(os.path.join(directory, "helper"))
sys.path.append(os.path.join(directory, "data"))
sys.path.append(os.path.join(directory, "classes", "objects"))
sys.path.append(os.path.join(directory, "classes", "algorithms"))

# import classes and functions
from hillclimber import HillClimber
from simulatedannealing import SimulatedAnnealing
from configuration import Configuration
from get_user_input import get_user_input
from output import get_output, get_output_shared

import json


def main():
    
    # global variables 
    HC_ITERATIONS = 1000
    TEMP = 102
    COOLING_RATE = 0.03
    SA_SCHEME = "exp"

    # parameters from which the user can choose 
    districts = ["1","2","3"]
    initialization_options = ["greedy", "random", "cluster"]
    optimization_options = ["none", "hillclimber","simulated annealing"]
    share_gridlines = ["yes", "no"]

    # welcome user
    print("\nWelcome to SmartGrid\n")
    
    # let user choose which parameters to use
    initialization, district, share_grid, optimization, optimization_type = get_user_input(initialization_options, districts, share_gridlines, optimization_options)

    # move to place where plots are made
    
    # save_name_grid = "grid" + district  + optimization
    # save_name_costs = "costs" + district  + optimization
    # plt.savefig(results_directory + save_name_costs + optimization_type)
    # plt.savefig(results_directory + save_name_grid + optimization_type)


    # initial configuration
    config1 = Configuration(initialization, district, share_grid)

    # plot the configuration grid when user wants no optimization 
    if optimization == "none":
        config1.make_plot(results_directory, optimization)
    
    elif optimization == "hillclimber":
        # create HC object with current parameters
        HC = HillClimber(config1.batteries, optimization_type, HC_ITERATIONS, share_grid)

        # generate figure with the change in costs over all iterations
        HC.plot_costs(results_directory, optimization, config1.district_nr)

        # update batteries in config1 and plot results
        config1.batteries = HC.batteries
        config1.make_plot(results_directory, optimization)

    else: # optimization == simulated annealing
        # create SA object with current parameters
        SA = SimulatedAnnealing(config1.batteries, share_grid, TEMP, COOLING_RATE, SA_SCHEME)
        
        # generate figure with the change in costs over all iterations
        SA.plot_costs(results_directory, optimization, config1.district_nr)

        # update batteries in config1 and plot results
        config1.batteries = SA.batteries
        config1.make_plot(results_directory, optimization)

    if not share_grid:
        output = get_output(config1.batteries)
    else:
        output = get_output_shared(config1)
    
    # print output
    # print(json.dumps(output, indent=4))


if __name__ == "__main__":
    main()
