
class Battery:
    def __init__(self, battery_id, x, y, capacity):
        self.id = battery_id
        self.x = x
        self.y = y
        self.capacity = capacity
        # self.houses = []

    # add a house objecy to the battery
    def add_house(self, house):
        # self.houses.append(house)
        self.capacity -= house.usage

    # remove a house object from the battery
    def remove_house(self, house):
        # self.houses.remove(house)
        self.capacity += house.usage

    def __repr__(self):
        return f"Battery {self.id}"
