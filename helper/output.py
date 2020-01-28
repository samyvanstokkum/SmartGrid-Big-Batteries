
from prim import Prim

def get_output_shared(config1):
    """ TODO """
    prim = Prim(config1.batteries)
    big_list = []
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
        big_list.append(batterij)

    return big_list

def get_output(batteries):
    """TODO"""
    # make structure for batteries dicts
    output = []

    for battery in batteries:
        battery_info = {}
        battery_info["locatie"] = f"{battery.x},{battery.y}"
        battery_info["capaciteit"] = battery.capacity
        battery_info["huizen"] = []

        for house in battery.houses:
            house_info = {}
            house_info["locatie"] = f"{house.x},{house.y}"
            house_info["output"] = house.power
            house_info["kabels"] = []

            # append kabels 
            x1= house.x
            x2 =battery.x
            y1 = house.y
            y2 = battery.y

            # part1: from house to mid_point
            if x2 > x1:
                node = x1
                while node != x2:
                    coordinate = f"({node},{y1})"
                    house_info["kabels"].append(coordinate)
                    node+=1
                coordinate = f"({node},{y1})"
                house_info["kabels"].append(coordinate)
            else:
                node = x1
                while node != x2:
                    coordinate = f"({node},{y1})"
                    house_info["kabels"].append(coordinate)
                    node-=1
                coordinate = f"({node},{y1})"
                house_info["kabels"].append(coordinate)
            # part2: from mid_point to battery

            if y2 > y1:
                node = y1
                while node != y2:
                    coordinate = f"({x2},{node})"
                    house_info["kabels"].append(coordinate)
                    node+=1
                coordinate = f"({x2},{node})"
                house_info["kabels"].append(coordinate)
            else:
                node = y1
                while node != y2:
                    coordinate = f"({x2},{node})"
                    house_info["kabels"].append(coordinate)
                    node-=1
                coordinate = f"({x2},{node})"
                house_info["kabels"].append(coordinate)

            # print(house_info)
            battery_info["huizen"].append(house_info)

        output.append(battery_info)
    
    return output