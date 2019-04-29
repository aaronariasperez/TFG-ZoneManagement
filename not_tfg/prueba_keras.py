from keras.datasets import mnist
from keras.models import Sequential
from keras.utils import np_utils
from keras.layers.core import Dense, Activation


def main(x_train, x_test, y_train, y_test):
    input_size = 784
    batch_size = 100
    hidden_neurons = 100
    epochs = 1

    model = Sequential()
    model.add(Dense(hidden_neurons, input_dim=input_size))
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


(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)

print(y_test.shape)
x_train = x_train.reshape(60000, 784)

x_test = x_test.reshape(10000, 784)
classes = 10
y_train = np_utils.to_categorical(y_train, classes)

y_test = np_utils.to_categorical(y_test, classes)

print(y_train.shape)
print(y_test.shape)


main(x_train, x_test, y_train, y_test)
