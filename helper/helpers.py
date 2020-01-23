from operator import itemgetter
from math import sqrt
import matplotlib.pyplot as plt
from random import choice
from node import Node

def get_houses_to_batteries_distances(district, batteries):
    houses_to_batteries_distances = {}
    for house in district:
        houses_to_batteries_distances[house] = []

        for battery in batteries:
            houses_to_batteries_distances[house].append(
                abs(battery.x-house.x) + abs(battery.y - house.y)
            )
    houses_to_batteries_distances = {house: distance for house, distance in 
        sorted(houses_to_batteries_distances.items(), key=lambda item: sum(item[1]), reverse=True)
        }
    
    # house, distances = choice(tuple(houses_to_batteries_distances.items()))
    # print(house)
    # del houses_to_batteries_distances[house]
    # houses_to_batteries_distances[house] = distances

    return houses_to_batteries_distances

def get_house_to_batteries_distances(distances):
    house_to_batteries_distances = {}
    for battery_nr, distance in enumerate(distances, 1):
        house_to_batteries_distances[battery_nr] = distance

    return house_to_batteries_distances

def get_coordinates(node1, node2):
    return ([node1.x, node1.x, node2.x], [node1.y, node2.y, node2.y])

def get_node_coordinates(path):
    x_co = []
    y_co = []
    for node in path:
        x_co.append(node.x)
        y_co.append(node.y)
    return (x_co, y_co)

def get_neighbours(x1, y1):
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
    path = []
    open_set = {start: sqrt((start.x - target.x)**2 + (start.y - target.y)**2) } # nodes to be evaluated # h = distance from end node
    closed_set = {} # nodes already evaluated
    while True:
        current, h = min(open_set.items(), key=itemgetter(1))
        # all_options = locate_mins(open_set)
        # current, h = choice(all_options)
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
                open_set[neighbour] = sqrt((neighbour.x - target.x)**2 + (neighbour.y - target.y)**2)
                
def get_manhattan_distance(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

def swap(potential_house, potential_battery,chosen_house, chosen_battery):
    potential_battery.remove_house(potential_house)
    chosen_battery.remove_house(chosen_house)
    chosen_battery.add_house(potential_house)
    potential_battery.add_house(chosen_house)

def reverse_swap(potential_house, potential_battery,chosen_house, chosen_battery):

    potential_battery.remove_house(chosen_house)
    chosen_battery.remove_house(potential_house)
    chosen_battery.add_house(chosen_house)
    potential_battery.add_house(potential_house)

