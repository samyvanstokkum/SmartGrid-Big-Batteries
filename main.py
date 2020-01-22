# Classes
from classes.hillclimber import HillClimber
from classes.simulatedannealing import SimulatedAnnealing
from classes.configuration import Configuration
from classes.prim_class import Prim


def main():
    
    # change this into get_string from user:
    # markov, different temp and cooling rates, linear/exp, etc
    # possible district, algorithm and optimization options 
    district_options = [1, 2, 3]
    algorithm_types = ["reverse", "random"]
    optimization_types = ["none", "stochastic_hill_climber", "steepest_ascent_hill_climber", "simulated_annealing"]
    extra_optimzation = "Prim"  # in combination with above

    # change if want to plot, keep?
    plot_costs = True
    plot_grid = True
    shared_grid = False

    config1 = Configuration("random", 1)
    config1.make_plot()
    # HillClimber(config1.batteries, "steepest", 1000)
    # HillClimber(config1.batteries, 'stochastic', 1000)
    SA = SimulatedAnnealing(config1.batteries)
    SA.plot_costs()
    


if __name__ == "__main__":
    main()
