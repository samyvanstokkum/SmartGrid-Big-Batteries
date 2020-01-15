import csv
from random_house import House
from random_battery import Battery
import matplotlib.pyplot as plt
from random_distance import get_distance


def main():
    # set to 1 if you want to print the houses and batteries
    yes_plot = True

    # district_number = input("What district?:")
    district, x_houses, y_houses = create_district(1)
    batteries, x_batteries, y_batteries = create_batteries(1)
    matrix = make_distance_matrix(district, batteries)
    # print(matrix)

    # print batteries and houses
    if yes_plot:
        plt.figure()
        colors = ['r', 'b', 'g', 'c', 'y']
        # plot batteries in red and houses in blue
        for battery in batteries.values():
            plt.plot(battery.x, battery.y,
                     colors[battery.id-1]+'o', markersize=10, label='batteries')

        plt.plot(x_houses, y_houses, 'k*', label='houses')

        # plt.title('houses and batteries')
        plt.grid(True)
        plt.legend(loc='upper center', ncol=10, fontsize=8)

    # append house to battery
    cable_distance, battery_id, house_id = 0, 0, 1
    for battery in batteries.values():
        while battery.capacity - district[house_id].usage >= 0:
            battery.add_house(district[house_id])
            route = battery.calculate_route(district[house_id])
            plt.plot(route[0], route[1], colors[battery_id])

            cable_distance += matrix[house_id-1][battery_id]
            house_id += 1
        battery_id += 1
    # print(cable_distance*9 + 5*5000)

    plt.show()

    # just to check if can add/remove houses
    batteries[1].add_house(district[1])
    batteries[1].remove_house(district[1])


def create_district(district_number):
    """Retrieve all houses from csv and create district with house objects."""

    f = open(f'Houses&Batteries/district{district_number}_houses.csv')
    district_data = csv.reader(f)
    next(district_data)
    district = {}
    x_houses = []
    y_houses = []

    # Create an object for each house
    for house_id, row in enumerate(district_data, 1):
        district[house_id] = House(house_id, int(
            row[0]), int(row[1]), float(row[2]))

        # append coordinates for later use (plotting the batteries)
        x_houses.append(int(row[0]))
        y_houses.append(int(row[1]))

    return district, x_houses, y_houses


def create_batteries(district_number):
    """Retrieve batteries from csv and create battery objects."""

    f = open(f'Houses&Batteries/district{district_number}_batteries.csv')
    batteries_data = csv.reader(f)
    next(batteries_data)
    batteries = {}
    x_batteries = []
    y_batteries = []

    # Create an object for each battery
    for battery_id, row in enumerate(batteries_data, 1):
        coordinates = eval(row[0])
        batteries[battery_id] = Battery(
            battery_id, coordinates[0], coordinates[1], eval(row[1]))

        # append coordinates for later use (plotting the batteries)
        x_batteries.append(coordinates[0])
        y_batteries.append(coordinates[1])

    return batteries, x_batteries, y_batteries


def make_distance_matrix(district, batteries):
    distance_matrix = []
    for house in district.values():
        row = []
        for battery in batteries.values():
            row.append(get_distance(house.x, house.y, battery.x, battery.y))
        distance_matrix.append(row)

    return distance_matrix


if __name__ == "__main__":
    main()
