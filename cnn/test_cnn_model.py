import keras
import numpy as np
import copy

"""This file will load the keras model and 
allow you to run a sudoku game on it to test"""

model = keras.models.load_model('solverModel.keras')


def denorm(a):
    return (a+.5)*9


def norm(a):

    return (a/9)-.5


def inference_sudoku(sample):
    '''
        This function solves the sudoku by filling blank positions one by one.
    '''

    feat = copy.copy(sample)

    while (1):

        # predicting values
        out = model.predict(feat.reshape((1, 9, 9, 1)))
        out = out.squeeze()

        # getting predicted values
        pred = np.argmax(out, axis=1).reshape((9, 9)) + 1
        # getting probability of each value
        prob = np.around(np.max(out, axis=1).reshape((9, 9)), 2)
        # creating mask for blank values
        feat = denorm(feat).reshape((9, 9))
        # i.e it will give you a 2D array with True/1 and False/0 where 0 is found and where 0 is not found respectively
        mask = (feat == 0)

        # if there are no 0 values left then break
        if (mask.sum() == 0):
            break

        # getting probabilities of values where 0 is present, which are the blank values we need to fill
        prob_new = prob * mask

        # getting highest probability index
        ind = np.argmax(prob_new)
        # getting row and col
        x, y = (ind // 9), (ind % 9)

        # getting predicted value at that cell
        val = pred[x][y]
        # assigning that value
        feat[x][y] = val

        # Print the current state of the board after each update
        print(f"Updated board after filling cell ({x}, {y}) with value {val}:")
        # print(feat)

        # again passing this sudoku with one value added to model to get the next most confident value
        feat = norm(feat)

    return pred


def solve_sudoku(game):

    game = game.replace('\n', '')
    game = game.replace(' ', '')
    game = np.array([int(j) for j in game]).reshape((9, 9, 1))
    game = norm(game)
    game = inference_sudoku(game)
    return game


# TODO: Try changing this to another 9x9 game and see if it solves it!
game = '''
          0 8 0 0 3 2 0 0 1
          7 0 3 0 8 0 0 0 2
          5 0 0 0 0 7 0 3 0
          0 5 0 0 0 1 9 7 0
          6 0 0 7 0 9 0 0 8
          0 4 7 2 0 0 0 5 0
          0 0 0 6 0 0 0 0 9
          8 0 6 0 9 0 3 2 0
          3 0 0 8 2 0 0 1 7
      '''

game = solve_sudoku(game)

for i in game:
    print(i)
