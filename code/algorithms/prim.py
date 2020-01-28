from node import Node
from branch import Branch
from helpers import *
import copy


class Prim():
    """
    This class is devoted to Prim's algorithm.

    It creates a minimum spanning tree as follows.
    For a given set of houses allocated to a
    battery, this class spans all trees for 
    all batteries and determines its costs.
    """

    def __init__(self, batteries):
        self.batteries = batteries
        self.mst_container = []
        self.span_trees()
        self.costs = 0
        self.set_costs()

    def span_trees(self):
        """
        Span a tree for each battery with its houses.
        For all nodes in the tree, determine all paths to
        remaining houses and choose the cheapest path. 
        Add the new house to the tree and all nodes of 
        its path. Continue until all houses are in the tree.
        """

        for battery in self.batteries:
            mst = {}
            tree = {battery: {}}
            houses = copy.deepcopy(battery.houses)

            for house in houses:
                distance = get_distance(house, battery)
                tree[battery][house] = distance

            least_distance = {}
            while houses:
                for vertice in tree.keys():
                    distance_to_targets = tree[vertice]
                    house, distance = min(
                        distance_to_targets.items(), key=lambda x: x[1])
                    least_distance[vertice] = (house, distance)

                link = min(least_distance.items(), key=lambda x: x[1][1])

                from_vertice, new_vertice, distance = link[0], link[1][0], link[1][1]
                new_nodes = pathfinder(from_vertice, new_vertice)[1:-1]
                branch = Branch(from_vertice, new_vertice)
                branch.load_path(new_nodes)
                mst[branch] = distance

                houses.remove(new_vertice)
                for vertice in tree.keys():
                    del tree[vertice][new_vertice]

                for node in new_nodes:
                    tree[node] = {}
                    for house in houses:
                        distance = get_distance(node, house)
                        tree[node][house] = distance

                tree[new_vertice] = {}
                for house in houses:
                    distance = get_distance(new_vertice, house)
                    tree[new_vertice][house] = distance

            self.mst_container.append(mst)

    def set_costs(self):
        """
        Set costs for all minimimum spanning trees
        and sum them.
        """

        for mst in self.mst_container:
            for branch in mst:
                self.costs += mst[branch]

        self.costs *= 9
