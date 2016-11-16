from keras.models import Sequential
from keras.layers import Dense, Flatten, Lambda, Activation, BatchNormalization
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import AveragePooling2D
from keras.optimizers import Nadam

def NvidiaNet(learning_rate = 0.1, width=640, height=480, channels=3, normalize_input=False):
    ch, row, col = channels, height, width  # camera format

    model = Sequential()

    if normalize_input:
        model.add(Lambda(lambda x: x / 127.5 - 1.,
                         input_shape=(row, col, ch),
                         output_shape=(row, col, ch)))

    model.add(Convolution2D(24, 5, 5, subsample=(2, 2)))
    model.add((BatchNormalization(mode=2, axis=3)))
    model.add(Activation('relu'))

    model.add(Convolution2D(36, 5, 5, subsample=(2, 2)))
    model.add((BatchNormalization(mode=2, axis=3)))
    model.add(Activation('relu'))

    model.add(Convolution2D(48, 5, 5, subsample=(2, 2)))
    model.add((BatchNormalization(mode=2, axis=3)))
    model.add(Activation('relu'))

    model.add(AveragePooling2D(pool_size=(4,4)))

    model.add(Convolution2D(64, 3, 3))
    model.add((BatchNormalization(mode=2, axis=3)))
    model.add(Activation('relu'))

    model.add(Convolution2D(64, 3, 3))
    model.add((BatchNormalization(mode=2, axis=3)))
    model.add(Activation('relu'))

    model.add(AveragePooling2D(pool_size=(4,4)))

    model.add(Flatten())
    model.add(Dense(1164))
    model.add((BatchNormalization(mode=2, axis=-1)))
    model.add(Activation('relu'))

    model.add(Dense(100))
    model.add((BatchNormalization(mode=2, axis=-1)))
    model.add(Activation('relu'))

    model.add(Dense(50))
    model.add((BatchNormalization(mode=2, axis=-1)))
    model.add(Activation('relu'))

    model.add(Dense(1, activation='tanh'))

    model.compile(optimizer=Nadam(lr=learning_rate), loss="mse", metrics=['accuracy'])
    model.summary()

    return model
