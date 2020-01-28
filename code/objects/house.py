import csv


class House():
    """
    Create a house object with its location and power.
    """

    def __init__(self, house_id, x, y, power):
        self.id = house_id
        self.x = x
        self.y = y
        self.power = power

    def __repr__(self):
        return f"House {self.id}"
