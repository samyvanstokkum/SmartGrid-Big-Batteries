import os, sys

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "classes"))
sys.path.append(os.path.join(directory, "helper"))
sys.path.append(os.path.join(directory, "data"))

sys.path.append(os.path.join(directory, "classes", "objects"))
sys.path.append(os.path.join(directory, "classes", "algorithms"))


# Classes
from hillclimber import HillClimber
from simulatedannealing import SimulatedAnnealing
from configuration import Configuration
from prim import Prim
import json

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

def main():
    
    # change this into get_string from user:
    # markov, different temp and cooling rates, linear/exp, etc
    config1 = Configuration("greedy", 1, share_grid = False)
    # SA = SimulatedAnnealing(config1.batteries, share_grid = False, scheme="exp")
    # SA.plot_costs()
    # get_output_prim(config1)
   
    HC = HillClimber(config1.batteries, "steepest", 10, share_grid = False)
    HC.plot_costs()

    # HillClimber(config1.batteries, 'stochastic', 1000, share_Grid = False)
    # SA = SimulatedAnnealing(config1.batteries, share_grid = True, scheme="exp")
    # SA.plot_costs()
    # config1.batteries = SA.batteries
    # config1.make_plot()


if __name__ == "__main__":
    main()
