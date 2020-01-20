import copy
import time
import matplotlib.pyplot as plt
from prim import prim

def get_distances(distances):
    distances_dic = {}
    for battery_nr, distance in enumerate(distances, 1):
        distances_dic[battery_nr] = distance
    return distances_dic

def get_coordinates(node1, node2):
    return ([node1.x, node1.x, node2.x], [node1.y, node2.y, node2.y])

def get_house_to_batteries_distances(district, batteries):
    house_to_batteries_distances = {}
    for house in district:
        house_to_batteries_distances[house] = []

        for battery in batteries:
            house_to_batteries_distances[house].append(
                abs(battery.x-house.x) + abs(battery.y - house.y)
            )
    house_to_batteries_distances = {house: distance for house, distance in 
        sorted(house_to_batteries_distances.items(), key=lambda item: sum(item[1]), reverse=True)
        }
        
    return house_to_batteries_distances

def update_routes(house, batteries, distances, routes):
    remaining_house = house

    remaining_capacity = {}
    for battery_nr, battery in enumerate(batteries, 1):
        remaining_capacity[battery_nr] = battery.capacity

    distances_dic = get_distances(distances)
    
    max_capacity_battery_nr = max(remaining_capacity, key=remaining_capacity.get)
    max_capacity_battery = batteries[max_capacity_battery_nr - 1]

    swap_options = []
    while not swap_options:
        desired_battery_nr = min(distances_dic, key=distances_dic.get)
        desired_battery = batteries[desired_battery_nr - 1]
        del distances_dic[desired_battery_nr] # TODO: MISSCHIEN EEN TRY-EXCEPT

        for house in desired_battery.houses:
            if house.usage < remaining_capacity[max_capacity_battery_nr] and house.usage + remaining_capacity[desired_battery_nr] > remaining_house.usage:
                # save these houses and the costs of swapping
                distance_desired = abs(house.x - desired_battery.x) + abs(house.y - desired_battery.y)
                distance_max_capacity = abs(house.x - max_capacity_battery.x) + abs(house.y - max_capacity_battery.y)
                distance_difference = distance_max_capacity - distance_desired
                swap_options.append((house, distance_difference))
            
    # check lowest cost for swapping and swap
    house_to_extract = min(swap_options, key= lambda x: x[1])[0]

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

    return routes
    
def get_routes(batteries, house_to_batteries_distances):

    routes = {}
    for battery in batteries:
        routes[battery] = []

    for house, distances in house_to_batteries_distances.items():
        
        distances_dic = get_distances(distances)

        while True:
            # select the route with the smallest distance from house to battery

            battery_nr = min(distances_dic, key=distances_dic.get)
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
                del distances_dic[battery_nr]
                if not distances_dic:
                    routes = update_routes(house, batteries, distances, routes)
                    # now we know that no batteries have room for this house
                    break
    return routes
            

def import_routes(district, batteries):
    house_to_batteries_distances = get_house_to_batteries_distances(district, batteries)
    routes = get_routes(batteries, house_to_batteries_distances)
    colors = ['r', 'b', 'k', 'g', 'm']
    
    i = 0
    # plt.figure()
    all_totals = []
    for j in range(100): 
        total = 0
        for battery in batteries:
            # for house in battery.houses:
            #     plt.plot(battery.x, battery.y, 'H')
            #     plt.plot(house.x, house.y, 'k*')
            mst = prim(battery)
    
            for val in mst.values():
                total += val
        
            # for branch in mst.keys():
            #     plt.plot(branch.path[0], branch.path[1], colors[i])
            # i += 1
            
        all_totals.append(total)
    # plt.xlim(-2, 55)
    # plt.ylim(-2, 55)
    # plt.show()
    print(all_totals)
    plt.figure()
    plt.hist(all_totals, bins=50)
    plt.show()
    return routes
    