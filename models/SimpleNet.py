from keras.models import Sequential
from keras.layers import Dense, Flatten, Lambda, Dropout
from keras.optimizers import Nadam

def SimpleNet(learning_rate = 0.1, width=320, height=240, channels=3, normalize_input=False):
    ch, row, col = channels, height, width  # camera format
    model = Sequential()

    if normalize_input:
        model.add(Lambda(lambda x: x / 127.5 - 1.,
                         input_shape=(row, col, ch),
                         output_shape=(row, col, ch)))
        model.add(Flatten())
    else:
        model.add(Flatten(input_shape=(row, col, ch)))
    model.add(Dense(100))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='tanh'))

    model.compile(optimizer=Nadam(lr=learning_rate), loss="mse", metrics=['accuracy'])
    model.summary()
    return model