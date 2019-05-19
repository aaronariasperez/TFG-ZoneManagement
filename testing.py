from keras.models import Sequential
from keras.utils import np_utils
from keras.layers.core import Dense, Activation
import numpy
import time
import random

input_size = 6
batch_size = 32
hidden_neurons = 10
hidden_layers = 3
classes = 2
epochs = 10000

start = time.time()
model = Sequential()
for i in range(hidden_layers):
    model.add(Dense(hidden_neurons, input_dim=input_size))
    model.add(Activation('sigmoid'))

model.add(Dense(classes, input_dim=hidden_neurons))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', metrics=['accuracy'],
              optimizer='adamax')

#layer1 = model.layers[0]
#layer2 = model.layers[2]
#layer3 = model.layers[4]
#layer4 = model.layers[6]
#
#w = layer1.get_weights()
#print(w)
#print(list([np.array([[0.]*10]*6), w[1]]))
#layer1.set_weights(list([numpy.array([[0.]*10]*6), w[1]]))
#w = layer1.get_weights()
#print(w)
end = time.time()

individual = [random.random()]*312
model.layers[0].set_weights(list([numpy.array(numpy.reshape(individual[:60], (6, 10))), numpy.array(individual[60:70])]))
model.layers[2].set_weights(list([numpy.array(numpy.reshape(individual[70:170], (10, 10))), numpy.array(individual[170:180])]))
model.layers[4].set_weights(list([numpy.array(numpy.reshape(individual[180:280], (10, 10))), numpy.array(individual[280:290])]))
model.layers[6].set_weights(list([numpy.array(numpy.reshape(individual[290:310], (10, 2))), numpy.array(individual[310:])]))

for w in model.get_weights():
    print("*******************")
    print(w)
    print(len(w))
    a=1

for layer in model.layers:
    for w in layer.get_weights():
        b = w
        a=1