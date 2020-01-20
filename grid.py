# Libraries
import matplotlib.pyplot as plt
import random
import numpy as np
from route import get_coordinates
import math


def SA(routes, batteries, iteration, temperature):
    
    # choose random battery and random house
    random_battery_nr = random.randint(1,5)
    random_battery = batteries[random_battery_nr -1]
    random_house = random.choice(random_battery.houses)

    # get index of battery number and delete the current battery 
    all_battery_nr = [1,2,3,4,5]
    index_rand_batt = all_battery_nr.index(random_battery_nr)
    del all_battery_nr[index_rand_batt] 

    # empty list for all swap_options
    swap_options = []

    # loop through all batteries and their houses to check if a swap is possible and what the cost would be
    for current_battery_nr in all_battery_nr:       
        current_battery = batteries[current_battery_nr-1]
        
        for house in current_battery.houses:
            random_battery_cap = random_battery.capacity + random_house.usage

            # check if swap is possible capacity-wise
            if house.usage < random_battery_cap and random_house.usage < current_battery.capacity + house.usage:
                
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

        # when a swap option leads to less costs
        if max(swap_options, key= lambda x: x[2])[2] > 0:
            acceptance = 1
            desired_battery = max(swap_options, key= lambda x: x[2])[0]
            house_to_extract = max(swap_options, key= lambda x: x[2])[1]

        # check if want to accept anyway (when )
        else:
            # go check for SA
            # chose random house from list
            random_choice = random.choice(swap_options)
            house_to_extract = random_choice[1]
            desired_battery = random_choice[0]
            acceptance = math.exp((random_choice[2])/temperature)
        
    # make swap
    if acceptance > random.random() :

        # remove house from desired battery
        desired_battery.remove_house(house_to_extract)
        x, y = get_coordinates(house_to_extract, desired_battery)
        routes[desired_battery].remove((x, y))

        # remove random house from random battery
        random_battery.remove_house(random_house)
        x, y = get_coordinates(random_house, random_battery)
        routes[random_battery].remove((x, y))

        # add house to extract to random battery
        random_battery.add_house(house_to_extract)
        x, y = get_coordinates (house_to_extract, random_battery)
        routes[random_battery].append((x, y))

        # add random house to desired battery
        desired_battery.add_house(random_house)
        x, y = get_coordinates(random_house, desired_battery)
        routes[desired_battery].append((x,y))

    return routes

def swap(routes, batteries, iteration, random_swap_every_x, optimization_type):
    
    # choose random battery and random house
    random_battery_nr = random.randint(1,5)
    random_battery = batteries[random_battery_nr -1]
    random_house = random.choice(random_battery.houses)

    # get index of battery number and delete the current battery 
    all_battery_nr = [1,2,3,4,5]
    index_rand_batt = all_battery_nr.index(random_battery_nr)
    del all_battery_nr[index_rand_batt] 

    # empty list for all swap_options
    swap_options = []

    # loop through all batteries and their houses to check if a swap is possible and what the cost would be
    for current_battery_nr in all_battery_nr:       
        current_battery = batteries[current_battery_nr-1]
        
        for house in current_battery.houses:
            random_battery_cap = random_battery.capacity + random_house.usage

            # check if swap is possible capacity-wise
            if house.usage < random_battery_cap and random_house.usage < current_battery.capacity + house.usage:
                
                # calculate current and new distance
                current_distance = abs(house.x - current_battery.x) + abs(house.y - current_battery.y) + abs(random_house.x - random_battery.x) + abs(random_house.y - random_battery.y)
                new_distance = abs(random_house.x - current_battery.x) + abs(random_house.y - current_battery.y) + abs(house.x - random_battery.x) + abs(house.y - random_battery.y)
                
                # distance_difference is positive when new distance is closer
                distance_difference = current_distance - new_distance

                # save every option as tuple in a list
                swap_options.append((current_battery, house, distance_difference))
   
    go_on = False
    
    # check if want to make swap happen (only when swap_options are present) and:
    if swap_options:

        # when it's time for random swap
        if iteration % random_swap_every_x == 0:
            go_on = True
        
        # when a swap option leads to less costs
        elif max(swap_options, key= lambda x: x[2])[2] > 0:
            go_on = True

    # make swap
    if go_on == True:
        
        # choose battery and house with minimal costs 
        if iteration % random_swap_every_x != 0:
            desired_battery = max(swap_options, key= lambda x: x[2])[0]
            house_to_extract = max(swap_options, key= lambda x: x[2])[1]

        elif optimization_type == "stochastic_hill_climber":
            random_battery_nr = random.choice(all_battery_nr)
            desired_battery = batteries[random_battery_nr -1]
            house_to_extract = random.choice(desired_battery.houses)

        # choose random battery and house
        else:
            random_battery_nr = random.choice(all_battery_nr)
            desired_battery = batteries[random_battery_nr -1]
            house_to_extract = random.choice(desired_battery.houses)

        # remove house from desired battery
        desired_battery.remove_house(house_to_extract)
        x, y = get_coordinates(house_to_extract, desired_battery)
        routes[desired_battery].remove((x, y))

        # remove random house from random battery
        random_battery.remove_house(random_house)
        x, y = get_coordinates(random_house, random_battery)
        routes[random_battery].remove((x, y))

        # add house to extract to random battery
        random_battery.add_house(house_to_extract)
        x, y = get_coordinates (house_to_extract, random_battery)
        routes[random_battery].append((x, y))

        # add random house to desired battery
        desired_battery.add_house(random_house)
        x, y = get_coordinates(random_house, desired_battery)
        routes[desired_battery].append((x,y))

    return routes

def hill_climbing(batteries, routes, optimization_type, iterations, random_swap_every_x, plot_grid, 
temperature, cooling_rate, markov):
    
    plot_fig = False
    colors = ['r', 'b', 'g', 'c', 'y']
    all_cable_distance = []

    # perform all swaps and save cable distances/costs
    for iteration in range(iterations):
        
        # set plot_fig to true when is last iteration
        if iteration == iterations-1 and plot_grid:
            plot_fig = True

        # create new routes with swap function, based on optimization type
        if optimization_type == "stochastic_hill_climber" or optimization_type == "steepest_ascent_hill_climber":
            routes = swap(routes, batteries, iteration, random_swap_every_x, optimization_type)
        elif optimization_type == "simulated_annealing":
            routes = SA(routes, batteries, iteration, temperature)
            if iteration % markov == 0 :
                temperature *= 1 - cooling_rate

        # plot batteries and houses
        if plot_fig:
            plt.figure()

            for battery in batteries:
                plt.plot(battery.x, battery.y, colors[battery.id-1]+'o', markersize=10, label='batteries')
                for house in battery.houses:
                    plt.plot(house.x, house.y, 'k*')
            plt.grid()
            plt.legend(loc='upper center', ncol=10, fontsize=8)

        cable_distance = 0
        
        # calculate costs and plot lines
        for battery in batteries:
            for coordinates_x, coordinates_y in routes[battery]:

                if plot_fig:
                    plt.plot(coordinates_x, coordinates_y, colors[battery.id -1])
                
                # calculate distance
                cable_distance += abs(coordinates_x[0]-coordinates_x[2]) + abs(coordinates_y[0] - coordinates_y[2])
        
        if plot_fig:
            plt.title(f"cable costs:{cable_distance * 9}")
            # plt.savefig(f"grid_{optimization_type}")
            # plt.close()
        
        # append cable distance for these options
        all_cable_distance.append(cable_distance)

    return all_cable_distance

def optimize(batteries, routes, optimization_type, iterations, random_swap_every_x, plot_costs,
 plot_grid, temperature, cooling_rate, markov):

    if optimization_type == "none":
        iterations = 1

    all_costs = hill_climbing(batteries, routes, optimization_type, iterations, random_swap_every_x, plot_grid, 
    temperature, cooling_rate, markov)
    print(min(all_costs))

    if plot_costs:
        plt.figure()
        plt.title(f"min_costs:{min(all_costs)}")
        plt.xlabel("iteration")
        plt.ylabel("costs (distance * 9)")
        plt.plot(all_costs)
        plt.show()
        # plt.savefig(f"{optimization_type}")

