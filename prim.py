from node import Node, get_nodes

def prim(battery):

    # distances_for_nodes_in_tree_to_remaining_nodes = {} for now 'tree'
    path = []
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
            house_with_least_cost = min(d.items(), key=lambda x: x[1])
            least_costs[vertice] = (house_with_least_cost[0], house_with_least_cost[1])

        # print('--------------------------------')
        new_branch = min(least_costs.items(), key=lambda x: x[1][1])
        # print(new_branch) # (from (to, costs))
        # print('--------------------------------')
        # print('--------------------------------')
        # print('')
        from_vertice, new_vertice, cost = new_branch[0], new_branch[1][0], new_branch[1][1]
        path.append((from_vertice, new_vertice, cost))

        
        for nodes in path:
            from_node = nodes[0]
            to_node = nodes[1]
            print(f"{from_node}: ({from_node.x}, {from_node.y}) -- {to_node}: ({to_node.x}, {to_node.y}) ")
        

        houses.remove(new_vertice)
        for vertice in tree.keys():
            del tree[vertice][new_vertice]
        
        new_nodes = get_nodes(from_vertice.x, from_vertice.y, new_vertice.x, new_vertice.y)
        for node in new_nodes: 
            all_nodes.append(node)
        
        for node in new_nodes:
            print(f"{node}: ({node.x}, {node.y})")
            tree[node] = {}
            for house in houses:
                distance = abs(node.x - house.x) + abs(node.y - house.y)
                tree[node][house] = distance
        
        tree[new_vertice] = {}
        for house in houses:
            distance = abs(new_vertice.x - house.x) + abs(new_vertice.y - house.y)
            tree[new_vertice][house] = distance
    cable = 0
    for i in range(len(path)):
        cable += path[i][2]
    print(cable)
    # plt.figure()
    # for node in all_nodes:
    #     plt.plot(node.x, node.y, 'b.')
    # for house in battery.houses:
    #     plt.plot(house.x, house.y, 'k*')
    # plt.show()
        t = time.time()
    path = prim(batteries[4])
    elapsed = time.time() - t
    print(elapsed)
    print(path)
    # x_co = []
    # y_co = []
    # plt.figure()
    # for nodes in path:
    #     from_node = nodes[0]
    #     to_node = nodes[1]
    #     print(f"{from_node}: ({from_node.x}, {from_node.y}) -- {to_node}: ({to_node.x}, {to_node.y}) ")
    #     plt.plot([from_node.x, to_node.x, to_node.x], [from_node.y, from_node.y, to_node.y])
    #     # plt.plot([from_node.x, from_node.x, to_node.x], [from_node.y, to_node.y, to_node.y])

    # #     x_co.append([from_node.x, to_node.x, to_node.x])
    # #     y_co.append([from_node.y, from_node.y, to_node.y])
    # # plt.plot(x_co, y_co)
    # plt.xlim(-2,50)
    # plt.show()
    # print()

    return path