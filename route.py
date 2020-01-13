import numpy as np
import copy


def get_distances(distances):
    distances_dic = {}
    for battery_nr, distance in enumerate(distances, 1):
        distances_dic[battery_nr] = distance
    return distances_dic


class Route:
    def __init__(self):
        self.routes = {}
        self.cable = 0

    def get_house_to_batteries_distances(self, district, batteries):
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

    def set_routes(self, batteries, house_to_batteries_distances):
   
        for battery in batteries:
            self.routes[battery] = []


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
                    x = [house.x, house.x, battery.x]
                    y = [house.y, battery.y, battery.y]

                    self.routes[battery].append((x, y))
                    
                    break
                else:
                    # update feasible battery distances
                    del distances_dic[battery_nr]
                    if not distances_dic:
                        # now we know that no batteries have room for this house
                        remaining_house = house 
                        remaining_capacity = {}
                        for battery_nr, battery in enumerate(batteries, 1):
                            remaining_capacity[battery_nr] = battery.capacity

                        distances_dic = get_distances(distances)
                        
                        desired_battery_nr = min(distances_dic, key=distances_dic.get)
                        desired_battery = batteries[desired_battery_nr - 1]

                        max_capacity_battery_nr = max(remaining_capacity, key=remaining_capacity.get)
                        max_capacity_battery = batteries[max_capacity_battery_nr - 1]

                        swap_options = []
                        for house in desired_battery.houses:
                            if house.usage < remaining_capacity[max_capacity_battery_nr] and house.usage + remaining_capacity[desired_battery_nr] > remaining_house.usage:
                                # save these houses and the costs of swapping
                                distance_desired = abs(house.x - desired_battery.x) + abs(house.y - desired_battery.y)
                                distance_max_capacity = abs(house.x - max_capacity_battery.x) + abs(house.y - max_capacity_battery.y)
                                distance_difference = distance_max_capacity - distance_desired
                                swap_options.append((house, distance_difference))
                            # check lowest cost for swapping and swap
                        print(swap_options)

                        house_to_extract = min(swap_options, key= lambda x: x[1])[0]
                        print(house_to_extract)
                        print(remaining_capacity, remaining_house.id)
                        print(distances)

                        desired_battery.remove_house(house_to_extract)
                        x = [house_to_extract.x, house_to_extract.x, desired_battery.x]
                        y = [house_to_extract.y, desired_battery.y, desired_battery.y]
                        self.routes[desired_battery].remove((x, y))

                        x = [house_to_extract.x, house_to_extract.x, max_capacity_battery.x]
                        y = [house_to_extract.y, max_capacity_battery.y, max_capacity_battery.y]
                        self.routes[max_capacity_battery].append((x, y))

                        max_capacity_battery.add_house(house_to_extract)
                        desired_battery.add_house(remaining_house)
                        x = [remaining_house.x, remaining_house.x, max_capacity_battery.x]
                        y = [remaining_house.y, max_capacity_battery.y, max_capacity_battery.y]
                        self.routes[desired_battery].append((x,y))
                        
                        nr = 0
                        for battery in batteries:
                            nr += len(battery.houses)
                        print(nr)
                        return 0
    

    def delete_duplicates():
        # TODO Delete coordinates that are duplicated if a line is shared with another battery line, change the color to a uniform color like black.
        pass

    def cable_costs(self):
        pass

    def import_routes(self, district, batteries):
        house_to_batteries_distances = self.get_house_to_batteries_distances(district, batteries)
        self.set_routes(batteries, house_to_batteries_distances)
        return self.routes