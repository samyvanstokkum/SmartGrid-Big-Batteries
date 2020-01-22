import random

class HillClimber():
    def __init__(self, batteries, variant, iterations, share_grid = False):
        self.batteries = batteries
        self.variant = variant
        self.iterations = iterations
        self.share_grid = share_grid
        self.optimize()

    def optimize(self):
        if self.variant == "stochastic":
            for i in range(self.iterations):
                self.stochastic_hillclimber()
        else: # if variant == "steepest ascent"
            for i in range(self.iterations):
                self.steepest_ascent_hillclimber()
    
    def stochastic_hillclimber(self):

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
            current_battery = self.batteries[current_battery_nr - 1]
            
            for house in current_battery.houses:
                random_battery_capacity = random_battery.capacity + random_house.power

                # check if swap is possible capacity-wise
                if house.power < random_battery_capacity and random_house.power < current_battery.capacity + house.power:
                    # calculate current and new distance
                    current_distance = abs(house.x - current_battery.x) + abs(house.y - current_battery.y) + abs(random_house.x - random_battery.x) + abs(random_house.y - random_battery.y)
                    new_distance = abs(random_house.x - current_battery.x) + abs(random_house.y - current_battery.y) + abs(house.x - random_battery.x) + abs(house.y - random_battery.y)
                    
                    # distance_difference is positive when new distance is closer
                    distance_difference = current_distance - new_distance

                    # save every option as tuple in a list
                    swap_options.append((current_battery, house, distance_difference))
    
        
        # check if want to make swap happen (only when swap_options are present)
        better_options = [option for option in swap_options if option[2] > 0]

        if better_options:
            battery_to_swap_with, house_to_extract, _ = random.choice(better_options) 

            battery_to_swap_with.remove_house(house_to_extract)
            random_battery.remove_house(random_house)
            random_battery.add_house(house_to_extract)
            battery_to_swap_with.add_house(random_house)


    def steepest_ascent_hillclimber(self):      
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
            current_battery = self.batteries[current_battery_nr - 1]
            
            for house in current_battery.houses:
                random_battery_capacity = random_battery.capacity + random_house.power

                # check if swap is possible capacity-wise
                if house.power < random_battery_capacity and random_house.power < current_battery.capacity + house.power:

                    # calculate current and new distance
                    current_distance = abs(house.x - current_battery.x) + abs(house.y - current_battery.y) + abs(random_house.x - random_battery.x) + abs(random_house.y - random_battery.y)
                    new_distance = abs(random_house.x - current_battery.x) + abs(random_house.y - current_battery.y) + abs(house.x - random_battery.x) + abs(house.y - random_battery.y)
                    
                    # distance_difference is positive when new distance is closer
                    distance_difference = current_distance - new_distance

                    # save every option as tuple in a list
                    swap_options.append((current_battery, house, distance_difference))
        
    
        # check if want to make swap happen (only when swap_options are present)
        battery_to_swap_with, house_to_extract, cost_decrease = max(swap_options, key=lambda x: x[2])
        if cost_decrease > 0:
            battery_to_swap_with.remove_house(house_to_extract)
            random_battery.remove_house(random_house)
            random_battery.add_house(house_to_extract)
            battery_to_swap_with.add_house(random_house)

        