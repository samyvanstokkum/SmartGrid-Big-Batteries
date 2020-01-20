# Classes
from house import House
from battery import Battery
from route import *
from random_route import *
from mpl_toolkits.mplot3d import axes3d


# Functions
from import_csv import import_district, import_batteries
from SA_grid import optimize, hill_climbing, SA
import numpy as np

def main():

    # possible district, algorithm and optimization options 
    district_options = [1, 2, 3]
    algorithm_types = ["reverse", "random"]
    optimization_types = ["simulated_annealing"]

    
    # choose which option to use
    district_nr = district_options[0] 
    algorithm_type = algorithm_types[1]
    optimization_type = optimization_types[0]

    all_temps = np.arange(100,140,2)
    all_coolings_rates = np.arange(0.003,0.03, 0.002)

    possibilities = len(all_temps) * len(all_coolings_rates)
    # min_costs = np.zeros((len(all_temps), len(all_coolings_rates)))
    min_costs = []
    xs = []
    ys = []
    # parameters for simulated_annealing

    # do 10000 its.
    temperature = 100
    cooling_rate = 0.003
    total_tries = 1000

    copy_temp = temperature
    iterations = 0
    while copy_temp > 1:
        copy_temp *= 1 - cooling_rate
        iterations += 1

    for i in range(total_tries):
    # for i in range(len(all_temps)):
    #     for j in range(len(all_coolings_rates)):
        # load houses from district and get house coordinates
        district, x_houses, y_houses = import_district(district_nr)

        # load batteries from district and get battery coordinates
        batteries = import_batteries(district_nr)

        # temperature = all_temps[i] #1, 100
        # copy_temp = temperature
        # cooling_rate = all_coolings_rates[j]

        # iterations = 0
        # while copy_temp > 1:
        #     copy_temp *= 1 - cooling_rate
        #     iterations += 1

        # based on the algorithms and optimization methods above, run different functions
        if algorithm_type == "random":
            # import random_routes
            routes = rand_import_routes(district, batteries) 
            min_costs.append(optimize(batteries, routes, iterations, temperature, cooling_rate))
            # xs.append(all_temps[i])
            # ys.append(all_coolings_rates[j])

        # when not random algorithm_type 
        elif algorithm_type == "reverse":
            routes = import_routes(district, batteries) # add algorithm_type
            min_costs.append(optimize(batteries, routes, iterations, temperature, cooling_rate))
            # xs.append(all_temps[i])
            # ys.append(all_coolings_rates[j])
    
    # now plot results
    fig = plt.figure()
    plt.hist(min_costs, bins=np.arange(min(min_costs), max(min_costs),1)
    plt.show()

    ax = plt.axes(projection='3d')

    # Plot a basic wireframe.
    # ax.plot_wireframe(xs, ys, min_costs, rstride=10, cstride=10)
    # plt.show()

    # Data for a three-dimensional line
    X, Y, Z = axes3d.get_test_data(0.05)
    ax.plot_trisurf(xs, ys, min_costs, cmap ="Reds")
    plt.ylabel("cooling factors")
    plt.title(f"min:{min(min_costs)}")
    plt.xlabel("temperature")
    plt.savefig("costs_random2")
    
    
    # plt.zlabel("costs")

    # ax.scatter3D(xs, ys, min_costs, c=min_costs, cmap='Greens')

    plt.show()
    a = b



if __name__ == "__main__":
    main()
