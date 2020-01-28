from random import choice
import matplotlib.pyplot as plt
from prim import Prim
from helpers import *
import copy


class HillClimber():
    """
    This class is devoted to the hillclimber algorithm.
    Given an initial configuration of houses to batteries, depending
    on the parameters, this algorithm will optimize the configuration.
    Plotting the results is also possible.
    """

    def __init__(self, batteries, variant, share_grid, iterations=1000):
        self.batteries = batteries
        self.variant = variant
        self.iterations = iterations
        self.share_grid = share_grid
        self.best_option = batteries
        self.all_costs = []
        self.optimize()

    def optimize(self):
        """
        Optimize the given configuration. Get costs for each iteration.
        """

        for i in range(self.iterations):
            progress = round((i/iterations)*100, 2)
            if i % 20 == 0:
                print(f"Progress: {progress}%")
            self.get_costs()
            self.hillclimbing()

    def hillclimbing(self):
        """
        Find possible swaps between a randomly chosen house 
        and all other houses. If there are multiple swaps possible given, 
        pick a random swap when hillblimbing is stochastic, and pick the best
        swap when hillblimbing is steepest ascent.
        """

        chosen_battery = choice(self.batteries)
        chosen_house = choice(chosen_battery.houses)

        swap_options = []
        old_costs = self.all_costs[-1]

        for potential_battery in self.batteries:
            if potential_battery == chosen_battery:
                continue
            houses = potential_battery.houses
            for potential_house in houses:
                chosen_battery_capacity = chosen_battery.capacity + \
                    chosen_house.power

                if potential_house.power < chosen_battery_capacity and \
                        chosen_house.power < potential_battery.capacity + potential_house.power:

                    if self.share_grid == True:
                        swap(potential_house,
                             potential_battery,
                             chosen_house,
                             chosen_battery)

                        prim = Prim(self.batteries)

                        battery_costs = 0
                        for battery in self.batteries:
                            battery_costs += battery.costs

                        new_costs = prim.costs + battery_costs
                        cost_difference = old_costs - new_costs

                        reverse_swap(potential_house,
                                     potential_battery,
                                     chosen_house,
                                     chosen_battery)

                    else:
                        potential_distance = get_distance(potential_house, potential_battery) + \
                            get_distance(chosen_house, chosen_battery)

                        new_distance = get_distance(chosen_house, potential_battery) + \
                            get_distance(potential_house, chosen_battery)

                        cost_difference = potential_distance - new_distance

                    swap_options.append((potential_battery,
                                         potential_house,
                                         cost_difference))

        better_options = [option for option in swap_options if option[2] > 0]
        if better_options:
            if self.variant == "stochastic":
                battery, house, _ = random.choice(better_options)
            else:
                battery, house, _ = max(swap_options, key=lambda x: x[2])

            swap(house,
                 battery,
                 chosen_house,
                 chosen_battery)

    def get_costs(self):
        """
        Get costs for current configuration depending
        on grid sharing possibilities.
        """

        costs = 0
        if self.share_grid == False:

            for battery in self.batteries:
                for house in battery.houses:
                    costs += (abs(house.x - battery.x) +
                              abs(house.y - battery.y)) * 9
                # costs += battery.costs

            self.all_costs.append(costs)

        else:
            prim = Prim(self.batteries)
            for battery in self.batteries:
                costs += battery.costs

            self.all_costs.append(prim.costs + costs)

    def plot_costs(self, results_directory, optimization, district_nr):
        """
        Plot the cost progression given the optimazation type and
        district number. Save the figure into the results folder.
        """

        figure_name = f"{self.variant}_{district_nr}_{optimization}"

        plt.figure()
        plt.plot(self.all_costs)
        plt.xlabel("iterations")
        plt.ylabel("costs")
        plt.title(f"minimum costs:{min(self.all_costs)}")
        plt.savefig(results_directory + figure_name)
        plt.show()