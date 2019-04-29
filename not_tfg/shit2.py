import math
import numpy as np
import csv

with open('shit.csv', mode='w', newline='') as shit:
    dataset_writer = csv.writer(shit, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(15):
        dataset_writer.writerow(['whaaat', 'hee', 'aaaa'])