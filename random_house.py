class House():

    def __init__(self, house_id, x, y, usage):
        self.id = house_id
        self.x = x
        self.y = y
        self.usage = usage

    def __str__(self):
        return f"{self.id}"
