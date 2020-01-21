import copy
import time
import matplotlib.pyplot as plt
import random
from prim import prim
from test import super_random

def get_distances(distances):
    distances_dic = {}
    for battery_nr, distance in enumerate(distances, 1):
        distances_dic[battery_nr] = distance
    return distances_dic

def get_coordinates(node1, node2):
    return ([node1.x, node1.x, node2.x], [node1.y, node2.y, node2.y])

def get_random_houses(district, batteries):
    random_houses = []
    
    for i in range(150):
        house = random.choice(district)
        index_house = district.index(house)
        random_houses.append(house)
        # delete house
        del district[index_house]
        
    return random_houses

def update_routes(house, batteries, routes):
    remaining_house = house

    remaining_capacity = {}
    for battery_nr, battery in enumerate(batteries, 1):
        remaining_capacity[battery_nr] = battery.capacity
    
    max_capacity_battery_nr = max(remaining_capacity, key=remaining_capacity.get)
    max_capacity_battery = batteries[max_capacity_battery_nr - 1]

    swap_options = []
    all_battery_nr = [1,2,3,4,5]
    fail = False
    while not swap_options:
        if not all_battery_nr:
            fail = True
            return routes, fail
        desired_battery_nr = random.choice(all_battery_nr)
        index_batt = all_battery_nr.index(desired_battery_nr)

        desired_battery = batteries[desired_battery_nr - 1]
        del all_battery_nr[index_batt] 

        for house in desired_battery.houses:
            if house.usage < remaining_capacity[max_capacity_battery_nr] and house.usage + remaining_capacity[desired_battery_nr] > remaining_house.usage:
                # save these houses and the costs of swapping
                distance_desired = abs(house.x - desired_battery.x) + abs(house.y - desired_battery.y)
                distance_max_capacity = abs(house.x - max_capacity_battery.x) + abs(house.y - max_capacity_battery.y)
                distance_difference = distance_max_capacity - distance_desired
                swap_options.append((house, distance_difference))
            
    # check lowest cost for swapping and swap
    house_to_extract = random.choice(swap_options)[0]

    # house swaps
    desired_battery.remove_house(house_to_extract)
    desired_battery.add_house(remaining_house)
    max_capacity_battery.add_house(house_to_extract)

    # routes updates
    x, y = get_coordinates(house_to_extract, desired_battery)
    routes[desired_battery].remove((x, y))

    x, y = get_coordinates(remaining_house, desired_battery)
    routes[desired_battery].append((x,y))

    x, y = get_coordinates(house_to_extract, max_capacity_battery)
    routes[max_capacity_battery].append((x, y))

    return routes, fail
    
def get_routes(batteries, random_houses):

    routes = {}
    for battery in batteries:
        routes[battery] = []

    start_again = False

    while start_again == False:
        for house in random_houses:
            while True:
                # random battery
                all_battery_nr = [1,2,3,4,5]
                battery_nr = random.choice(all_battery_nr)
                battery = batteries[battery_nr - 1] 

                # check if capacity fits the usage
                if battery.capacity - house.usage >= 0:
                    battery.add_house(house) 

                    # save x and y coordinates from house to battery
                    x, y = get_coordinates(house, battery)
                    routes[battery].append((x, y))
                    break
                else:
                    # update feasible battery distances
                    routes, fail = update_routes(house, batteries, routes)
                    # when cannot place house, start over
                    if fail:
                        print("fail")
                        start_again = True
                        break

                    # now we know that no batteries have room for this house
                    break
    return routes
            

def rand_import_routes(district, batteries):
    # random_houses = get_random_houses(district, batteries)
    # routes = get_routes(batteries, random_houses)
    super_random(district, batteries)
    # colors = ['r', 'b', 'k', 'g', 'm']

    # for i in range(5):
    #     plt.figure()
    #     battery = batteries[i]
    #     for house in battery.houses:
    #         plt.plot(battery.x, battery.y, 'H')
    #         plt.plot(house.x, house.y, 'k*')
    #     mst = prim(battery)
    #     for branch in mst.keys():
    #         plt.plot(branch.path[0], branch.path[1], colors[i])
    #     plt.savefig(f"Battery{i+1} with random allocation")

    
    
    # i = 0
    # plt.figure()

    # for battery in batteries:
    #     for house in battery.houses:
    #         plt.plot(battery.x, battery.y, 'H')
    #         plt.plot(house.x, house.y, 'k*')
    #     mst = prim(battery)
    
    #     for branch in mst.keys():
    #         plt.plot(branch.path[0], branch.path[1], colors[i])
    #     i += 1
        
    # plt.xlim(-2, 55)
    # plt.ylim(-2, 55)
    # plt.show()

    # return routes
    