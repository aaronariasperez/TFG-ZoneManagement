import Simulation
from Bus import Bus
from Create_route_csv import read_route
import Constants as ct
import random
import numpy
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import csv


# ****Parameters and environment initialization****
path_windows2 = 'E:\Dropbox\TFG\TFG_code\\route.csv'
path_linux2 = r'/home/aaron/Dropbox/TFG/TFG_code/route.csv'

#create_route(path_windows)  # use when a new green section assignation required (random)
route = read_route(path_windows2)

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
        if t == 1 and zcov[i] == 1:
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

    pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, 100, 100, cxpb=0.5, mutpb=0.2, ngen=10, stats=stats, halloffame=hof,
                                       verbose=False)

    return pop, logbook, hof


# ****Experiment execution****
if __name__ == "__main__":
    pop, log, hof = zone_assignment_system()
    print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))

    main_bus = Bus(1, route, ct.initial_charge, [3500, 2800, 1125, 800, 3000, 2200, 2340], 1.3)

    [km_cov, zcov, remaining_charge, charges] = Simulation.simulation_noSchedule(hof[0], main_bus, zexp)

    print("The expected sections to be covered\n%s" % zexp)
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

    # ****Write the solution in the format: [fitness,0,1,0,....]****
    with open('solution_ev.csv', mode='w', newline='') as dataset:
        dataset_writer = csv.writer(dataset, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        aux = [hof[0].fitness.values[0]]
        aux = aux + hof[0]

        dataset_writer.writerow(aux)

    # ****Plot the fitness by generations (minimum, maximum, average)****
    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")
    plt.show()


