import os, sys

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "classes"))
sys.path.append(os.path.join(directory, "helper"))
sys.path.append(os.path.join(directory, "data"))

sys.path.append(os.path.join(directory, "classes", "objects"))
sys.path.append(os.path.join(directory, "classes", "algorithms"))

# Classes
from hillclimber import HillClimber
from simulatedannealing import SimulatedAnnealing
from configuration import Configuration


def main():
    
    # change this into get_string from user:
    # markov, different temp and cooling rates, linear/exp, etc


    config1 = Configuration("greedy", 2, share_grid = False)
    HC = HillClimber(config1.batteries, "stochastic", 10, share_grid = False)
    HC.plot_costs()
    # HillClimber(config1.batteries, 'stochastic', 1000, share_Grid = False)
    # SA = SimulatedAnnealing(config1.batteries, share_grid = False)
    config1.make_plot()
    # SA.plot_costs()
    


if __name__ == "__main__":
    main()
