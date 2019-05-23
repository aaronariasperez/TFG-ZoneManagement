import csv
from Route import Route
from Section import Section
import Constants as ct
import numpy as np


# ****Reads the Escenario.csv and returns the useful information****
def get_route_from_csv(path):
    slopes = []
    distances = []
    with open(path, mode='r') as data:
        csv_reader = csv.reader(data, delimiter=',')
        first = True
        for row in csv_reader:
            if first:
                first = False
            else:
                slopes.append(float(row[2]))
                distances.append(float(row[3]))

    return [slopes, distances]


# ****Using the information returned by get_route_from_csv, creates the route.csv****
def create_route(path, percentage):
    [slopes, distances] = get_route_from_csv(path)

    green_zones = int(percentage * len(slopes))  # % of green sections
    mask = [0] * len(slopes)
    for i in range(green_zones):
        mask[i] = 1
    type_sections = np.random.permutation(mask)

    sections = []
    for i in range(len(slopes)):
        sec = Section(i, type_sections[i], slopes[i], distances[i])
        sections.append(sec)

    aux = 'routes/route' + str(percentage*100)[:-2] + '.csv'
    with open(aux, mode='w', newline='') as route_write:
        dataset_writer = csv.writer(route_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for sec in sections:
            dataset_writer.writerow([sec.identity, sec.section_type, sec.slope, sec.distance])


# ****Reads the route.csv and returns a route with this information****
def read_route(path):
    sections = []
    with open(path, mode='r') as data:
        csv_reader = csv.reader(data, delimiter=',')
        for row in csv_reader:
            sec = Section(int(row[0]), int(row[1]), float(row[2]), float(row[3]))
            sections.append(sec)

    route = Route(1, sections)

    return route
