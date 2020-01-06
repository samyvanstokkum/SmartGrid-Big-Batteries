import csv
from house import House

f = open('Houses&Batteries/disctrict1_battery.csv')

district1_data = csv.reader(f)
next(district1_data)
district1 = []

for number, row in enumerate(district1_data, 1):
    print(row)
    print(number)
