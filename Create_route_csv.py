import csv
from Route import Route
from Section import Section
import Constants as ct
import numpy as np


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

    route = Route(1, sections, [])

    return route

