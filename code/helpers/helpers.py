from operator import itemgetter
from math import sqrt
import math
import matplotlib.pyplot as plt
from random import choice, sample, shuffle
from node import Node
import random
import numpy as np
from sklearn.cluster import KMeans


def get_houses_to_batteries_distances(district, batteries, district_nr):
    """
    Get all distances to all batteries for each house and pair them.
    """

    houses_to_batteries_distances = []
    for house in district:
        distances = []
        for battery in batteries:
            distances.append(abs(battery.x - house.x) +
                             abs(battery.y - house.y))
        houses_to_batteries_distances.append((house, distances))
    houses_to_batteries_distances = sorted(houses_to_batteries_distances,
                                           key=lambda item: sum(item[1]), reverse=True)
    if district_nr != 1:
        sample_items = sample(houses_to_batteries_distances, 5)
        for item in sample_items:
            houses_to_batteries_distances.remove(item)
            houses_to_batteries_distances.append(item)

    return houses_to_batteries_distances


def get_house_to_batteries_distances(distances):
    """
    Get distances to all batteries for a given house.
    """

    house_to_batteries_distances = {}
    for battery_nr, distance in enumerate(distances, 1):
        house_to_batteries_distances[battery_nr] = distance

    return house_to_batteries_distances


def get_coordinates(node1, node2):
    """
    Create a coordinate path from one node to the other, 
    with only one corner point.
    """

    return ([node1.x, node1.x, node2.x], [node1.y, node2.y, node2.y])


def get_node_coordinates(path):
    """
    Create a coordinate path from one node to the other, 
    for each node on the path.
    """

    x_co = []
    y_co = []
    for node in path:
        x_co.append(node.x)
        y_co.append(node.y)
    return (x_co, y_co)


def get_neighbours(x1, y1):
    """
    Get all neighbours for a given point on the grid.
    Only allow for adjacent neighbours.
    """

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


def pathfinder(start, target):
    """
    Create a path between to points using a Eucilian distance 
    heuristic.
    """

    path = []
    open_set = {start: sqrt((start.x - target.x)**2 + (start.y - target.y)**2)}
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


def get_distance(point1, point2):
    """
    Get the manhattan distances between two points.
    """

    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


def get_distance_cluster(cluster, battery):
    """
    Get the manhattan distances between two points.
    """

    return math.sqrt(((cluster[0]-battery.x)**2)+((cluster[1]-battery.y)**2))


def swap(potential_house, potential_battery, chosen_house, chosen_battery):
    """
    Swap two houses with each other and allocate to their new battery.
    """

    potential_battery.remove_house(potential_house)
    chosen_battery.remove_house(chosen_house)
    chosen_battery.add_house(potential_house)
    potential_battery.add_house(chosen_house)


def reverse_swap(potential_house, potential_battery, chosen_house, chosen_battery):
    """
    Swap two houses with each other and allocate to their new battery.
    In doing so, reverse the initial swap.
    """

    potential_battery.remove_house(chosen_house)
    chosen_battery.remove_house(potential_house)
    chosen_battery.add_house(chosen_house)
    potential_battery.add_house(potential_house)


def get_random_batteries(district):
    """
    Choose a combination from the battery types 
    that satisfy the total usage from a district.
    """

    batteries = []

    total_usage = 0
    for house in district:
        total_usage += house.power

    battery_types = {"PowerStar": {"capacity": 450, "price": 900}, "Imerse-II": {
        "capacity": 900, "price": 900}, "Imerse-III": {"capacity": 1800, "price": 1800}}

    battery = random.choice(list(battery_types.items()))

    while total_usage >= 0:
        batteries.append(battery)
        total_usage -= battery[1]['capacity']
        battery = random.choice(list(battery_types.items()))

    return batteries

    # Choose random battery till capacity exceeds total district usage
    while total_usage >= 0:
        batteries.append(battery)
        # Subtract capacity of added battery from total usage
        total_usage -= battery[1]['capacity']
        # Choose new randopm battery
        battery = random.choice(list(battery_types.items()))

    return batteries


def get_clusters(district, batteries):
    """
    Create clusters based on the amount of batteries. The district data
    will be transformed into points that are used as input for K-Means clustering.
    """

    points = []
    for house in district:
        coordinate = [house.x, house.y]
        points.append(coordinate)
    points = np.array(points)

    # Create a kmeans object
    kmeans = KMeans(n_clusters=len(batteries))

    # Fit the kmeans object to the dataset
    labels = kmeans.fit_predict(points)

    clusters = kmeans.cluster_centers_.astype(int)

    return labels, clusters


def check(house, remaining_house, random_battery, battery):
    """Return True if combination of houses and batteries allow
    for a swap. Return False otherwise"""

    if remaining_house.power < battery.capacity + house.power:
        go_on = True
    if go_on:
        if house.power < random_battery.capacity:
            return True
    return False
