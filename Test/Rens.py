from distance import get_distance
import csv
from house import House
from battery import Battery


def main():
    # district_number = input("What district?:")
    district = create_district(1)
    batteries = create_batteries(1)
    matrix = make_distance_matrix(district, batteries)
    print(matrix)


def create_district(district_number):
    """Retrieve all houses from csv and create district with house objects."""

    f = open(f'Houses&Batteries/district{district_number}_houses.csv')
    district_data = csv.reader(f)
    next(district_data)
    district = {}

    # Create an object for each house
    for house_id, row in enumerate(district_data, 1):
        district[house_id] = House(house_id, int(
            row[0]), int(row[1]), float(row[2]))

    return district


def create_batteries(district_number):
    """Retrieve batteries from csv and create battery objects."""

    f = open(f'Houses&Batteries/district{district_number}_batteries.csv')
    batteries_data = csv.reader(f)
    next(batteries_data)
    batteries = {}

    # Create an object for each house
    for battery_id, row in enumerate(batteries_data, 1):
        coordinates = eval(row[0])
        batteries[battery_id] = Battery(
            battery_id, coordinates[0], coordinates[1], eval(row[1]))

    print(batteries[1])

    return batteries

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

