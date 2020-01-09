import numpy as np
import copy

class Route:
    def __init__(self):
        self.routes = {}
        self.cable = 0

    def get_house_to_batteries_distances(self, district, batteries):
        # all_distances = {}
        # for house in district:
        #     all_distances[house] = []

        #     for battery in batteries:
        #         all_distances[house].append(
        #             (abs(battery.x-house.x) + abs(battery.y - house.y)))
        # sorted_list = sorted(
        #     all_distances.items(), key=lambda x: sum(x[1]), reverse=True)
        # print(sorted_list)
        # return sorted_list
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
        # for battery in batteries:
        #     self.routes[battery] = []
        #     # last_house = list(house_to_batteries_distances.keys())[-1]
        #     # print(last_house)
        # for house, distances in house_to_batteries_distances.items():

        #     # add house to battery
        #     while True:
        #         # select the route with the smallest distance from house to battery
                
        #         battery_index = distances.index(np.nanmin(distances))
        #         battery = batteries[battery_index]

        #         # check if capacity fits the usage
        #         if battery.capacity - house.usage >= 0:
        #             battery.add_house(house) 
        #             # x and y coordinates from house to battery
        #             x = [house.x, house.x, battery.x]
        #             y = [house.y, battery.y, battery.y]

        #             self.routes[battery].append((x, y))
                    
        #             break
        #         else:
        #             distances[battery_index] = np.nan
        #             if all(np.isnan(distances)):
        #                 pass
        for battery in batteries:
            self.routes[battery] = []
            # last_house = list(house_to_batteries_distances.keys())[-1]
            # print(last_house)
        for house, distances in house_to_batteries_distances.items():

            distances_dic = {}
            for battery_nr, distance in enumerate(distances, 1):
                distances_dic[battery_nr] = distance 
    
            while True:
                # select the route with the smallest distance from house to battery

                battery_nr = min(distances_dic, key=distances_dic.get)
                battery = batteries[battery_nr - 1] 

                # check if capacity fits the usage
                if battery.capacity - house.usage >= 0:
                    battery.add_house(house) 
                    # x and y coordinates from house to battery
                    x = [house.x, house.x, battery.x]
                    y = [house.y, battery.y, battery.y]

                    self.routes[battery].append((x, y))
                    
                    break
                else:
                    # update feasible battery distances
                    del distances_dic[battery_nr]
                    # distances = [distance for i, distance in enumerate(distances) if i in index_possibilities]
                    # print(distances)


    def delete_duplicates():
        # TODO Delete coordinates that are duplicated if a line is shared with another battery line, change the color to a uniform color like black.
        pass

    def cable_costs(self):
        pass

    def import_routes(self, district, batteries):
        house_to_batteries_distances = self.get_house_to_batteries_distances(district, batteries)
        self.set_routes(batteries, house_to_batteries_distances)
        return self.routes
