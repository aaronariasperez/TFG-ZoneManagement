import Simulation
from Bus import Bus
from Route import Route
from Section import Section
import Constants as ct
import random
import numpy
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms


# ****Parameters and environment initialization****
sec1 = Section(1, 0, 0, 1200, False, ct.avg_speed)
sec2 = Section(2, 0, 5, 1500, True, ct.avg_speed)
sec3 = Section(3, 0, 10, 1450, True, ct.avg_speed)
sec4 = Section(4, 0, 0, 2400, True, ct.avg_speed)
sec5 = Section(5, 1, -10, 1450, False, ct.avg_speed)
sec6 = Section(6, 0, -5, 1500, False, ct.avg_speed)
sec7 = Section(7, 1, 0, 1200, True, ct.avg_speed)

route = Route(1, [sec1, sec2, sec3, sec4, sec5, sec6, sec7], [(8,0), (8,4), (8,8), (8,12), (8,19), (8,23), (8,27), (8,31)])

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
    main_bus = Bus(1, route, ct.initial_charge, [3500, 2800, 1125, 800, 3000, 2200, 2340], 1.0)

    [normalKm_cov, greenKm_cov, zcov, charge] = Simulation.simulation(individual, main_bus, zexp)

    fit = sum(zcov)

    for ind, t in enumerate(zexp):
        if t == 1 and zcov[ind] == 0:
            fit -= 1000

    #print(individual, end='')
    #print(" valor: "+str(fit))

    return fit,


def eval_zone2(individual):
    main_bus = Bus(1, route, ct.initial_charge, [3500, 2800, 1125, 800, 3000, 2200, 2340], 1.3)

    [arrival_times, km_cov, zcov, charge] = Simulation.simulation(individual, main_bus, zexp)

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

toolbox.register("evaluate", eval_zone2)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.10)
toolbox.register("select", tools.selTournament, tournsize=2)


# ****Returns the best zone assignment found****
def zone_assignment_system():
    pop = toolbox.population(n=50)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, 100, 100, cxpb=0.5, mutpb=0.2, ngen=100, stats=stats, halloffame=hof,
                                       verbose=True)

    return pop, logbook, hof


# ****Experiment execution****
if __name__ == "__main__":
    pop, log, hof = zone_assignment_system()
    print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))

    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")
    plt.show()
