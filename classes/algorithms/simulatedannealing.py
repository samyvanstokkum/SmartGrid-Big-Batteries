from math import log, floor, exp
import random
import matplotlib.pyplot as plt
from helpers import *
from prim import Prim
import copy


class SimulatedAnnealing():
    def __init__(self, batteries, share_grid, temp = 100, cooling_rate = 0.03, scheme = "linear"):
        self.batteries = batteries
        self.share_grid = share_grid 
        self.temp = temp
        self.cooling_rate = cooling_rate
        self.scheme = scheme 
        self.all_costs = []
        self.optimize()
    
    def optimize(self):

        # calculate number of iterations possible with current temp and cooling rate
        if self.scheme == "linear":
            iterations = floor(self.temp/self.cooling_rate)

        elif self.scheme == "exp":
            iterations = floor(log(1/self.temp)/log(1 - self.cooling_rate))


        for i in range(iterations):
            if i % 10 == 0:
                print(f"still running... {i}")
            # calculate costs of current iteration and perform SA
            
        
            # best_costs starts as costs from i = 0
            if i == 0:
                self.get_costs()
                best_costs = copy.deepcopy(self.all_costs[0])
                best_option = copy.deepcopy(self.batteries)

            self.SA()
            self.get_costs()

            # # check if cost from this i is better than best_cost option and update best_option   
            if i > 0 and self.all_costs[-1] < best_costs:
                best_option = copy.deepcopy(self.batteries)
                best_costs = self.all_costs[-1]

            # update temperature
            if self.scheme == "linear":
                self.temp = self.temp - self.cooling_rate
            elif self.scheme == "exp":
                self.temp *= 1 - self.cooling_rate

        self.batteries = best_option

    def get_costs(self):
        costs = 0

        if self.share_grid == False:

            for battery in self.batteries:
                for house in battery.houses:
                    costs += (abs(house.x - battery.x) + abs(house.y - battery.y)) * 9
            
            self.all_costs.append(costs)

        else:
            prim = Prim(self.batteries)
            self.all_costs.append(prim.costs)

    def plot_costs(self):
        plt.figure()
        plt.plot(self.all_costs)
        plt.xlabel("iterations")
        plt.title(f"Begin costs: {self.all_costs[0]} \n minimum costs: {min(self.all_costs)}\n SA")
        plt.ylabel("costs")
        plt.show()

    def SA(self):
        # choose random battery and random house
        chosen_battery = random.choice(self.batteries)
        chosen_house = random.choice(chosen_battery.houses)

        # get index of battery number and delete the current battery 
        all_battery_nrs = [1, 2, 3, 4, 5]
        all_battery_nrs.remove(chosen_battery.id) 

        # empty list for all swap_options
        swap_options = []
        old_costs = self.all_costs[-1]

        # loop through all batteries and their houses to check if a swap is possible and what the cost would be
        for potential_battery_nr in all_battery_nrs:       
            potential_battery = self.batteries[potential_battery_nr-1]
            
            for potential_house in potential_battery.houses:
                chosen_battery_cap = chosen_battery.capacity + chosen_house.power

                # check = check_swap(potential_house, chosen_battery_cap, chosen_house, potential_battery)
                # check if swap is possible capacity-wise

                if potential_house.power < chosen_battery_cap and \
                    chosen_house.power < potential_battery.capacity + potential_house.power:
                    
                    if self.share_grid == False:
                        # calculate current and new distance
                        potential_distance = get_manhattan_distance(potential_house, potential_battery) + \
                            get_manhattan_distance(chosen_house, chosen_battery)
                        new_distance = get_manhattan_distance(chosen_house, potential_battery) + \
                            get_manhattan_distance(potential_house, chosen_battery)
                        cost_difference = potential_distance - new_distance
                    
                    else: # share grid == True
                        swap(potential_house, potential_battery, chosen_house, chosen_battery)

                        prim = Prim(self.batteries)
                        new_costs = prim.costs
                        cost_difference = old_costs - new_costs

                        # reverse the swap
                        reverse_swap(potential_house, potential_battery, chosen_house, chosen_battery)

                    # save every option as tuple in a list
                    swap_options.append((potential_battery, potential_house, cost_difference))
        
        # check if want to make swap happen (only when swap_options are present) and:
        acceptance = 0
        
        if swap_options:
            desired_battery, house_to_extract, cost_decrease = max(swap_options, key= lambda x: x[2])
            if cost_decrease > 0:
                acceptance = 1

            else:
                desired_battery, house_to_extract, cost_increase = random.choice(swap_options)
                acceptance = exp(cost_increase/self.temp)
            
        # make swap
        if acceptance > random.random():

            # remove house from desired battery
            swap(house_to_extract, desired_battery, chosen_house, chosen_battery)
            print("Swapped")
            
       
