class Battery:
    def init(self, x, y, capacity):
        self.x = x
        self.y = y
        self.capacity = capacity
        self.houses = []

    # Add a house to the battery
    def add_house(self, house):
        self.houses.append(house)
        self.capacity -= house.usage

    # Remove a house from the battery
    def remove_house(self, house):
        self.houses.remove(house)
        self.capacity += house.usage
