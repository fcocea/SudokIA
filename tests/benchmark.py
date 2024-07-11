import importlib.util
keras = None


def run_test(method='classic', model_path=None, all=None):
    if method == 'cnn' or all:
        global keras
        if keras is None:
            keras = importlib.import_module('keras')
        model = keras.models.load_model(model_path)

    print("Running test")
