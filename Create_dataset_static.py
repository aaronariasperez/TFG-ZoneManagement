import Simulation
from Bus import Bus
import Constants as ct
import random
import numpy
from deap import base, creator, tools, algorithms
import csv
from Create_route_csv import create_route, read_route
import sys

# ************************** CLEAN DATASETS FOLDER BEFORE EXECUTE THIS FROM THE SCRIPT **************************

# ****Parameters and environment initialization****

path_windows = 'E:\Dropbox\TFG\TFG_code\Escenario.csv'
path_linux = r'/home/aaron/Dropbox/TFG/TFG_code/Escenario.csv'
path_windows2 = 'E:\Dropbox\TFG\TFG_code\\route.csv'
path_linux2 = r'/home/aaron/Dropbox/TFG/TFG_code/route.csv'

# paths for each green coverage percentage
path_windows2_mod = 'E:\Dropbox\TFG\TFG_code\\routes\\route' + str(float(sys.argv[1])*100)[:-2] + '.csv'
path_linux2_mod = r'/home/aaron/Dropbox/TFG/TFG_code/routes/route' + str(float(sys.argv[1])*100)[:-2] + '.csv'

# argv[1] is the first argument (percentage of green coverage)
create_route(path_windows, float(sys.argv[1]))  # use when a new green section assignation required (random)
route = read_route(path_windows2_mod)

zexp = []
greenKm_expected = 0
normalKm_expected = 0
for sec in route.sections:
    zexp.append(sec.section_type)
    if sec.section_type == 1:
        greenKm_expected += sec.distance
    else:
        normalKm_expected += sec.distance


# ****This function prints some info about the population of each generation****
def print_info(individual, km_cov, zcov, charge, fit, arrival_times):
    print(individual, end="")
    print(", km_cov: ", end="")
    print(km_cov)
    print(", cubierto: ", end="")
    print(zcov)
    print(", bateria: ", end="")
    print(charge)
    print(", fitness: ", end="")
    print(fit)
    print(", tiempos de llegada: ", end="")
    print(arrival_times)
    print("\n")


# ****This function evaluates the zone assignment****
def eval_zone(individual):
    main_bus = Bus(1, route, ct.initial_charge, [3500, 2800, 1125, 800, 3000, 2200, 2340], 1.3)

    [km_cov, zcov, charge, charges] = Simulation.simulation_noSchedule(individual, main_bus, zexp)

    fit = 0
    for i, t in enumerate(zexp):
        if t == 1:
            fit += 2*km_cov[i]
        if t == 0:
            fit += km_cov[i]
        if t == 1 and zcov[i] == 0:
            fit -= (route.sections[i].distance*0.001 - km_cov[i])*10000

    #print_info(individual, km_cov, zcov, charge, fit, arrival_times)

    return fit,


# ****Evolutionary algorithm configuration****
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(route.sections))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", eval_zone)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.10)
toolbox.register("select", tools.selTournament, tournsize=2)


# ****Returns the best zone assignment found****
def zone_assignment_system():
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, 100, 100, cxpb=0.5, mutpb=0.2, ngen=20, stats=stats, halloffame=hof,
                                       verbose=False)

    return pop, logbook, hof


# ****Experiment execution****
if __name__ == "__main__":
    pop, log, hof = zone_assignment_system()
    print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))

    # ****Writes the dataset in a csv file****
    # The format of the data is:
    # [green expected, normal expected, distance, slope, remaining charge, remaining meters (normal),
    # remaining meters (green), output of the GA for this section]

    aux = 'datasets/dataset' + str(float(sys.argv[1])*100)[:-2] + '.csv' # clear datasets folder before execute this
    with open(aux, mode='a', newline='') as dataset:
        dataset_writer = csv.writer(dataset, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        main_bus = Bus(1, route, ct.initial_charge, [3500, 2800, 1125, 800, 3000, 2200, 2340], 1.3)

        [km_cov, zcov, remaining_charge, charges] = Simulation.simulation_noSchedule(hof[0], main_bus, zexp)

        #print("The expected sections to be covered\n%s" % zexp)
        #print("The sections covered\n%s" % zcov)
        #print("The remaining charge %skWh" % remaining_charge)

        total_km_normal = sum([x.distance if x.section_type == 0 else 0 for x in route.sections])
        total_km_green = sum([x.distance if x.section_type == 1 else 0 for x in route.sections])
        travelled_km_normal = 0
        travelled_km_green = 0
        for i in range(len(hof[0])):
            if route.sections[i].section_type == 0:
                green_exp = '0'
                normal_exp = '1'
            else:
                green_exp = '1'
                normal_exp = '0'
            distance = route.sections[i].distance
            slope = route.sections[i].slope
            charge = charges[i]
            remaining_normal = total_km_normal - travelled_km_normal
            remaining_green = total_km_green - travelled_km_green
            travelled_km_normal += distance if route.sections[i].section_type == 0 else 0
            travelled_km_green += distance if route.sections[i].section_type == 1 else 0
            y = hof[0][i]
            dataset_writer.writerow([green_exp, normal_exp, distance, slope, charge, remaining_normal, remaining_green, y])


