def get_houses_to_batteries_distances(district, batteries):
    houses_to_batteries_distances = {}
    for house in district:
        houses_to_batteries_distances[house] = []

        for battery in batteries:
            houses_to_batteries_distances[house].append(
                abs(battery.x-house.x) + abs(battery.y - house.y)
            )
    houses_to_batteries_distances = {house: distance for house, distance in 
        sorted(houses_to_batteries_distances.items(), key=lambda item: sum(item[1]), reverse=True)
        }
        
    return houses_to_batteries_distances

def get_house_to_batteries_distances(distances):
    house_to_batteries_distances = {}
    for battery_nr, distance in enumerate(distances, 1):
        house_to_batteries_distances[battery_nr] = distance

    return house_to_batteries_distances

def get_coordinates(node1, node2):
    return ([node1.x, node1.x, node2.x], [node1.y, node2.y, node2.y])




