import Simulation
from Bus import Bus
import Constants as ct
import numpy as np
import csv
from keras.models import load_model
from Create_route_csv import read_route
import time


path_windows2 = 'E:\Dropbox\TFG\TFG_code\\routes\\route20.csv'
path_linux2 = r'/home/aaron/Dropbox/TFG/TFG_code/routes/route5.csv'
path_windows3 = 'E:\Dropbox\TFG\TFG_code\\dynamic_model_ne.h5'
path_linux3 = r'/home/aaron/Dropbox/TFG/TFG_code/dynamic_model_ne.h5'

model = load_model(path_windows3)

route = read_route(path_windows2)
max_dist = max([a.distance for a in route.sections])
min_dist = min([a.distance for a in route.sections])
max_slope = max([a.slope for a in route.sections])
min_slope = min([a.slope for a in route.sections])

zexp = []
greenKm_expected = 0
normalKm_expected = 0
for sec in route.sections:
    zexp.append(sec.section_type)
    if sec.section_type == 1:
        greenKm_expected += sec.distance
    else:
        normalKm_expected += sec.distance


# ****This function evaluates the zone assignment****
def eval_model():
    fits = []
    for i in range(1000):

        main_bus = Bus(1, route, ct.initial_charge, 1.3)

        [zone_assignment, km_cov, zcov, charge, charges] = Simulation.dynamic_simulation(main_bus, model, normalKm_expected,
                                                                                    greenKm_expected, [max_dist, min_dist, max_slope, min_slope])

        fit = 0
        for i, t in enumerate(zexp):
            if t == 1 and zcov[i] == 1:
                fit += 2*km_cov[i]
            if t == 0:
                fit += km_cov[i]
            if t == 1 and zcov[i] == 0:
                fit -= (route.sections[i].distance*0.001 - km_cov[i])*10000
        fits.append(fit)

    return [fits, zone_assignment, zcov, charge, km_cov]


fits, zone_assignment, zcov, remaining_charge, km_cov = eval_model()

print("Fitness: %s" % fits)
print("The expected sections to be covered\n%s" % zexp)
print("The assignment of the ANN\n%s" % zone_assignment)
print("The sections covered\n%s" % zcov)
print("The remaining charge %skWh" % remaining_charge)

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

count_valid = 0
count_novalid = 0
acum_valid = 0
acum_novalid = 0
for f in fits:
    if f < 0:
        count_novalid += 1
        acum_novalid += f
    else:
        count_valid += 1
        acum_valid += f
print("Not valid mean: %s, proportion of cases: %s" % (str(acum_novalid/count_novalid if not count_novalid == 0 else 0), str(count_novalid/(count_valid+count_novalid))))
print("Valid mean: %s, proportion of cases: %s" % (str(acum_valid/count_valid if not count_valid == 0 else 0), str(count_valid/(count_valid+count_novalid))))