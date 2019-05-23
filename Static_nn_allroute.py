import Simulation
from Bus import Bus
import Constants as ct
import numpy as np
import csv
from keras.models import load_model
from Create_route_csv import read_route
import time


path_windows = 'E:\Dropbox\TFG\TFG_code\\route_for_nn20.csv'
path_linux = r'/home/aaron/Dropbox/TFG/TFG_code/route_for_nn10.csv'
path_windows3 = 'E:\Dropbox\TFG\TFG_code\\trained_model3_10_adamax_best.h5'
path_linux3 = r'/home/aaron/Dropbox/TFG/TFG_code/trained_model3_10_adamax_best.h5'

model = load_model(path_windows3)
sections = []
ev_fitness = 0
with open(path_windows, mode='r') as dataset:
    csv_reader = csv.reader(dataset, delimiter=',')
    for row in csv_reader:
        sections.append([float(x) for x in row[:-1]])
        ev_fitness = row[-1:]

sections = np.array(sections)

path_windows = 'E:\Dropbox\TFG\TFG_code\dataset.csv'
path_linux = r'/home/aaron/Dropbox/TFG/TFG_code/dataset.csv'
x = []
with open(path_windows, mode='r') as dataset:
    csv_reader = csv.reader(dataset, delimiter=',')
    for row in csv_reader:
        x.append([float(x) for x in row[:-1]])

x = np.array(x)

computed = {}


def normalize(data, data_array, i):
    if i in computed:
        minim = computed[i][0]
        maxim = computed[i][1]
    else:
        minim = min(data_array)
        maxim = max(data_array)
        computed[i] = (minim, maxim)

    return (data-minim)/(maxim-minim)

start = time.time()
individual = []
for i, s in enumerate(sections):
    green_exp, normal_exp, dist, slope, charge, rem_normal, rem_green = s

    norm_expected = 1 if green_exp == 1 else -1
    norm_dist = normalize(dist, x[:, 2], 2)
    norm_slope = normalize(slope, x[:, 3], 3)
    norm_charge = normalize(charge, x[:, 4], 4)
    norm_rem_normal = normalize(rem_normal, x[:, 5], 5)
    norm_rem_green = normalize(rem_green, x[:, 6], 6)

    sec = [norm_expected, norm_dist, norm_slope, norm_charge, norm_rem_normal, norm_rem_green]
    prediction = model.predict(np.array([sec]))

    if prediction[0][0] >= prediction[0][1]:  # combustion
        individual.append(0)
    else:
        individual.append(1)
end = time.time()

path_windows4 = 'E:\Dropbox\TFG\TFG_code\\routes\\route20.csv'
path_linux4 = r'/home/aaron/Dropbox/TFG/TFG_code/routes/route10.csv'

route = read_route(path_windows4)
zexp = []
greenKm_expected = 0
normalKm_expected = 0
for sec in route.sections:
    zexp.append(sec.section_type)
    if sec.section_type == 1:
        greenKm_expected += sec.distance
    else:
        normalKm_expected += sec.distance

main_bus = Bus(1, route, ct.initial_charge, 1.3)

[km_cov, zcov, remaining_charge, charges] = Simulation.static_simulation(individual, main_bus)

nn_fitness = 0
for i, t in enumerate(zexp):
    if t == 1 and zcov[i] == 1:
        nn_fitness += 2*km_cov[i]
    if t == 0:
        nn_fitness += km_cov[i]
    if t == 1 and zcov[i] == 0:
        nn_fitness -= (route.sections[i].distance*0.001 - km_cov[i])*10000

print("The expected sections to be covered\n%s" % zexp)
print("The sections covered\n%s" % zcov)
print("The remaining charge %skWh" % remaining_charge)
print("Time of inference " + str(end - start) + " seconds")

normal_kms = 0
green_kms = 0
sections = route.sections
for i, sec in enumerate(sections):
    if sec.section_type == 1:
        green_kms += km_cov[i]
    else:
        normal_kms += km_cov[i]

print("Green kms covered: %s of %s" % (green_kms, greenKm_expected/1000))
print("Normal kms covered: %s of %s" % (normal_kms, normalKm_expected/1000))

print("The fitness of nn is: "+str(nn_fitness))
print("The fitness of ev is: "+str(ev_fitness[0]))

