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
    def __init__(self, type_of_config, district_nr, share_grid, advanced):
        self.type = type_of_config
        self.district_nr = district_nr
        self.share_grid = share_grid
        self.district = []
        self.get_district()
        self.batteries = []
        self.get_batteries(advanced)
        self.get_configuration()
        self.routes = {}

    def get_district(self):
        """Retrieve all houses from csv and create district with house objects."""

        # open and read the csv file
        f = open(f'data/district{self.district_nr}_houses.csv')
        district_data = csv.reader(f)
        next(district_data)

        # create an object for each house
        for house_id, row in enumerate(district_data, 1):
            x, y = eval(row[0]), eval(row[1])
            power = eval(row[2])
            house = House(house_id, x, y, power)
            self.district.append(house)
    
    def get_batteries(self, advanced): 
        """Retrieve batteries from csv and create battery objects."""

        if advanced == True:
            random_batteries = get_random_batteries(self.district)
            labels, points, clusters = get_clusters(self.district, random_batteries)
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
            # open and read the csv file
            f = open(f'data/district{self.district_nr}_batteries.csv')
            batteries_data = csv.reader(f)
            next(batteries_data)

            # create an object for each battery
            for battery_id, row in enumerate(batteries_data, 1):
                x, y = eval(row[0])[0], eval(row[0])[1]
                capacity = eval(row[1])
                battery = Battery(battery_id, x, y, capacity)

                self.batteries.append(battery)

    def get_configuration(self):
        """Get configuration depending on the type of configuration."""

        if self.type == "random":
            self.random_algo()
        elif self.type == "greedy":
            if self.district_nr != 1:
                while True:
                    for battery in self.batteries:
                        battery.restore()
                    self.greedy_algo()
                    nrs = 0
                    for battery in self.batteries:
                        nrs += len(battery.houses)
                    if nrs == 150:
                        print("Found allocation")
                        break
            else:
                self.greedy_algo()
            
        else: # if type = "cluster"
            self.cluster_algo()
        
    def random_algo(self):
        """Randomly allocate 30 houses to the 5 batteries until solution is 
        feasible. """

        HOUSES_PER_BATTERY = 30
        t = time.time()
        while True:
            all_houses = copy.deepcopy(self.district)
            
            for battery in self.batteries:
                battery.restore()

            while all_houses:
                for battery in self.batteries:
                    sample_of_houses = random.sample(all_houses, HOUSES_PER_BATTERY)
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
                s = abs(t - time.time())
                print(f"Took {s} seconds to find solution")
                break

    def cluster_algo(self):
        while True:
            labels, points, clusters = get_clusters(self.district, self.batteries)

            # Get the clostest batteries to a cluster centroid
            distance_cluster_to_batteries = {}
            
            for cluster in range(len(self.batteries)):
                distance_cluster_to_batteries[cluster] = {}
                for battery in self.batteries:
                    distance = math.sqrt(
                        ((clusters[cluster][0]-battery.x)**2)+((clusters[cluster][1]-battery.y)**2))
                    distance_cluster_to_batteries[cluster][battery] = distance

                # Sort the batteries distances of a cluster from closest to furthest
                distance_cluster_to_batteries[cluster] = {k: v for k, v in sorted(
                    distance_cluster_to_batteries[cluster].items(), key=lambda item: item[1])}

                # Filter the houses to contain only the house of the cluster
                houses_in_cluster = [x for x, y in zip(
                    self.district, labels) if y == cluster]

                # Sort houses per cluster that are furthest away from all suboptimal batteries
                suboptimal_battery_distance = {}
                # Battery closest to cluster (optimal battery)
                optimal_battery = list(
                    distance_cluster_to_batteries[cluster].keys())[0]
                # Calculate distance from house to battery and add it to the dictionary
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

                # Iterate over the houses and assign the house furthest away from the suboptimal batteries first to the optimal battery
                for house in houses_in_cluster_sorted:
                        y = 0
                        while True:
                            # Select battery closest to district
                            battery = list(distance_cluster_to_batteries[cluster].keys())[y]
                            # check if capacity fits the usage
                            if battery.capacity - house.power >= 0:
                                battery.add_house(house)
                                break
                            else:
                                # update feasible battery distances
                                y += 1
                                if y > len(self.batteries)-1:
                                    limit_exceeded = True
                                    break
            amount = 0
            for battery in self.batteries:
                for house in battery.houses:
                    amount += 1
            if amount == len(self.district):
                return True
        


    def greedy_algo(self):
    
        houses_to_batteries_distances = get_houses_to_batteries_distances(self.district, self.batteries, self.district_nr)
        
        # for house, distances in houses_to_batteries_distances.items():
        for house, distances in houses_to_batteries_distances:
            house_to_batteries_distances = get_house_to_batteries_distances(distances)

            while True:
                
                battery_nr = min(house_to_batteries_distances, key=house_to_batteries_distances.get)
                battery = self.batteries[battery_nr - 1]

                if battery.capacity - house.power >= 0:
                    battery.add_house(house)
                    break

                else:
                    # update feasible battery distances
                    del house_to_batteries_distances[battery_nr]
                    if not house_to_batteries_distances:
                        # now we know that no batteries have room for this house
                        if self.district_nr == 1:
                            self.update_configuration(house, distances)
                            break
                        else:
                            return 1
                        
    def update_configuration(self, house, distances):

        remaining_house = house

        remaining_capacity = {}
        for battery_nr, battery in enumerate(self.batteries, 1):
            remaining_capacity[battery_nr] = battery.capacity

        house_to_batteries_distances = get_house_to_batteries_distances(distances)
        
        max_capacity_battery_nr = max(remaining_capacity, key=remaining_capacity.get)
        max_capacity_battery = self.batteries[max_capacity_battery_nr - 1]       

        swap_options = []
        while not swap_options:
            try:
                desired_battery_nr = min(house_to_batteries_distances, key=house_to_batteries_distances.get)
                desired_battery = self.batteries[desired_battery_nr - 1]
                del house_to_batteries_distances[desired_battery_nr] 
            except:
                exit
               
            for house in desired_battery.houses:
                if house.power < remaining_capacity[max_capacity_battery_nr] and house.power + remaining_capacity[desired_battery_nr] > remaining_house.power:
                    # save these houses and the costs of swapping
                    distance_desired = abs(house.x - desired_battery.x) + abs(house.y - desired_battery.y)
                    distance_max_capacity = abs(house.x - max_capacity_battery.x) + abs(house.y - max_capacity_battery.y)
                    distance_difference = distance_max_capacity - distance_desired
                    swap_options.append((house, distance_difference))
                
        # check lowest cost for swapping and swap
        house_to_extract = min(swap_options, key=lambda x: x[1])[0]

        # house swaps
        desired_battery.remove_house(house_to_extract)
        desired_battery.add_house(remaining_house)
        max_capacity_battery.add_house(house_to_extract)

    def make_plot(self, results_directory, optimization):
        save_name_grid = f"{self.type}_{self.district_nr}_{optimization}"
        colors = ['yellowgreen', 'yellow', 'violet', 'tomato', 'turquoise', 'sienna','blue', 'pink', 'teal', 'tan']
        
        plt.figure()
        for battery in self.batteries:
            plt.plot(battery.x, battery.y, 'H', color=colors[battery.id -1])
            for house in battery.houses:
                plt.plot(house.x, house.y, 'k*')

        if self.share_grid == False:
            self.get_routes()
            # get costs? 
            i = 0
            for battery in self.batteries:
                for x, y in self.routes[battery]:
                    plt.plot(x, y, colors[i])
                i += 1
            
            costs = 0
            for battery in self.batteries:
                for house in battery.houses:
                    costs += (abs(house.x - battery.x) + abs(house.y - battery.y)) * 9
            plt.title(f"Total costs:{costs}")

        else:
            i = 0
            prim = Prim(self.batteries)
            for mst in prim.mst_container:
                for branch in mst.keys():
                    plt.plot(branch.path[0], branch.path[1], colors[i])
                i += 1
            plt.title(f"Total costs: {prim.costs}")
            

        plt.xlim(-2, 55)
        plt.ylim(-2, 55)
        plt.savefig(results_directory + save_name_grid)
        plt.show()

    def get_routes(self, share_grid = False):
        for battery in self.batteries:
            self.routes[battery] = []
            for house in battery.houses:
                A = get_coordinates(house, battery)
                self.routes[battery].append(A) 


    
    
    