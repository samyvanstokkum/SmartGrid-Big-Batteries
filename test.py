def get_output_prim(config1):
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
    print(json.dumps(big_list, indent=4))
