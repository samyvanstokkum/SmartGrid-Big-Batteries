from prim import Prim


def get_output_shared(config1):
    """
    Generate output in desired format given a configuration.
    Take into account that grid lines can be shared.
    """

    prim = Prim(config1.batteries)
    output_list = []
    for j, mst in enumerate(prim.mst_container):
        battery = config1.batteries[j]
        batterij = {
            "locatie": f"{battery.x},{battery.y}",
            "capaciteit": 1507.0,
            "huizen": []
        }
        for branch in mst.keys():
            x, y = branch.path
            kabels = []
            for i in range(len(x)):
                coordinate = f"({x[i]},{y[i]})"
                kabels.append(coordinate)
            kabels.reverse()
            for house in config1.district:
                if (house.x, house.y) == (branch.end_x, branch.end_y):
                    output = house.power
                    break
            house_info = {
                "locatie": f"{branch.end_x},{branch.end_y}",
                "output": f"{output}",
                "kabels": kabels
            }
            batterij["huizen"].append(house_info)
        output_list.append(batterij)

    return output_list


def get_output(batteries):
    """
    Generate output in desired format given a configuration.
    Take into account that grid lines cannot be shared.
    """

    output_list = []
    for battery in batteries:
        battery_info = {
            "locatie": f"{battery.x},{battery.y}",
            "capaciteit": battery.real_capacity,
            "huizen": []
        }

        for house in battery.houses:
            house_info = {
                "locatie": f"{house.x},{house.y}",
                "output_list": house.power,
                "kabels": []
            }

            x1 = house.x
            x2 = battery.x
            y1 = house.y
            y2 = battery.y

            if x2 > x1:
                node = x1
                while node != x2:
                    coordinate = f"({node},{y1})"
                    house_info["kabels"].append(coordinate)
                    node += 1
                coordinate = f"({node},{y1})"
                house_info["kabels"].append(coordinate)
            else:
                node = x1
                while node != x2:
                    coordinate = f"({node},{y1})"
                    house_info["kabels"].append(coordinate)
                    node -= 1
                coordinate = f"({node},{y1})"
                house_info["kabels"].append(coordinate)

            if y2 > y1:
                node = y1
                while node != y2:
                    coordinate = f"({x2},{node})"
                    house_info["kabels"].append(coordinate)
                    node += 1
                coordinate = f"({x2},{node})"
                house_info["kabels"].append(coordinate)
            else:
                node = y1
                while node != y2:
                    coordinate = f"({x2},{node})"
                    house_info["kabels"].append(coordinate)
                    node -= 1
                coordinate = f"({x2},{node})"
                house_info["kabels"].append(coordinate)

            battery_info["huizen"].append(house_info)

        output_list.append(battery_info)

    return output_list
