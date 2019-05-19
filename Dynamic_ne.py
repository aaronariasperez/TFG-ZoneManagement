import Simulation
from Bus import Bus
from Create_route_csv import read_route
import Constants as ct
import random
import numpy
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from keras.models import Sequential
from keras.layers.core import Dense, Activation
import csv
import time


# ****Parameters and environment initialization****
input_size = 6
batch_size = 32
hidden_neurons = 10
hidden_layers = 3
classes = 2
epochs = 10000

# ****Create the model****
model = Sequential()
for i in range(hidden_layers):
    model.add(Dense(hidden_neurons, input_dim=input_size))
    model.add(Activation('sigmoid'))

model.add(Dense(classes, input_dim=hidden_neurons))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', metrics=['accuracy'],
              optimizer='adamax')

path_windows2 = 'E:\Dropbox\TFG\TFG_code\\routes\\route15.csv'
path_linux2 = r'/home/aaron/Dropbox/TFG/TFG_code/routes/route15.csv'

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


def modify_model(individual):
    model.layers[0].set_weights(
        list([numpy.array(numpy.reshape(individual[:60], (6, 10))), numpy.array(individual[60:70])]))
    model.layers[2].set_weights(
        list([numpy.array(numpy.reshape(individual[70:170], (10, 10))), numpy.array(individual[170:180])]))
    model.layers[4].set_weights(
        list([numpy.array(numpy.reshape(individual[180:280], (10, 10))), numpy.array(individual[280:290])]))
    model.layers[6].set_weights(
        list([numpy.array(numpy.reshape(individual[290:310], (10, 2))), numpy.array(individual[310:])]))


# ****This function evaluates the zone assignment****
def eval_zone(individual):
    modify_model(individual)
    fits = []
    for i in range(10):

        main_bus = Bus(1, route, ct.initial_charge, 1.3)

        #print("******************************")
        #start = time.time()
        [zone_assignment, km_cov, zcov, charge, charges] = Simulation.dynamic_simulation(main_bus, model, normalKm_expected,
                                                                                    greenKm_expected, [max_dist, min_dist, max_slope, min_slope])
        #print("Tiempo de simulacion: %s" % str(time.time()-start))
        fit = 0
        for i, t in enumerate(zexp):
            if t == 1 and zcov[i] == 1:
                fit += 2*km_cov[i]
            if t == 0:
                fit += km_cov[i]
            if t == 1 and zcov[i] == 0:
                fit -= (route.sections[i].distance*0.001 - km_cov[i])*10000
        fits.append(fit)

    return numpy.mean(fits),


# ****Evolutionary algorithm configuration****
individual_size = 312  # 280 weights + 32 biases

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -1, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=individual_size)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", eval_zone)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1.5, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=2)


# ****Returns the best zone assignment found****
def zone_assignment_system():
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, 100, 100, cxpb=0.5, mutpb=0.2, ngen=500, stats=stats, halloffame=hof,
                                       verbose=True)

    return pop, logbook, hof


# ****Experiment execution****
if __name__ == "__main__":
    pop, log, hof = zone_assignment_system()
    #print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))
    print("Best individual fitness: %s" % (hof[0].fitness))

    modify_model(hof[0])
    main_bus = Bus(1, route, ct.initial_charge, 1.3)

    [zone_assignment, km_cov, zcov, remaining_charge, charges] = Simulation.dynamic_simulation(main_bus, model, normalKm_expected, greenKm_expected, [max_dist, min_dist, max_slope, min_slope])

    print("ESTA MEDIDA NO ES REALISTA PORQUE SE ESTA EJECUTANDO UNA VEZ")
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

    model.save('dynamic_model_ne.h5')
#
    ## ****Write the solution in the format: [fitness,0,1,0,....]****
    #with open('solution_ev.csv', mode='w', newline='') as dataset:
    #    dataset_writer = csv.writer(dataset, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#
    #    aux = [hof[0].fitness.values[0]]
    #    aux = aux + hof[0]
#
    #    dataset_writer.writerow(aux)
#
    ## ****Plot the fitness by generations (minimum, maximum, average)****
    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")
    plt.show()


