
class Battery:
    def __init__(self, battery_id, x, y, capacity):
        self.id = battery_id
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

    def calculate_route(self, house):
        list_x = [house.x, house.x, self.x]
        list_y = [house.y, self.y, self.y]
        route = [list_x, list_y]
        return route

    def __str__(self):
        return f"{self.id}"
