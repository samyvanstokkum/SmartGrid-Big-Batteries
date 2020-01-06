CAPACITY = 1507.0


class Battery:
    def __init__(self, battery_id, x, y):
        self.id = battery_id
        self.x = x
        self.y = y
        self.capacity = CAPACITY
        self.houses = []

    # Add a house to the battery
    def add_house(self, house):
        self.houses.append(house)
        self.capacity -= house.usage

    # Remove a house from the battery
    def remove_house(self, house):
        self.houses.remove(house)
        self.capacity += house.usage

    def __str__(self):
        return f"{self.id}"
