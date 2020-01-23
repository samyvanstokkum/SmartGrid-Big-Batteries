import random
import matplotlib.pyplot as plt


class HillClimber():
    def __init__(self, batteries, variant, iterations, share_grid):
        self.batteries = batteries
        self.variant = variant
        self.iterations = iterations
        self.share_grid = share_grid
        self.all_costs = []
        self.optimize()

    def optimize(self):
        if self.share_grid:

            if self.variant == "stochastic":
                for i in range(self.iterations):
                    self.get_costs()
                    self.stochastic_hillclimber_sharing()
            else: # if variant == "steepest ascent"
                for i in range(self.iterations):
                    self.get_costs()
                    self.steepest_ascent_hillclimber_sharing()

        else:

            if self.variant == "stochastic":
                for i in range(self.iterations):
                    self.get_costs()
                    self.stochastic_hillclimber_no_sharing()
            else: # if variant == "steepest ascent"
                for i in range(self.iterations):
                    self.get_costs()
                    self.steepest_ascent_hillclimber_no_sharing()

    
    def stochastic_hillclimber_sharing(self):

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
            potential_battery = self.batteries[potential_battery_nr - 1]
            
            for potential_house in potential_battery.houses:
                chosen_battery_capacity = chosen_battery.capacity + chosen_house.power

                # check if swap is possible capacity-wise
                if potential_house.power < chosen_battery_capacity and chosen_house.power < potential_battery.capacity + potential_house.power:
                    # calculate current and new distance
                    swap(potential_house, potential_battery, chosen_house, chosen_battery)

                    prim = Prim(self.batteries)
                    new_costs = prim.costs
                    cost_difference = old_costs - new_costs

                    # reverse the swap
                    reverse_swap(potential_house, potential_battery, chosen_house, chosen_battery)
                    
                    # save every option as tuple in a list
                    swap_options.append((potential_battery, potential_house, cost_difference))
    
        
        # check if want to make swap happen (only when swap_options are present)
        better_options = [option for option in swap_options if option[2] > 0]

        if better_options:
            battery_to_swap_with, house_to_extract, _ = random.choice(better_options) 

            swap(house_to_extract, battery_to_swap_with, chosen_house, chosen_battery)


    def stochastic_hillclimber_no_sharing(self):

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

    def steepest_ascent_hillclimber_no_sharing(self):      
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

    def steepest_ascent_hillclimber_sharing(self):      
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

    def get_costs(self):
        costs = 0
        for battery in self.batteries:
            for house in battery.houses:
                costs += (abs(house.x - battery.x) + abs(house.y - battery.y)) * 9
        
        self.all_costs.append(costs)

    def plot_costs(self):
            plt.figure()
            plt.plot(self.all_costs)
            plt.xlabel("iterations")
            plt.ylabel("costs")
            plt.show()
        