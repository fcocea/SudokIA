
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import keras
from keras.optimizers import Adam
from keras.layers import Activation
from keras.layers import Conv2D, BatchNormalization, Dense, Flatten, Reshape

df = pd.read_csv('./data/data-1.csv')

feat = np.array([np.array([int(j) for j in i]).reshape((9, 9, 1))
                for i in df['quizzes'].values])
feat = (feat / 9) - 0.5

label = np.array([np.array([int(j) for j in i]).reshape(
    (81, 1)) - 1 for i in df['solutions'].values])

X_train, X_test, y_train, y_test = train_test_split(
    feat, label, test_size=0.33, random_state=42)


def get_model():

    model = keras.models.Sequential()

    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu',
              padding='same', input_shape=(9, 9, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(128, kernel_size=(1, 1),
              activation='relu', padding='same'))

    model.add(Flatten())
    model.add(Dense(81*9))
    model.add(Reshape((-1, 9)))
    model.add(Activation('softmax'))

    return model


def train_model():
    model = get_model()
    adam = Adam(learning_rate=0.001)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)
    model.fit(X_train, y_train, batch_size=32, epochs=2)
    model.save('./cnn/solverModel.keras')
