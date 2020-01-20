
class Branch():
    branch_nr = 1

    def __init__(self, start, end):
        self.name = "branch" + f"{Branch.branch_nr}"
        self.start_x = start.x
        self.start_y = start.y
        self.end_x = end.x
        self.end_y = end.y
        self.path = None
        Branch.branch_nr += 1
    
    def load_path(self, path):
        x, y = get_coordinates(path)
        x.insert(0, self.start_x)
        y.insert(0, self.start_y)
        x.append(self.end_x)
        y.append(self.end_y)
        coordinates = (x, y)
        self.path = coordinates
    
    def __repr__(self):
        return self.name

def get_coordinates(path):
    x_co = []
    y_co = []
    for node in path:
        x_co.append(node.x)
        y_co.append(node.y)
    return (x_co, y_co)
    




