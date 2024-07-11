import importlib.util
import cnn.test as cnn_test
import pandas as pd
import numpy as np
import time
keras = None

DATA = pd.read_csv('data/test.csv').to_numpy()
TESTS = 1000


def run_test(method='classic', model_path=None, all=None):
    boards, solutions = zip(*[(
        np.reshape([int(c) for c in data[0]], (9, 9)),
        np.reshape([int(c) for c in data[1]], (9, 9))
    ) for data in DATA])
    if method == 'cnn' or all:
        global keras
        if keras is None:
            keras = importlib.import_module('keras')
        model = keras.models.load_model(model_path)
        print(f"Running CNN test ({TESTS})")
        correct = 0
        total_prediction_time = 0
        for i in range(TESTS):
            if i % 100 == 0:
                print(f'CNN: {i}/{TESTS}')
            board, solution = boards[i], solutions[i]
            start = time.time()
            pred = cnn_test.prediction(board, model)
            total_prediction_time += (time.time() - start)
            if np.array_equal(pred, solution):
                correct += 1
        print(f'CNN: {correct}/{TESTS} correct')
        # % correct
        print(f'Accuracy: {correct/TESTS*100:.2f}%')
        print(f'Total prediction time: {total_prediction_time:.2f}s')
        # average
        print(f'Average prediction time: {total_prediction_time/TESTS:.2f}s')

    print("Running test")
