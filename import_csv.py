# Libraries
import csv

# Classes
from house import House
from battery import Battery


def import_district(district_number):
    """Retrieve all houses from csv and create district with house objects."""

    # open and read the csv file
    f = open(f'Houses&Batteries/district{district_number}_houses.csv')
    district_data = csv.reader(f)
    next(district_data)

    # will contain the house objects
    district = []
    x_houses = []
    y_houses = []
    # create an object for each house
    for house_id, row in enumerate(district_data, 1):
        x, y = eval(row[0]), eval(row[1])
        usage = eval(row[2])
        house = House(house_id, x, y, usage)
        district.append(house)
        x_houses.append(x)
        y_houses.append(y)

    return district, x_houses, y_houses


def import_batteries(district_number):
    """Retrieve batteries from csv and create battery objects."""

    # open and read the csv file
    f = open(f'Houses&Batteries/district{district_number}_batteries.csv')
    batteries_data = csv.reader(f)
    next(batteries_data)

    # will contain the battery objects
    batteries = []

    # create an object for each battery
    for battery_id, row in enumerate(batteries_data, 1):
        x, y = eval(row[0])[0], eval(row[0])[1]
        capacity = eval(row[1])
        battery = Battery(battery_id, x, y, capacity)

        batteries.append(battery)

    return batteries
