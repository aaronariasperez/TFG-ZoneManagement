import random
import numpy
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

bag_prices = [2, 5, 5, 7, 7, 2]
bag_weights = [1, 4, 3, 7, 4, 2]
bag_existences = [2, 1, 3, 5, 2, 3]
max_weight = 30


def eval_bag(individual):
    fit = 0
    current_weight = 0
    for i, elements in enumerate(individual):
        if elements > bag_existences[i] or current_weight > max_weight:
            return -100, (current_weight - max_weight)**2# + (elements - bag_existences[i])
        else:
            fit += bag_prices[i] * elements
            current_weight += bag_weights[i] * elements
    if current_weight > 30:
        return -100, (current_weight - max_weight) ** 2# + (elements - bag_existences[i])

    return fit, current_weight

def mutKnapsack(individual):
    if random.random() < 0.5:
        individual[random.randrange(len(individual))] += 1
    else:
        aux = individual[random.randrange(len(individual))] - 1
        if aux > 0:
            individual[random.randrange(len(individual))] = aux
    return individual,

creator.create("FitnessMax", base.Fitness, weights=(1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 5)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(bag_prices))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", eval_bag)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutKnapsack)
toolbox.register("select", tools.selNSGA2)


def main():
    pop = toolbox.population(n=50)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, stats=stats, halloffame=hof,
                                       verbose=True)

    return pop, logbook, hof


if __name__ == "__main__":
    pop, log, hof = main()
    print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))

    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")
    plt.show()
