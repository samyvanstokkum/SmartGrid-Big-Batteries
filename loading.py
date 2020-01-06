import csv


def get_info_district1():
    f = open('wijk1_huizen.csv')

    district1_data = csv.reader(f)
    next(district1_data)
    district1 = {}
    housenumber = 1
    for row in district1_data:
        row[0] = int(row[0])
        row[1] = int(row[1])
        row[2] = float(row[2])
        district1[housenumber] = row
        housenumber += 1

    # comment blabla
    print(district1)
