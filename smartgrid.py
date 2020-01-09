# Classes
from house import House
from battery import Battery
from route import Route

# Functions
from import_csv import import_district, import_batteries
from grid import create_grid


def main():
    # load houses from district1 and get house coordinates
    district, x_houses, y_houses = import_district(1)
    # print(district)

    # load batteries from district1 and get battery coordinates
    batteries = import_batteries(1)
    # print(batteries)

    # calculates and stores the routes
    r = Route()
    routes = r.import_routes(district, batteries)
    print(routes)
    # plots the district and batteries in a grid
    create_grid(district, x_houses, y_houses, batteries, routes)


if __name__ == "__main__":
    main()
