from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.utils import np_utils
from keras.layers.core import Dense, Activation


x, y = load_iris(True)

x = np.array(x)
y = np.array(y)
pca = PCA(n_components=2)
pca.fit(x)

PCA(copy=True, n_components=2, whiten=False)

x_ = pca.transform(x)

x1 = x[np.argwhere(y==0)[:, 0], :]
x2 = x[np.argwhere(y==1)[:, 0], :]
x3 = x[np.argwhere(y==2)[:, 0], :]

#plt.scatter(x1[:,0],x1[:,1],c='red')
#plt.scatter(x2[:,0],x2[:,1],c='blue')
#plt.scatter(x3[:,0],x3[:,1],c='green')

#plt.show()


def shuffle_two_arrays(x, y):
    rng_state = np.random.get_state()
    np.random.shuffle(x)
    np.random.set_state(rng_state)
    np.random.shuffle(y)


def main(x_train, x_test, y_train, y_test):
    input_size = 4
    batch_size = 20
    hidden_neurons = 8
    epochs = 5000

    model = Sequential()
    model.add(Dense(hidden_neurons, input_dim=input_size))
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


classes = 3
y = np_utils.to_categorical(np.array(y), classes)

print(y)

shuffle_two_arrays(x, y)

print(x.shape)

p = int(0.7*x.shape[0])

x_train = x[:p, :]
y_train = y[:p, :]
x_test = x[p:, :]
y_test = y[p:, :]

model = main(x_train, x_test, y_train, y_test)

#prediction = model.predict(np.array([[1, 0, 100, -20, 100, 10]]))
#print(prediction)