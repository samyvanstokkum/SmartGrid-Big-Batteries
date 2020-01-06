class House():
    
    def __init__(self, x, y, usage):
        self.x = x
        self.y = y 
        self.usage = usage 
    
    def __str__(self): 
        return f"{self.x} - {self.y}"
