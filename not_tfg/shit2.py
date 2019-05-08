import math
import numpy as np
import csv
from ast import literal_eval as make_tuple
import sys

print('Los args son: %s' % ([float(x) for x in sys.argv[1:]]))

aux = 'route' + str(float(sys.argv[1])*100)[:-2] + '.csv'
print(aux)

with open('pruebas/prueba.txt', mode='a', newline='') as prueba:
    dataset_writer = csv.writer(prueba, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    dataset_writer.writerow(aux)
