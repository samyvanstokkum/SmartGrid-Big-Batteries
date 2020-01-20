def determine_relative_location(x1, y1, x2, y2):
    if x1 > x2:
        if y1 < y2:
            rel_location = "northwest"
        if y1 == y2:
            rel_location = "west"
        if y1 > y2: 
            rel_location = "southwest"
    if x1 == x2:
        if y1 < y2:
            rel_location = "north"
        if y1 > y2:
            rel_location = "south"
    if x1 < x2:
        if y1 < y2:
            rel_location = "northeast"
        if y1 == y2:
            rel_location = "east"
        if y1 > y2: 
            rel_location = "southeast"
    
    return rel_location
