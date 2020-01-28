class Battery:
    """
    Create a battery object with all its attributes and functionality.
    """

    def __init__(self, battery_id, x, y, capacity, cost=5000):
        self.real_capacity = capacity
        self.id = battery_id
        self.x = x
        self.y = y
        self.capacity = capacity
        self.houses = []
        self.costs = cost

    def add_house(self, house):
        """
        Add house and update battery capacity. Then sort 
        the houses on id.
        """

        self.houses.append(house)
        self.capacity -= house.power
        self.houses = sorted(self.houses, key=lambda x: x.id)

    def remove_house(self, house):
        """
        Remove house and update battery capacity. Then sort 
        the houses on id.
        """

        self.houses.remove(house)
        self.capacity += house.power
        self.houses = sorted(self.houses, key=lambda x: x.id)

    def restore(self):
        """
        Clear all houses from battery and reset
        capacity to its initial value.
        """

        self.houses.clear()
        self.capacity = self.real_capacity

    def __repr__(self):
        return f"Battery {self.id}"
