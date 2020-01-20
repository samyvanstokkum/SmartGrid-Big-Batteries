from classes.node import *
from classes.branch import Branch
import copy
import matplotlib.pyplot as plt

def prim(battery):

    # distances_for_nodes_in_tree_to_remaining_nodes = {} for now 'tree'
    mst = {}
    tree = {battery: {} }
    houses = copy.deepcopy(battery.houses)
    all_nodes = []

    for house in houses:
        distance = abs(battery.x - house.x) + abs(battery.y - house.y)
        tree[battery][house] = distance
    least_costs = {}
    while houses:
        for vertice in tree.keys():
            # get for all vertices the closest connectino 
            d = tree[vertice]
            house, cost = min(d.items(), key=lambda x: x[1])
            least_costs[vertice] = (house, cost)

        # print('--------------------------------')
        link = min(least_costs.items(), key=lambda x: x[1][1])
        # (from, (to, costs))
        # print('--------------------------------')
        
        from_vertice, new_vertice, cost = link[0], link[1][0], link[1][1]
        new_nodes = get_path(from_vertice, new_vertice)[1:-1]
        branch = Branch(from_vertice, new_vertice)
        branch.load_path(new_nodes)
        mst[branch] = cost
        

        #path.append((from_vertice, new_vertice, cost))
        
        houses.remove(new_vertice)
        for vertice in tree.keys():
            del tree[vertice][new_vertice]        
        
        for node in new_nodes:
            tree[node] = {}
            for house in houses:
                distance = abs(node.x - house.x) + abs(node.y - house.y)
                tree[node][house] = distance
        
        tree[new_vertice] = {}
        for house in houses:
            distance = abs(new_vertice.x - house.x) + abs(new_vertice.y - house.y)
            tree[new_vertice][house] = distance
    
    # for branch in mst.keys():
    #     plt.plot(branch.path[0], branch.path[1], 'r')
    # plt.xlim(-2, 55)
    # plt.ylim(-2, 55)
    # plt.show()

    
    return mst