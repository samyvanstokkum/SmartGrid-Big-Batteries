class Node():
    node_id = 1
    def __init__(self, x, y):
        self.name = "node" + f"{Node.node_id}"
        self.x = x
        self.y = y
        Node.node_id += 1
    
    def __repr__(self):
        return self.name

def get_nodes(x1, y1, x2, y2):
    new_nodes = []
    corner_point = Node(x2, y1)
    new_nodes.append(corner_point)
    
    for i in range(1, abs(y1-y2)):
        if y1 < y2:
            node = Node(x1, y2 - i)
            new_nodes.append(node)
        if y1 > y2:
            node = Node(x1, y2 + i)
            new_nodes.append(node)
    for j in range(1, abs(x1 - x2)):
        if x1 < x2:
            node = Node(x1 + j, y2)
            new_nodes.append(node)
        if x1 > x2:
            node = Node(x1 - j, y2)
            new_nodes.append(node)

    return new_nodes