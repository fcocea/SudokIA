import numpy as np


def denorm(a):
    return (a+.5)*9


def norm(a):
    return (a/9)-.5


def prediction(board, model):
    if model is None:
        return None
    feet = norm(board)
    while True:
        out = model.predict(feet.reshape(1, 9, 9, 1), verbose=None).squeeze()
        pred = np.argmax(out, axis=-1) + 1
        prob = np.around(np.max(out, axis=-1), 2)
        feet = denorm(feet).reshape((9, 9))
        mask = (feet == 0)
        if (mask.sum() == 0):
            break
        ind = np.argmax(prob * mask)
        x, y = (ind // 9), (ind % 9)
        val = pred[x][y]
        feet[x][y] = val
        feet = norm(feet)
    return pred
