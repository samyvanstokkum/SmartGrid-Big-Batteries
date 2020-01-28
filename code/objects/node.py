class Node():
    """
    Create a node object with its location and name.
    """

    node_id = 1

    def __init__(self, x, y):
        self.name = "node" + f"{Node.node_id}"
        self.x = x
        self.y = y
        Node.node_id += 1

    def __repr__(self):
        return self.name
