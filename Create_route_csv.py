import csv
from Route import Route
from Section import Section
import Constants as ct
import numpy as np


# ****Reads the Escenario.csv and returns the useful information****
def get_route_from_csv(path):
    slopes = []
    distances = []
    stops = []
    with open(path, mode='r') as data:
        csv_reader = csv.reader(data, delimiter=',')
        first = True
        for row in csv_reader:
            if first:
                first = False
            else:
                slopes.append(float(row[2]))
                distances.append(float(row[3]))
                if row[5] in (None, ""):  # there is not a stop
                    stops.append(False)
                else:
                    stops.append(True)

    return [slopes, distances, stops]


# ****Using the information returned by ge_route_from_csv, creates the route.csv****
def create_route(path):
    [slopes, distances, stops] = get_route_from_csv(path)

    green_zones = int(0.2 * len(slopes))  # % of green sections
    mask = [0] * len(slopes)
    for i in range(green_zones):
        mask[i] = 1
    type_sections = np.random.permutation(mask)

    sections = []
    for i in range(len(slopes)):
        sec = Section(i, type_sections[i], slopes[i], distances[i], stops[i], ct.avg_speed)
        sections.append(sec)

    with open('route.csv', mode='w', newline='') as route_write:
        dataset_writer = csv.writer(route_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for sec in sections:
            dataset_writer.writerow([sec.identity, sec.section_type, sec.slope, sec.distance, sec.stop, ct.avg_speed])


# ****Reads the route.csv and returns a route with this information****
def read_route(path):
    sections = []
    with open(path, mode='r') as data:
        csv_reader = csv.reader(data, delimiter=',')
        for row in csv_reader:
            stop = True if row[4] == 'True' else False
            sec = Section(int(row[0]), int(row[1]), float(row[2]), float(row[3]), stop, float(row[5]))
            sections.append(sec)

    route = Route(1, sections, [])

    return route
