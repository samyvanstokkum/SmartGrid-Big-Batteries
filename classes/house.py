import csv


class House():

    def __init__(self, house_id, x, y, usage):
        self.id = house_id
        self.x = x
        self.y = y
        self.usage = usage

    def __repr__(self):
        return f"House {self.id}"
