from keras.models import Sequential
from keras.utils import np_utils
from keras.layers.core import Dense, Activation
import numpy as np
import csv
import os


def shuffle_two_arrays(x, y):
    rng_state = np.random.get_state()
    np.random.shuffle(x)
    np.random.set_state(rng_state)
    np.random.shuffle(y)


def main(x_train, x_test, y_train, y_test, n_layers, n_neurons):
    input_size = 6
    batch_size = 32
    hidden_neurons = n_neurons
    epochs = 10000

    model = Sequential()
    for i in range(n_layers):
        model.add(Dense(hidden_neurons, input_dim=input_size))
        model.add(Activation('sigmoid'))

    model.add(Dense(classes, input_dim=hidden_neurons))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'],
                  optimizer='adamax')

    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,
              verbose=1, validation_split=0.1)

    score = model.evaluate(x_test, y_test, verbose=1)
    print('Test accuracy:', score[1])

    return model, score[1]


# ****Read dataset from csv and reformat it****
x = []
y = []

path_windows = 'E:\Dropbox\TFG\TFG_code\\norm_dataset.csv'
path_linux = r'/home/aaron/Dropbox/TFG/TFG_code/norm_dataset.csv'

with open(path_windows, mode='r') as dataset:
    csv_reader = csv.reader(dataset, delimiter=',')
    for row in csv_reader:
        x.append([float(x) for x in row[:-1]])
        #x.append([float(x) for x in np.take(row,[0,1,3,4,5,6])])
        y.append([float(x) for x in row[-1:]])

# ****This is for balance the data (50% of each class)****
number_of_electrics = sum([a[0] for a in y])
shuffle_two_arrays(x, y)
cont = 0
i = 0
total = len(y)
while cont < (total-(2*number_of_electrics)):
    if y[i][0] == 0:
        del x[i]
        del y[i]
        i -= 1
        cont += 1
    i += 1

# ****Adapting the variables for the training****
print('Number of electrics: %s' % str(sum([a[0] for a in y])))
print('Number of normals: %s' % str(len(y)-sum([a[0] for a in y])))
x = np.array(x)
classes = 2
y = np_utils.to_categorical(np.array(y), classes)

print('Shape of x: %s' % str(np.shape(x)))

shuffle_two_arrays(x, y)

p = int(0.7*x.shape[0])

x_train = x[:p, :]
y_train = y[:p, :]
x_test = x[p:, :]
y_test = y[p:, :]

# ****Train and save the models****
os.remove('static_nn_results.csv')
for n_n in [1]:
    for n_l in [1]:
        model, score = main(x_train, x_test, y_train, y_test, n_l, n_n)
        model.save('models/trained_model'+str(n_l)+'_'+str(n_n)+'.h5')
        f_result = open('static_nn_results.csv', 'a')
        aux = str(n_l)+','+str(n_n)+','+str(score)+'\n'
        f_result.write(aux)


# Test accuracy: 0.7719107241038726 - con 1000 epochs, 1 capa y 40 neuronas y adam
# Test accuracy: 0.7646394273684832 - con 10000 epochs, 3 capas y 10 neuronas y sgd
# Test accuracy: 0.7754491018288544 - con 10000 epochs, 3 capas y 10 neuronas y adam
# Test accuracy: 0.7770821991405477 - con 10000 epochs, 3 capas y 10 neuronas y adamax
# Test accuracy: 0.7509526402390905 - con 10000 epochs, 3 capas y 10 neuronas y adagrad
# Test accuracy: 0.7645617855198693 - con 10000 epochs, 3 capas y 10 neuronas y adadelta
# Test accuracy: 0.7684431138373485 - con 10000 epochs, 3 capas y 10 neuronas y rmsprop
# Test accuracy: 0.7623843221347749 - con 10000 epochs, 3 capas y 10 neuronas y nadam
