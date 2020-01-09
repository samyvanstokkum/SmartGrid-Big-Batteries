import numpy as np


class Route:
    def __init__(self):
        self.routes = {}
        self.cable = 0

    def get_house_to_batteries_distances(self, district, batteries):
        """Create dictionary containing distances to each battery for each house.
        Order such that houses with greatest cummulative distance are first. 
        """
        house_to_batteries_distances = {}
        for house in district:
            house_to_batteries_distances[house] = []

            for battery in batteries:
                house_to_batteries_distances[house].append(
                    abs(battery.x-house.x) + abs(battery.y - house.y)
                )
        house_to_batteries_distances = {house: distance for house, distance in 
            sorted(all_distances.items(), key=lambda item: sum(item[1]), reverse=True)
            }
        return house_to_batteries_distances

    def calculate_routes(self, district, batteries, houses_desc):
        for battery in batteries:
            self.routes[battery] = []
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

                    self.routes[battery].append([x, y])

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
        print(self.routes)
