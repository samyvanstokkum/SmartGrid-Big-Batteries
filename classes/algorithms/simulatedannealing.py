from math import log, floor, exp
import random
import matplotlib.pyplot as plt
from helpers import *
from prim import Prim


class SimulatedAnnealing():
    def __init__(self, batteries, share_grid, temp = 102, cooling_rate = 0.003, scheme = "linear"):
        self.batteries = batteries
        self.share_grid = share_grid 
        self.temp = temp
        self.cooling_rate = cooling_rate
        self.scheme = scheme 
        self.all_costs = []
        self.optimize()
    
    def optimize(self):

        # calculate number of iterations possible with current temp and cooling rate
        iterations = floor(log(1/self.temp)/log(1 - self.cooling_rate))
        for i in range(iterations):
            if i % 10 == 0:
                print(f"still running... {i}")
            # calculate costs of current iteration and perform SA
            
            self.get_costs()
            if self.share_grid == False:
                self.SA_no_sharing()
            else:
                self.SA_sharing()
                
            # update temperature
            if self.scheme == "linear":
                self.temp *= 1 - self.cooling_rate
            elif self.schema == "exp":
                pass
            else:
                pass

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
        plt.show()

    def SA_no_sharing(self):
        # choose random battery and random house
        chosen_battery = random.choice(self.batteries)
        chosen_house = random.choice(chosen_battery.houses)

        # get index of battery number and delete the current battery 
        all_battery_nrs = [1, 2, 3, 4, 5]
        all_battery_nrs.remove(chosen_battery.id) 

        # empty list for all swap_options
        swap_options = []

        # loop through all batteries and their houses to check if a swap is possible and what the cost would be
        for potential_battery_nr in all_battery_nrs:       
            potential_battery = self.batteries[potential_battery_nr-1]
            
            for potential_house in potential_battery.houses:
                chosen_battery_cap = chosen_battery.capacity + chosen_house.power

                # check if swap is possible capacity-wise
                if potential_house.power < chosen_battery_cap and chosen_house.power < potential_battery.capacity + potential_house.power:
                    
                    # calculate current and new distance
                    potential_distance = abs(potential_house.x - potential_battery.x) + abs(potential_house.y - potential_battery.y) + abs(chosen_house.x - chosen_battery.x) + abs(chosen_house.y - chosen_battery.y)
                    new_distance = abs(chosen_house.x -potential_battery.x) + abs(chosen_house.y - potential_battery.y) + abs(potential_house.x - chosen_battery.x) + abs(potential_house.y - chosen_battery.y)
                    
                    # distance_difference is positive when new distance is closer
                    distance_difference = potential_distance - new_distance

                    # save every option as tuple in a list
                    swap_options.append((potential_battery, potential_house, distance_difference))
        
        # check if want to make swap happen (only when swap_options are present) and:
        acceptance = 0
        
        if swap_options:
            desired_battery, house_to_extract, cost_decrease = max(swap_options, key= lambda x: x[2])
            if cost_decrease > 0:
                acceptance = exp(cost_decrease/self.temp)

            else:
                desired_battery, house_to_extract, cost_increase = random.choice(swap_options)
                acceptance = exp(cost_increase/self.temp)
            
        # make swap
        if acceptance > random.random():

            # remove house from desired battery
            desired_battery.remove_house(house_to_extract)
            chosen_battery.remove_house(chosen_house)
            chosen_battery.add_house(house_to_extract)
            desired_battery.add_house(chosen_house)
            
    def SA_sharing(self):
        # choose random battery and random house
        chosen_battery = random.choice(self.batteries)
        chosen_house = random.choice(chosen_battery.houses)

        # get index of battery number and delete the current battery 
        all_battery_nrs = [1, 2, 3, 4, 5]
        all_battery_nrs.remove(chosen_battery.id) 

        # empty list for all swap_options
        swap_options = []

        # loop through all batteries and their houses to check if a swap is possible and what the cost would be
        old_costs = self.all_costs[-1]

        for potential_battery_nr in all_battery_nrs:       
            potential_battery = self.batteries[potential_battery_nr-1]
            
            houses = potential_battery.houses
            for potential_house in houses:
                chosen_battery_cap = chosen_battery.capacity + chosen_house.power

                # check if swap is possible capacity-wise
                if potential_house.power < chosen_battery_cap and chosen_house.power < potential_battery.capacity + potential_house.power:
                    
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
                # chose random house from list
                desired_battery, house_to_extract, cost_increase = random.choice(swap_options)
                acceptance = exp(cost_increase/self.temp)
            
        # make swap
        if acceptance > random.random():
            swap(house_to_extract, desired_battery, chosen_house, chosen_battery)
            print("Swapped, :) jeeeej!, Lekker dan, congratz")
        
