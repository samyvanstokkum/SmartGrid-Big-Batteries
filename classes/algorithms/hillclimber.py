import random
import matplotlib.pyplot as plt
from prim import Prim
from helpers import *
import copy


class HillClimber():
    def __init__(self, batteries, variant, iterations, share_grid):
        self.batteries = batteries
        self.variant = variant
        self.iterations = iterations
        self.share_grid = share_grid
        self.best_option = batteries
        self.all_costs = []
        self.optimize()

    def optimize(self):
      
        for i in range(self.iterations):
            self.get_costs()
            self.hillclimbing()
         
    def hillclimbing(self):

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
            potential_battery = self.batteries[potential_battery_nr - 1]
            
            houses = potential_battery.houses
            for potential_house in houses:
                chosen_battery_capacity = chosen_battery.capacity + chosen_house.power

                # check if swap is possible capacity-wise
                if potential_house.power < chosen_battery_capacity and chosen_house.power < potential_battery.capacity + potential_house.power:
                    
                    if self.share_grid == True:
                        # swap
                        swap(potential_house, potential_battery, chosen_house, chosen_battery)
                        
                        prim = Prim(self.batteries)
                        new_costs = prim.costs
                        cost_difference = old_costs - new_costs
                    
                        # reverse the swap
                        reverse_swap(potential_house, potential_battery, chosen_house, chosen_battery)
                    
                    else: # share grid == False
                        potential_distance = get_manhattan_distance(potential_house, potential_battery) + get_manhattan_distance(chosen_house, chosen_battery)
                        new_distance = get_manhattan_distance(chosen_house, potential_battery) + get_manhattan_distance(potential_house, chosen_battery)
                        cost_difference = potential_distance - new_distance

                    # save every option as tuple in a list
                    swap_options.append((potential_battery, potential_house, cost_difference))
    
        
        # check if want to make swap happen (only when swap_options are present)
        better_options = [option for option in swap_options if option[2] > 0]

        if better_options:
            if self.variant == "stochastic":
                battery_to_swap_with, house_to_extract, _ = random.choice(better_options) 
            else: # variant is steepest
                battery_to_swap_with, house_to_extract, cost_decrease = max(swap_options, key=lambda x: x[2])

            swap(house_to_extract, battery_to_swap_with, chosen_house, chosen_battery)
            print("Swapped, :) jeeeej!, Lekker dan, congratz")

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
            plt.ylabel("costs")
            plt.title(f"minimum costs:{min(self.all_costs)}")
            plt.show()
        

