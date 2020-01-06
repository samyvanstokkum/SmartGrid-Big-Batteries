import csv
import House from house

# retrieve district
def get_info_district1():

    f = open('wijk1_huizen.csv')

    district1_data = csv.reader(f)
    next(district1_data)
    district1 = []

    for row in district1_data:
        district1.append(House(int(row[0]), int(row[1], float(row[2]))))

    # comment blabla
    print(district1)

district()

# retrieve batteries
battery()