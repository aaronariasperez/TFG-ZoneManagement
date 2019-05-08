from keras.datasets import mnist
from keras.models import Sequential
from keras.utils import np_utils
from keras.layers.core import Dense, Activation
import numpy as np
import csv


def shuffle_two_arrays(x, y):
    rng_state = np.random.get_state()
    np.random.shuffle(x)
    np.random.set_state(rng_state)
    np.random.shuffle(y)


def main(x_train, x_test, y_train, y_test):
    input_size = 3
    batch_size = 10
    hidden_neurons = 10
    epochs = 12000

    model = Sequential()
    model.add(Dense(hidden_neurons, input_dim=input_size))
    model.add(Activation('sigmoid'))
    model.add(Dense(hidden_neurons, input_dim=hidden_neurons))
    model.add(Activation('sigmoid'))
    model.add(Dense(hidden_neurons, input_dim=hidden_neurons))
    model.add(Activation('sigmoid'))
    model.add(Dense(hidden_neurons, input_dim=hidden_neurons))
    model.add(Activation('sigmoid'))
    model.add(Dense(hidden_neurons, input_dim=hidden_neurons))
    model.add(Activation('sigmoid'))
    model.add(Dense(classes, input_dim=hidden_neurons))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'],
                  optimizer='sgd')

    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,
              verbose=1)

    score = model.evaluate(x_test, y_test, verbose=1)
    print('Test accuracy:', score[1])

    return model


# ****Read dataset from csv and reformat it****
x = []
y = []

path_windows = 'E:\Dropbox\TFG\TFG_code\dataset.csv'
path_linux = r'/home/aaron/Dropbox/TFG/TFG_code/dataset.csv'

with open(path_linux, mode='r') as dataset:
    csv_reader = csv.reader(dataset, delimiter=',')
    for row in csv_reader:
        #x.append([float(x) for x in row[:-1]])
        x.append([float(x) for x in np.take(row,[0,1,3])])
        y.append([float(x) for x in row[-1:]])

x = np.array(x)
classes = 2
y = np_utils.to_categorical(np.array(y), classes)

print(np.shape(x))

print(y[0])
print(y[3])

shuffle_two_arrays(x, y)

p = int(0.7*x.shape[0])

x_train = x[:p, :]
y_train = y[:p, :]
x_test = x[p:, :]
y_test = y[p:, :]

model = main(x_train, x_test, y_train, y_test)

model.save('trained_model.h5')

