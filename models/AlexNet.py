from keras.models import Sequential
from keras.layers import Dense, Flatten, Lambda, Activation, BatchNormalization
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import AveragePooling2D
from keras.optimizers import Nadam

def AlexNet(learning_rate = 0.1, width=640, height=480, channels=3, normalize_input=False):
    ch, row, col = channels, height, width  # camera format

    model = Sequential()

    if normalize_input:
        model.add(Lambda(lambda x: x / 127.5 - 1.,
                         input_shape=(row, col, ch),
                         output_shape=(row, col, ch)))

    model.add(Convolution2D(64, 3, 11, 11, border_mode='full'))
    model.add(BatchNormalization((64,226,226)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(poolsize=(3, 3)))

    model.add(Convolution2D(128, 64, 7, 7, border_mode='full'))
    model.add(BatchNormalization((128,115,115)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(poolsize=(3, 3)))

    model.add(Convolution2D(192, 128, 3, 3, border_mode='full'))
    model.add(BatchNormalization((128,112,112)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(poolsize=(3, 3)))

    model.add(Convolution2D(256, 192, 3, 3, border_mode='full'))
    model.add(BatchNormalization((128,108,108)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(poolsize=(3, 3)))

    model.add(Flatten())
    model.add(Dense(12*12*256, 4096, init='normal'))
    model.add(BatchNormalization(4096))
    model.add(Activation('relu'))
    model.add(Dense(4096, 4096, init='normal'))
    model.add(BatchNormalization(4096))
    model.add(Activation('relu'))
    model.add(Dense(4096, 1000, init='normal'))
    model.add(BatchNormalization(1000))
    model.add(Dense(1, activation='tanh'))

    model.compile(optimizer=Nadam(lr=learning_rate), loss="mse", metrics=['accuracy'])
    model.summary()

    return model
