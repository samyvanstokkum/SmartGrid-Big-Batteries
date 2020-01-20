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


def hill_climbing(batteries, routes, iterations, temperature, cooling_rate):
    
    plot_fig = False
    colors = ['r', 'b', 'g', 'c', 'y']
    all_cable_distance = []

    # perform all swaps and save cable distances/costs
    for iteration in range(iterations):

        # create new routes with swap function, based on optimization type
        routes = SA(routes, batteries, iteration, temperature)
        temperature *= 1 - cooling_rate

        # plot batteries and houses
        cable_distance = 0
        
        # calculate costs and plot lines
        for battery in batteries:
            for coordinates_x, coordinates_y in routes[battery]:
                # calculate distance
                cable_distance += abs(coordinates_x[0]-coordinates_x[2]) + abs(coordinates_y[0] - coordinates_y[2])
        
        # append cable distance for these options
        all_cable_distance.append(cable_distance)

    return all_cable_distance

def optimize(batteries, routes, iterations, temperature, cooling_rate):

    all_costs = hill_climbing(batteries, routes, iterations, temperature, cooling_rate)
    return(min(all_costs))


