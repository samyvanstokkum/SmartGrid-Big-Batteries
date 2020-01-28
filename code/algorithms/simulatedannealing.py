from math import log, floor, exp
import random
import matplotlib.pyplot as plt
from helpers import *
from prim import Prim
import copy


class SimulatedAnnealing():
    """
    This class is devoted to the simulated annealing algorithm.

    Given an initial solution and several parameters, this algorithm 
    finds new solutions and, mostly in the beginning of the run, 
    accepts worse solutions in order to get to different optima. 
    In the end the process cools down and a (local) optimum 
    will be found.
    """

    def __init__(self, batteries, share_grid, temp=100, cooling_rate=0.03, scheme="exp"):
        self.batteries = batteries
        self.share_grid = share_grid
        self.temp = temp
        self.cooling_rate = cooling_rate
        self.scheme = scheme
        self.all_costs = []
        self.optimize()

    def optimize(self):
        """
        Optimize the configuration depending on the parameters.
        Keep a copy of the best configuration and update temperature
        after each iteration.
        """

        if self.scheme == "linear":
            iterations = floor(self.temp/self.cooling_rate)

        elif self.scheme == "exp":
            iterations = floor(log(1/self.temp)/log(1 - self.cooling_rate))

        for i in range(iterations):
            progress = round((i/iterations)*100, 2)
            if i % 20 == 0:
                print(f"Progress: {progress}%")
            if i == 0:
                self.get_costs()
                best_costs = copy.deepcopy(self.all_costs[0])
                best_option = copy.deepcopy(self.batteries)

            self.anneal()
            self.get_costs()

            if i > 0 and self.all_costs[-1] < best_costs:
                best_option = copy.deepcopy(self.batteries)
                best_costs = self.all_costs[-1]

            if self.scheme == "linear":
                self.temp = self.temp - self.cooling_rate
            elif self.scheme == "exp":
                self.temp *= 1 - self.cooling_rate

        self.batteries = best_option

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

                costs += battery.costs

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

        figure_name = f"{district_nr}_{optimization}"
        plt.figure()
        plt.plot(self.all_costs)
        plt.xlabel("iterations")
        plt.title(
            f"Begin costs: {self.all_costs[0]} \n Minimum costs: {min(self.all_costs)}\n")
        plt.ylabel("costs")
        plt.savefig(results_directory + figure_name)

        plt.show()

    def anneal(self):
        """Find possible swaps between a randomly chosen house and other houses. 
        
        If there are multiple swaps possible, make the best swap if it is an 
        improvement or accept a worse swap depending on an acceptance probability. 
        This in turns depends on the temperature at that time, which decreases
        after each iteration using a cooling scheme.
        """

        chosen_battery = random.choice(self.batteries)
        chosen_house = random.choice(chosen_battery.houses)

        swap_options = []
        old_costs = self.all_costs[-1]

        for potential_battery in self.batteries:
            if potential_battery == chosen_battery:
                continue
            for potential_house in potential_battery.houses:
                chosen_capacity = chosen_battery.capacity + chosen_house.power
                potential_capacity = potential_battery.capacity + potential_house.power

                if potential_house.power < chosen_capacity and \
                        chosen_house.power < potential_capacity:

                    if self.share_grid == False:
                        potential_distance = get_distance(potential_house, potential_battery) + \
                            get_distance(chosen_house, chosen_battery)

                        new_distance = get_distance(chosen_house, potential_battery) + \
                            get_distance(potential_house, chosen_battery)

                        cost_difference = potential_distance - new_distance

                    else:
                        swap(potential_house, potential_battery,
                             chosen_house, chosen_battery)

                        prim = Prim(self.batteries)

                        battery_costs = 0
                        for battery in self.batteries:
                            battery_costs += battery.costs

                        new_costs = prim.costs + battery_costs
                        cost_difference = old_costs - new_costs

                        reverse_swap(potential_house, potential_battery,
                                     chosen_house, chosen_battery)

                    swap_options.append(
                        (potential_battery, potential_house, cost_difference))

        acceptance = 0
        if swap_options:
            desired_battery, house_to_extract, cost_decrease = max(
                swap_options, key=lambda x: x[2])
            if cost_decrease > 0:
                acceptance = 1
            else:
                desired_battery, house_to_extract, cost_increase = random.choice(
                    swap_options)
                acceptance = exp(cost_increase/self.temp)
        if acceptance > random.random():
            swap(house_to_extract, desired_battery,
                 chosen_house, chosen_battery)
