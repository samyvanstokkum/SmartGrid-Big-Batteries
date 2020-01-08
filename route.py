import numpy as np


class Route:
    def __init__(self):
        self.routes = []
        self.cable = 0

    def distance_descending(self, district, batteries):
        all_distances = {}
        for house in district:
            all_distances[house] = []

            for battery in batteries:
                all_distances[house].append(
                    (abs(battery.x-house.x) + abs(battery.y - house.y)))
        sorted_list = sorted(
            all_distances.items(), key=lambda x: sum(x[1]), reverse=True)
        return sorted_list

    def calculate_routes(self, district, batteries, houses_desc):
        for h in houses_desc:
            house = h[0]
            distances_list = h[1]
            last_house = houses_desc[-1][0]

            # add house to battery
            while True:
                # select the route with the lowest possible distance from house to battery
                battery_index = distances_list.index(np.nanmin(distances_list))
                battery = batteries[battery_index]

                # check if capacity fits the usage
                if battery.capacity - house.usage >= 0:
                    battery.add_house(house)
                    # x and y coordiates from house to battery
                    x = [house.x, house.x, battery.x]
                    y = [house.y, battery.y, battery.y]
                    self.routes.append([x, y])
                    break
                else:
                    distances_list[battery_index] = np.nan
                if house == last_house:
                    break

    def delete_duplicates():
        # TODO Delete coordinates that are duplicated if a line is shared with another battery line, change the color to a uniform color like black.
        pass

    def cable_costs(self):
        pass

    def import_routes(self, district, batteries):
        descending_distances = self.distance_descending(district, batteries)
        self.calculate_routes(district, batteries, descending_distances)
        return self.routes
