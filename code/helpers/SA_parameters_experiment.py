import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
results_directory = directory + ".." +'/results/'
sys.path.append(os.path.join(directory, "..", "..", "data"))
sys.path.append(os.path.join(directory, "..", "..", "code"))
sys.path.append(os.path.join(directory, "..", "..", "code", "objects"))
sys.path.append(os.path.join(directory, "..", "..", "code", "algorithms"))
sys.path.append(os.path.join(directory, "..", "..", "code", "helpers"))

from configuration import Configuration
from simulatedannealing import SimulatedAnnealing
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import axes3d
import numpy as np 


def SA_parameters_experiment():
    """
    Given a list of temperatures and a list of coolings rates, this function will
    perform a simulated annealing for every combination. The minimum costs will be
    saved in 3D figure (temperature, coolingrate, costs) in which the optimal
    parameters combination can be found.
    """

    district = "1"              # ,"2","3"],
    initialization = "greedy"  # , "random", "cluster"
    share_grid = True           # False
    advanced = False            # True

    temperatures = np.arange(102, 110, 1)
    cooling_rates = np.arange(0.02, 0.09, 0.01)
    SA_SCHEME = "exp"

    min_costs = []
    xs = []
    ys = []

    # parameters for simulated_annealing
    for i in range(len(temperatures)):
        print("i")
        for j in range(len(cooling_rates)):
            print("j")
            TEMP = temperatures[i]
            print("1")
            COOLING_RATE = cooling_rates[j]
            print("2")
            config1 = Configuration(
                initialization, district, share_grid, advanced)
            print("3")
            SA = SimulatedAnnealing(
                config1.batteries, share_grid, TEMP, COOLING_RATE, SA_SCHEME)
            print("4")
            min_costs.append(min(SA.all_costs))
            xs.append(TEMP)
            ys.append(COOLING_RATE)

    # now plot results
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # create 3D plot and save
    ax.plot_trisurf(xs, ys, min_costs, cmap="Reds")
    index_min_cost = min_costs.index(min(min_costs))

    plt.title(
        f"temp:{xs[index_min_cost]}\n cooling_rate: {ys[index_min_cost]}")
    plt.ylabel("cooling factors")
    plt.xlabel("temperature")

    save_name_grid = f"SA_parameters{district}_{initialization}_{share_grid}"
    plt.savefig(results_directory + save_name_grid)


if __name__ == "__main__":
    SA_parameters_experiment()
