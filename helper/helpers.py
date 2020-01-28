from operator import itemgetter
from math import sqrt
import matplotlib.pyplot as plt
from random import choice, sample, shuffle
import json
from node import Node



def get_houses_to_batteries_distances(district, batteries, district_nr):
    """Get all distances to all batteries for each house and pair them."""
    # houses_to_batteries_distances = {}
    # for house in district:
    #     houses_to_batteries_distances[house] = []

    #     for battery in batteries:
    #         houses_to_batteries_distances[house].append(
    #             abs(battery.x-house.x) + abs(battery.y - house.y)
    #         )
    # houses_to_batteries_distances = {house: distance for house, distance in 
    #     sorted(houses_to_batteries_distances.items(), key=lambda item: sum(item[1]), reverse=True)
    #     }
    
    houses_to_batteries_distances = []
    for house in district:
        distances = []
        for battery in batteries:
            distances.append(abs(battery.x - house.x) + abs(battery.y - house.y))
        houses_to_batteries_distances.append((house, distances))
    houses_to_batteries_distances = sorted(houses_to_batteries_distances, 
                                key=lambda item: sum(item[1]), reverse=True)
    if district_nr != 1:                
        sample_items = sample(houses_to_batteries_distances, 5)
        for item in sample_items:
            houses_to_batteries_distances.remove(item)
            houses_to_batteries_distances.append(item)
    
    return houses_to_batteries_distances

def get_houses_with_same_distance(houses_to_batteries_distances):
    houses_with_same_distance = {}
    for house, distances in houses_to_batteries_distances:
        try:
            houses_with_same_distance[sum(distances)].append(house)
        except:
            houses_with_same_distance[sum(distances)] = [house]
        
    same_distance_houses = [houses for houses in houses_with_same_distance.values() 
                            if len(houses) > 1]  

    return same_distance_houses

def get_house_pair_to_swap(houses_with_same_distance, houses_to_batteries_distances):
    i = choice(range(len(houses_with_same_distance)))
    house1, house2 = sample(houses_with_same_distance[i], 2)
    for pair in houses_to_batteries_distances:
        if pair[0] == house1:
            item1 = pair
        if pair[0] == house2:
            item2 = pair

    return (item1, item2)


def get_house_to_batteries_distances(distances):
    """Get distances to all batteries for a given house."""
    house_to_batteries_distances = {}
    for battery_nr, distance in enumerate(distances, 1):
        house_to_batteries_distances[battery_nr] = distance

    return house_to_batteries_distances

def get_coordinates(node1, node2):
    """Create a coordinate path from one node to the other, 
    with only one corner point.
    """

    return ([node1.x, node1.x, node2.x], [node1.y, node2.y, node2.y])

def get_node_coordinates(path):
    """Create a coordinate path from one node to the other, 
    for each node on the path.
    """

    x_co = []
    y_co = []
    for node in path:
        x_co.append(node.x)
        y_co.append(node.y)
    return (x_co, y_co)

def get_neighbours(x1, y1):
    """Get all neighbours for a given point on the grid."""
    DISTRICT_SIZE = 51
    neighbours = []
    feasible_points = list(range(DISTRICT_SIZE))

    change = [-1, 1]
    for delta in change:
        x = x1 + delta
        if x in feasible_points:
            node = Node(x, y1)
            neighbours.append(node)
        y = y1 + delta
        if y in feasible_points:
            node = Node(x1, y)
            neighbours.append(node)

    return neighbours

def locate_mins(open_set):
    _, h = min(open_set.items(), key=itemgetter(1))
    all_mins = []
    for node, cost in open_set.items():
        if cost == h:
            all_mins.append((node, cost))
    return all_mins

def pathfinder(start, target):
    """Create a path between to points using a Eucilian distance 
    heuristic.
    """

    path = []
    open_set = {start: sqrt((start.x - target.x)**2 + (start.y - target.y)**2) } 
    closed_set = {} 
    while True:
        current, h = min(open_set.items(), key=itemgetter(1))
        path.append(current)
        del open_set[current]
        closed_set[current] = h

        if (current.x, current.y) == (target.x, target.y):
            return path
            
        neighbours = get_neighbours(current.x, current.y)
        for neighbour in neighbours:
            if neighbour in closed_set.keys():
                continue

            if neighbour not in open_set.keys():
                open_set[neighbour] = sqrt((neighbour.x - target.x)**2 + 
                                            (neighbour.y - target.y)**2)
                
def get_manhattan_distance(point1, point2):
    """Get the manhattan distances between two points."""
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

def swap(potential_house, potential_battery,chosen_house, chosen_battery):
    """Swap two houses with each other and allocate to their new battery."""
    potential_battery.remove_house(potential_house)
    chosen_battery.remove_house(chosen_house)
    chosen_battery.add_house(potential_house)
    potential_battery.add_house(chosen_house)

def reverse_swap(potential_house, potential_battery,chosen_house, chosen_battery):
    """Swap two houses with each other and allocate to their new battery.
    In doing so, reverse the initial swap."""

    potential_battery.remove_house(chosen_house)
    chosen_battery.remove_house(potential_house)
    chosen_battery.add_house(chosen_house)
    potential_battery.add_house(potential_house)
