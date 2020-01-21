import random
import copy
from classes.battery import *

def super_random(district, batteries):
    # for i in range(5000):
    while True:
        all_houses = copy.deepcopy(district)
        for battery in batteries:
            battery.restore()

        while all_houses:
            set_of_houses = random.sample(all_houses, 30)
            for house in set_of_houses:
                all_houses.remove(house)

            random.shuffle(batteries)
            while set_of_houses:
                for battery in batteries:
                    six_houses = random.sample(set_of_houses, 6)
                    for house in six_houses:
                        battery.add_house(house)
                        set_of_houses.remove(house)

        still_to_place = []        
        satisfing_constraints = []

        for battery in batteries:
            if battery.capacity < 0:
                house = random.choice(battery.houses)
                still_to_place.append(house)
                battery.remove_house(house)
                satisfing_constraints.append(False)
            else: 
                satisfing_constraints.append(True)

        # print(still_to_place)
        # print(satisfing_constraints)
        total = 0
        if all(satisfing_constraints):
            print("SOLUTION FOUND:")
            for battery in batteries:
                print(battery, f'-')
                print(battery.houses)
                for house in battery.houses:
                    total += abs(house.x - battery.x) + abs(house.y - battery.y)
            print(total * 9)

            break
        # print("------------------------------")
        # if len(still_to_place) == 1:
        #     leftover = 0
        #     for battery in batteries:
        #         if battery.capacity > leftover:
        #             leftover = battery.capacity 
        #             bat_with_most_room = battery 
        #     for house in still_to_place:
        #         bat_with_most_room.add_house(house)
        #         still_to_place.clear()
        #     for battery in batteries:
        #         print(len(battery.houses))
        #         print(battery.capacity)
        # print("------------------------------")

        # if all(satisfing_constraints):
        #     if not still_to_place:
        #         print("ALLOCATION FOUND")
        #         for battery in batteries:
        #             print(battery.houses)
        #     else:
        #         for house in still_to_place:
        #             print(house.usage)
        

        
    