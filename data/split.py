import pandas as pd
import numpy as np


def split_data(data, split_ratio=0.8):
    """Split data into training and testing datasets."""
    np.random.seed(42)
    mask = np.random.rand(len(data)) < split_ratio
    return data[mask], data[~mask]


def load_data():
    """Load data from CSV."""
    return pd.read_csv('data/data.csv')


def save_data(data, filename):
    """Save data to CSV."""
    data.to_csv(filename, index=False)


if __name__ == '__main__':
    data = load_data()
    train, test = split_data(data)
    save_data(train, 'data/train.csv')
    save_data(test, 'data/test.csv')
