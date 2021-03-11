"""Data mockup for ECMWF"""
import random


header = "{year} SBUV_V86 MOD V10 PROF TOT Zonal Means"
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
index = "{lat1:3} {lat2:3}"
columns = 5*' ' + (3*' ').join(months)
latitude_step = 5


def create_data(years):
    with open("sbuv.v86.mod_v10.70-18.za.txt", 'w') as textfile:
        for year in years:
            textfile.write(header.format(year=year) + '\n')
            textfile.write(random_table())


def random_table():
    table = columns + '\n'
    for latitude in range(-90, 90, latitude_step):
        start = latitude
        end = latitude + latitude_step
        table = table + random_row(start, end) + '\n'
    return table


def random_row(start, end):
    ix = index.format(lat1=start, lat2=end)
    values = [random.uniform(0, 400) for _ in range(0, 12)]
    return ix + ''.join([" {:5.1f}".format(n) for n in values])
