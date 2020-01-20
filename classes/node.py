from operator import itemgetter
from math import sqrt
import matplotlib.pyplot as plt
from branch import Branch
from random import choice

class Node():
    node_id = 1
    def __init__(self, x, y):
        self.name = "node" + f"{Node.node_id}"
        self.x = x
        self.y = y
        Node.node_id += 1

    def __repr__(self):
        return self.name

def get_neighbours(x1, y1):
    neighbours = []
    feasible_points = list(range(51))

    # for dx in range(-1, 2):
    #     for dy in range(-1, 2):
    #         if dx != 0 or dy != 0:
    #             node = Node(x1 + dx, y1 + dy)
    #             if node.x in feasible_points and node.y in feasible_points:
    #                 neighbours.append(node)

    change = [-1, 1]
    for delta in change:
        x = x1 + delta
        if x in feasible_points:
            node = Node(x, y1)
            neighbours.append(node)
        y = y1 + delta
        if y in feasible_points:
            node = Node(x1, y)
            neighbours.append(node)

    return neighbours

def locate_mins(open_set):
    _, h = min(open_set.items(), key=itemgetter(1))
    all_mins = []
    for node, cost in open_set.items():
        if cost == h:
            all_mins.append((node, cost))
    return all_mins


def get_path(start, target):
    path = []
    open_set = {start: sqrt((start.x - target.x)**2 + (start.y - target.y)**2) } # nodes to be evaluated # h = distance from end node
    closed_set = {} # nodes already evaluated
    while True:
        all_options = locate_mins(open_set)
        current, h = choice(all_options)
        # current, h = min(open_set.items(), key=itemgetter(1))
        path.append(current)
        del open_set[current]
        closed_set[current] = h

        if current.x is target.x and current.y is target.y:
            return path
            

        neighbours = get_neighbours(current.x, current.y)
        for neighbour in neighbours:
            if neighbour in closed_set.keys():
                continue

            if neighbour not in open_set.keys():
                open_set[neighbour] = sqrt((neighbour.x - target.x)**2 + (neighbour.y - target.y)**2)
                # print(open_set)


if __name__ == "__main__":
    
    start = Node(1, 10)
    target = Node(1, 3)
    path = get_path(start, target)
    print(path)
#     branch = Branch(start, target)
#     branch.load_path(path)
#     x, y = get_coordinates(branch.path)
#     plt.figure()
#     plt.plot(x, y, '-o')
#     plt.xlim(0, 10)
#     plt.show()
#     print("Done!")


















    #________________________________________________________#

     # rel_location = determine_relative_location(x1, y1, x2, y2)
        # right_locations = ['north', 'east', 'south', 'west']
        # if not rel_location in right_locations:
        #     corner_point = Node(x2, y1)

        
        # for i in range(1, abs(y1-y2)):
        #     if y1 < y2:
        #         node = Node(x1, y2 - i)
        #         new_nodes.append(node)
        #     if y1 > y2:
        #         node = Node(x1, y2 + i)
        #         new_nodes.append(node)
                
        # for j in range(1, abs(x1 - x2)):
        #     if x1 < x2:
        #         node = Node(x1 + j, y2)
        #         new_nodes.append(node)
        #     if x1 > x2:
        #         node = Node(x1 - j, y2)
        #         new_nodes.append(node)

        # return new_nodes