# Libraries
import matplotlib.pyplot as plt
import random
import numpy as np

def swap(routes, batteries, house_to_battery_distance, iteration, random_swap_every_x, optimization_type):
    
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
   
    # make swap if it will improve costs OR when it's time for a random swap OR when stochastic climber (random swap)
    if iteration % random_swap_every_x == 0 and swap_options or optimization_type == "stochastic_hill_climber" and swap_options or swap_options and max(swap_options, key= lambda x: x[2])[2] > 0:
        
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
        x = [house_to_extract.x, house_to_extract.x, desired_battery.x]
        y = [house_to_extract.y, desired_battery.y, desired_battery.y]
        routes[desired_battery].remove((x, y))

        # remove random house from random battery
        random_battery.remove_house(random_house)
        x = [random_house.x, random_house.x, random_battery.x]
        y = [random_house.y, random_battery.y, random_battery.y]
        routes[random_battery].remove((x, y))

        # add house to extract to random battery
        x = [house_to_extract.x, house_to_extract.x, random_battery.x]
        y = [house_to_extract.y, random_battery.y, random_battery.y]
        routes[random_battery].append((x, y))
        random_battery.add_house(house_to_extract)

        # add random house to desired battery
        desired_battery.add_house(random_house)
        x = [random_house.x, random_house.x, desired_battery.x]
        y = [random_house.y, desired_battery.y, desired_battery.y]
        routes[desired_battery].append((x,y))

    return routes

def hill_climbing(district, x_houses, y_houses, batteries, routes, house_to_battery_distance, optimization_type,iterations,random_swap_every_x, plot_grid):
    
    plot_fig = False
    colors = ['r', 'b', 'g', 'c', 'y']
    all_cable_distance = []

    for iteration in range(iterations):
        if iteration == iterations-1 and plot_grid:
            plot_fig = True

        if optimization_type == "stochastic_hill_climber" or optimization_type == "steepest_ascent_hill_climber":
            routes = swap(routes, batteries,house_to_battery_distance, iteration,random_swap_every_x, optimization_type)
        elif optimization_type == "simulated_annealing":
            # TODO: call function
            pass
        
        # if optimization_type = "none", will remain old routes
    	
        # plot batteries
        if plot_fig:
            plt.figure()

            for battery in batteries:
                plt.plot(battery.x, battery.y,
                            colors[battery.id-1]+'o', markersize=10, label='batteries')

            plt.plot(x_houses, y_houses, 'k*', label='houses')
            plt.grid()
            plt.legend(loc='upper center', ncol=10, fontsize=8)

        # calculate costs and plot houses
        cable_distance = 0
        for battery in batteries:
            for coordinates_x, coordinates_y in routes[battery]:
                
                if plot_fig:
                    plt.plot(coordinates_x, coordinates_y, colors[battery.id -1])
                
                # calculate distance
                cable_distance += abs(coordinates_x[0]-coordinates_x[2]) + abs(coordinates_y[0] - coordinates_y[2])
        
        if plot_fig:
            plt.title(f"cable distance:{cable_distance * 9}")
            plt.savefig(f"grid_{optimization_type}")
            plt.close()
        
        # append cable distance for these options
        all_cable_distance.append(cable_distance*9)

    return all_cable_distance

def create_grid(district, x_houses, y_houses, batteries, routes, house_to_battery_distance,
 optimization_type, iterations, random_swap_every_x, plot_costs, plot_grid):

    if optimization_type == "none":
        iterations = 1

    all_costs = hill_climbing(district, x_houses, y_houses, batteries, routes, house_to_battery_distance,optimization_type, 
    iterations,random_swap_every_x, plot_grid)
    print(min(all_costs))

    if plot_costs:
        plt.figure()
        plt.title(f"min_costs:{min(all_costs) * 9}")
        plt.xlabel("iteration")
        plt.ylabel("costs (distance * 9)")
        plt.plot(all_costs)
        plt.show()
        plt.savefig(f"{optimization_type}")

