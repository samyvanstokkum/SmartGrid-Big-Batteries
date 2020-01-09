# Libraries
import matplotlib.pyplot as plt


def create_grid(district, x_houses, y_houses, batteries, routes):
    print(routes)
    # set to True to print the houses and batteries
    yes_plot = True

    # print batteries and houses
    if yes_plot:
        plt.figure()
        colors = ['r', 'b', 'g', 'c', 'y']
        # plot batteries in red and houses in blue
        for battery in batteries:
            plt.plot(battery.x, battery.y,
                     colors[battery.id-1]+'o', markersize=10, label='batteries')

        plt.plot(x_houses, y_houses, 'k*', label='houses')

        # plt.title('houses and batteries')
        plt.grid(True)
        plt.legend(loc='upper center', ncol=10, fontsize=8)

        # append house to battery
        print(routes)
        cable_distance = 0

        for battery in batteries:
            for coordinates_x, coordinates_y in routes[battery]:
                plt.plot(coordinates_x, coordinates_y, colors[battery.id -1])
                cable_distance += abs(coordinates_x[0]-coordinates_x[2]) + abs(coordinates_y[0] - coordinates_y[2])
        
        print(cable_distance)
        print(cable_distance*9)

        plt.show()
