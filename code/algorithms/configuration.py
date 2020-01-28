from house import House
from battery import Battery
from prim import Prim
from helpers import *

import csv
import copy
import math
import random
import matplotlib.pyplot as plt
import time


class Configuration():
    """
    This class is devoted to finding a solution through several algorithms.

    It will first load all data from thecsv files and depending on its parameters, 
    Configuration finds different solutions that can then be optimized further.
    """

    def __init__(self, type_of_config, district_nr, share_grid, advanced):
        self.type = type_of_config
        self.district_nr = district_nr
        self.share_grid = share_grid
        self.advanced = advanced
        self.routes = {}
        self.district = []
        self.get_district()
        self.batteries = []
        self.get_batteries()
        self.get_configuration()

    def get_district(self):
        """
        Retrieve all houses from csv and create district with house objects.
        """

        f = open(f'data/district{self.district_nr}_houses.csv')
        district_data = csv.reader(f)
        next(district_data)

        for house_id, row in enumerate(district_data, 1):
            x, y = eval(row[0]), eval(row[1])
            power = eval(row[2])
            house = House(house_id, x, y, power)
            self.district.append(house)

    def get_batteries(self):
        """
        Retrieve batteries from csv and create battery objects.
        """

        if self.advanced == True:
            random_batteries = get_random_batteries(self.district)
            labels, clusters = get_clusters(
                self.district, random_batteries)
            clusters = clusters.tolist()
            for battery_id, battery in enumerate(random_batteries, 1):
                cluster = random.choice(clusters)
                clusters.remove(cluster)
                x = cluster[0]
                y = cluster[1]
                capacity = battery[1]["capacity"]
                cost = battery[1]["price"]
                b = Battery(battery_id, x, y, capacity, cost)
                self.batteries.append(b)
        else:
            f = open(f'data/district{self.district_nr}_batteries.csv')
            batteries_data = csv.reader(f)
            next(batteries_data)

            for battery_id, row in enumerate(batteries_data, 1):
                x, y = eval(row[0])[0], eval(row[0])[1]
                capacity = eval(row[1])
                battery = Battery(battery_id, x, y, capacity)

                self.batteries.append(battery)

    def get_configuration(self):
        """
        Get configuration depending on the type of configuration.
        """

        if self.type == "random":
            self.random_algo()
        elif self.type == "greedy":
            if self.district_nr != 1:
                while True:
                    for battery in self.batteries:
                        battery.restore()
                    self.greedy_algo()
                    if self.is_feasible_solution():
                        break
            else:
                self.greedy_algo()
        else:
            self.cluster_algo()

    def random_algo(self):
        """
        Randomly allocate 30 houses to 5 batteries until solution is feasible.
        """

        HOUSES_PER_BATTERY = 30
        while True:
            all_houses = copy.deepcopy(self.district)

            for battery in self.batteries:
                battery.restore()

            while all_houses:
                for battery in self.batteries:
                    sample_of_houses = random.sample(
                        all_houses, HOUSES_PER_BATTERY)
                    for house in sample_of_houses:
                        all_houses.remove(house)

                    for house in sample_of_houses:
                        battery.add_house(house)

            satisfing_constraints = []
            for battery in self.batteries:
                if battery.capacity < 0:
                    satisfing_constraints.append(False)
                else:
                    satisfing_constraints.append(True)

            if all(satisfing_constraints):
                break

    def cluster_algo(self):
        """Use K-means to group houses into clusters. 
        
        These clusters are assigned to the optimal battery.
        The houses in the clusters are sorted by the sum of the 
        distance to the suboptimal batteries. The algorithms keeps 
        running untill all houses are assigned to a battery.
        """

        while True:
            labels, clusters = get_clusters(
                self.district, self.batteries)

            distance_cluster_to_batteries = {}

            for cluster in range(len(self.batteries)):
                distance_cluster_to_batteries[cluster] = {}
                for battery in self.batteries:
                    distance = get_distance_cluster(clusters[cluster], battery)
                    distance_cluster_to_batteries[cluster][battery] = distance

                distance_cluster_to_batteries[cluster] = {k: v for k, v in sorted(
                    distance_cluster_to_batteries[cluster].items(), key=lambda item: item[1])}

                houses_in_cluster = [x for x, y in zip(
                    self.district, labels) if y == cluster]

                suboptimal_battery_distance = {}

                optimal_battery = list(
                    distance_cluster_to_batteries[cluster].keys())[0]

                for house in houses_in_cluster:
                    suboptimal_battery_distance[house] = {}
                    total_distance = 0
                    for battery in self.batteries:
                        if battery != optimal_battery:
                            total_distance += math.sqrt(
                                ((house.x-battery.x)**2)+((house.y-battery.y)**2))
                    suboptimal_battery_distance[house] = total_distance

                houses_in_cluster_sorted = {k: v for k, v in sorted(
                    suboptimal_battery_distance.items(), key=lambda item: item[1], reverse=True)}

                for house in houses_in_cluster_sorted:
                    index = 0
                    while True:
                        battery = list(
                            distance_cluster_to_batteries[cluster].keys())[index]
                        if battery.capacity - house.power >= 0:
                            battery.add_house(house)
                            break
                        else:
                            index += 1
                            if index > len(self.batteries)-1:
                                break

            amount = 0
            for battery in self.batteries:
                for house in battery.houses:
                    amount += 1
            if amount == len(self.district):
                return True

    def greedy_algo(self):
        """Allocate all houses to batteries.

        Start with the houses that have the greatest total 
        distance to the batteries and go from there. If 
        allocation is not possible, update configuration or
        start over.
        """

        houses_to_batteries_distances = get_houses_to_batteries_distances(
            self.district,
            self.batteries,
            self.district_nr)

        for house, distances in houses_to_batteries_distances:
            house_to_batteries_distances = get_house_to_batteries_distances(
                distances)

            while True:
                battery_nr = min(house_to_batteries_distances,
                                 key=house_to_batteries_distances.get)
                battery = self.batteries[battery_nr - 1]

                if battery.capacity - house.power >= 0:
                    battery.add_house(house)
                    break
                else:
                    # update feasible battery distances
                    del house_to_batteries_distances[battery_nr]
                    if not house_to_batteries_distances:
                        if self.district_nr == 1:
                            self.update_configuration(house, distances)
                            break
                        else:
                            return 1

    def update_configuration(self, house, distances):
        """
        Find a battery for de remaining house.
        """

        remaining_house = house
        while remaining_house:
            random_battery = choice(self.batteries)
            for battery in self.batteries:
                if battery == random_battery:
                    continue
                for house in battery.houses:

                    swap_possible = check(house, remaining_house,
                                          random_batttery, battery)
                    if swap_possible:
                        battery.remove_house(house)
                        battery.add_house(remaining_house)
                        random_battery.add_house(house)
                        remaining_house = None

    def make_plot(self, results_directory, optimization):
        """
        Make plot based on given configuration and whether 
        or not grid lines can be shared.
        """

        figure_name = f"{self.type}_{self.district_nr}_{optimization}"
        colors = ['yellowgreen',
                  'yellow', 'violet',
                  'tomato', 'turquoise',
                  'sienna', 'blue', 'pink',
                  'teal', 'tan']

        plt.figure()
        for battery in self.batteries:
            plt.plot(battery.x, battery.y, 'H', color=colors[battery.id - 1])
            for house in battery.houses:
                plt.plot(house.x, house.y, 'k*')

        costs = 0
        if self.share_grid == False:
            self.get_routes()
            i = 0
            for battery in self.batteries:
                for x, y in self.routes[battery]:
                    plt.plot(x, y, colors[i])
                i += 1

            for battery in self.batteries:
                for house in battery.houses:
                    costs += (abs(house.x - battery.x) +
                              abs(house.y - battery.y)) * 9
                costs += battery.costs
            plt.title(f"Total costs:{costs}")

        else:
            i = 0
            prim = Prim(self.batteries)

            for battery in self.batteries:
                costs += battery.costs

            for mst in prim.mst_container:
                for branch in mst.keys():
                    plt.plot(branch.path[0], branch.path[1], colors[i])
                i += 1
            plt.title(f"Total costs: {prim.costs + costs}")

        plt.xlim(-2, 55)
        plt.ylim(-2, 55)
        plt.savefig(results_directory + figure_name)
        plt.show()

    def get_routes(self):
        """
        Get all routes from batteries to houses for a 
        given configuration when grid lines have to be unique.
        """

        for battery in self.batteries:
            self.routes[battery] = []
            for house in battery.houses:
                coordinate = get_coordinates(house, battery)
                self.routes[battery].append(coordinate)

    def is_feasible_solution(self):
        """
        Return True if given allocation is feasible, 
        False otherwise.
        """

        capacity = []
        nrs = 0
        for battery in self.batteries:
            nrs += len(battery.houses)
            capacity.append(battery.capacity)
        if nrs == 150 and all(capacity):
            return True
        return False
