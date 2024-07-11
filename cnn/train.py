
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import keras
from keras.optimizers import Adam
from keras.layers import Activation
from keras.layers import Conv2D, BatchNormalization, Dense, Flatten, Reshape, Dropout

df = pd.read_csv('./data/train.csv')

X = np.array(df.quizzes.map(lambda x: list(
    map(int, x))).to_list()).reshape(-1, 9, 9, 1)
X = X / 9
X -= .5
Y = np.array(df.solutions.map(lambda x: list(
    map(int, x))).to_list()).reshape(-1, 9, 9)
Y -= 1


def get_model():

    model = keras.models.Sequential()

    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu',
              padding='same', input_shape=(9, 9, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3),
              activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3),
              activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3),
              activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3),
              activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3),
              activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3),
              activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3),
              activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(512, kernel_size=(3, 3),
              activation='relu', padding='same'))
    model.add(Flatten())
    model.add(Dense(81*9))
    model.add(Dropout(0.1))
    model.add(keras.layers.LayerNormalization(axis=-1))
    model.add(Reshape((9, 9, 9)))
    model.add(Activation('softmax'))

    return model


def train_model():
    model = get_model()
    adam = Adam(learning_rate=0.001)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)
    model.fit(X, Y, batch_size=32, epochs=2)
    model.save('./cnn/solverModel.keras')
