import csv


class House():

    def __init__(self, house_id, x, y, usage):
        self.id = house_id
        self.x = x
        self.y = y
        self.usage = usage

    # def import_district(district_number):
    #     """Retrieve all houses from csv and create district with house objects."""

    #     # open and read the csv file
    #     f = open(f'Houses&Batteries/district{district_number}_houses.csv')
    #     district_data = csv.reader(f)
    #     next(district_data)

    #     # will contain the house objects
    #     district = []

    #     # create an object for each house
    #     for house_id, row in enumerate(district_data, 1):
    #         x, y = eval(row[0]), eval(row[1])
    #         usage = eval(row[2])
    #         house = House(house_id, x, y, usage)
    #         district.append(house)

    #     return district

    def __repr__(self):
        return f"House {self.id}"
