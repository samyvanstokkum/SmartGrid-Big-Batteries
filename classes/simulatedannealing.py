from math import log, floor, exp
import random


class SimulatedAnnealing():
    def __init__(self, batteries, share_grid = False, temp = 102, cooling_rate = 0.003, scheme = "linear"):
        self.batteries = batteries
        self.share_grid = share_grid 
        self.temp = temp
        self.cooling_rate = cooling_rate
        self.scheme = scheme 
        self.optimize()
    
    def optimize(self):
        iterations = floor(log(1/self.temp)/log(1 - self.cooling_rate))
        for i in range(iterations):
            self.SA()
    

    def SA(self):
        # choose random battery and random house
        random_battery = random.choice(self.batteries)
        random_house = random.choice(random_battery.houses)

        # get index of battery number and delete the current battery 
        all_battery_nrs = [1, 2, 3, 4, 5]
        all_battery_nrs.remove(random_battery.id) 

        # empty list for all swap_options
        swap_options = []

        # loop through all batteries and their houses to check if a swap is possible and what the cost would be
        for current_battery_nr in all_battery_nrs:       
            current_battery = self.batteries[current_battery_nr-1]
            
            for house in current_battery.houses:
                random_battery_cap = random_battery.capacity + random_house.power

                # check if swap is possible capacity-wise
                if house.power < random_battery_cap and random_house.power < current_battery.capacity + house.power:
                    
                    # calculate current and new distance
                    current_distance = abs(house.x - current_battery.x) + abs(house.y - current_battery.y) + abs(random_house.x - random_battery.x) + abs(random_house.y - random_battery.y)
                    new_distance = abs(random_house.x - current_battery.x) + abs(random_house.y - current_battery.y) + abs(house.x - random_battery.x) + abs(house.y - random_battery.y)
                    
                    # distance_difference is positive when new distance is closer
                    distance_difference = current_distance - new_distance

                    # save every option as tuple in a list
                    swap_options.append((current_battery, house, distance_difference))
        
        # check if want to make swap happen (only when swap_options are present) and:
        acceptance = 0
        
        if swap_options:
            desired_battery, house_to_extract, cost_decrease = max(swap_options, key= lambda x: x[2])
            if cost_decrease> 0:
                acceptance = 1

            else:
                # chose random house from list
                desired_battery, house_to_extract, cost_increase = random.choice(swap_options)
                acceptance = exp(cost_increase/self.temp)
            
        # make swap
        if acceptance > random.random():

            # remove house from desired battery
            desired_battery.remove_house(house_to_extract)
            random_battery.remove_house(random_house)
            random_battery.add_house(house_to_extract)
            desired_battery.add_house(random_house)
            

        


        
