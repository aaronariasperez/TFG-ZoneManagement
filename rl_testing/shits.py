from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from scipy.spatial import distance
import sklearn.preprocessing

model = Sequential()

model.add(Convolution2D(nb_filter=10, nb_row=2, nb_col=2,
                        input_shape=(64,64,1)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))

model.add(Convolution2D(nb_filter=10, nb_row=2, nb_col=2,
                        input_shape=(10, 21, 21)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(nb_filter=10, nb_row=2, nb_col=2,
                        input_shape=(10, 10, 10)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))

model.add(Convolution2D(nb_filter=3, nb_row=2, nb_col=2,
                        input_shape=(10, 3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# The model needs to be compiled before it can be used for prediction
sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

print(len(model.get_weights()))

for w in model.get_weights():
    print("*******************")
    print(w)
    print(len(w))
    a=1