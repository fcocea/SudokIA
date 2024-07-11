

import importlib.util
import pygame as pg
from bck import is_valid
from game.cell import Cell
import pandas as pd
import numpy as np

DATA = pd.read_csv('data/data-1.csv').to_numpy()[5312]
keras = None

METHODS = {
    'cnn': 'Redes Neuronales Convolucionales',
    'back': 'Backtracking',
    'gen': 'Algoritmo Genético',
}


def denorm(a):
    return (a+.5)*9


def norm(a):
    return (a/9)-.5


class Board:
    def __init__(self, screen: pg.display, cnn_model=None):
        self.screen = screen
        self.board = np.reshape([int(c) for c in DATA[0]], (9, 9))
        self.solved_board = np.reshape([int(c) for c in DATA[1]], (9, 9))
        self.cells = [[Cell(screen, i * 60, j * 60, self.board[i][j])
                       for j in range(9)] for i in range(9)]
        self.cnn_model = cnn_model
        self.cnn_feet = norm(self.board.copy()) if cnn_model else None
        self.finished = False

    def update_cell(self, x: int, y: int, value: int):
        self.board[x][y] = value
        self.cells[x][y].value = value

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        for i in range(9):
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    pg.draw.line(
                        self.screen,
                        (0, 0, 0),
                        (j // 3 * 180, 0),
                        (j // 3 * 180, 540),
                        4,
                    )
                if i % 3 == 0 and i != 0:
                    pg.draw.line(
                        self.screen,
                        (0, 0, 0),
                        (0, i // 3 * 180),
                        (540, i // 3 * 180),
                        4,
                    )
                _cell: Cell = self.cells[i][j]
                _cell.draw((0, 0, 0))
                if _cell.value != 0:
                    _cell.display(
                        _cell.value, (21 + j * 60, 16 + i * 60))
        pg.display.flip()

    def dfs_solver(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        empty = None
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    empty = (i, j)
                    break
            if empty:
                break

        if not empty:
            if not self.finished:
                self.finished = True
                print('Sudoku resuelto')

            return True
        for nums in range(9):
            if is_valid(self.board, empty[0], empty[1], nums + 1):
                self.update_cell(empty[0], empty[1], nums + 1)
                pg.time.delay(52)
                self.draw_board()
                if self.dfs_solver():
                    return True
                self.update_cell(empty[0], empty[1], 0)
                pg.time.delay(52)
                self.draw_board()

    def cnn_solver(self):
        self.draw_board()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
        empty = None
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    empty = (i, j)
                    break
            if empty:
                break

        if not empty:
            if not self.finished:
                self.finished = True
                print('Sudoku resuelto')
            return True
        while True:
            out = self.cnn_model.predict(
                self.cnn_feet.reshape(1, 9, 9, 1)).squeeze()

            pred = np.argmax(out, axis=1).reshape((9, 9)) + 1
            prob = np.around(np.max(out, axis=1).reshape((9, 9)), 2)
            self.cnn_feet = denorm(self.cnn_feet).reshape((9, 9))
            mask = (self.cnn_feet == 0)
            if (mask.sum() == 0):
                break
            prob_new = prob * mask
            ind = np.argmax(prob_new)
            x, y = (ind // 9), (ind % 9)
            val = pred[x][y]
            self.cnn_feet[x][y] = val
            if val != self.solved_board[x][y]:
                print(
                    f"Error: Expected {self.solved_board[x][y]} but got {val}")
                self.cells[x][y].update_color((255, 0, 0))
            self.update_cell(x, y, val)
            self.draw_board()
            print(
                f"Updated board after filling cell ({x}, {y}) with value {val}:")
            self.cnn_feet = norm(self.cnn_feet)


def run_game(method):
    print(f"Resolviendo Sudoku con el método {METHODS[method]}")
    model = None
    if method == 'cnn':
        global keras
        print('Cargando modelo de red neuronal...')
        spec = importlib.util.find_spec('keras')
        if spec is not None:
            keras = importlib.import_module('keras')

        model = keras.models.load_model('cnn/solverModel.keras')
    try:
        pg.init()
        screen = pg.display.set_mode((540, 540))
        screen.fill((255, 255, 255))
        pg.display.set_caption('SudokIA')
        board = Board(screen, cnn_model=model)
        running = True
        while running:
            if method == 'back':
                board.dfs_solver()
            elif method == 'cnn':
                board.cnn_solver()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
            pg.time.Clock().tick(60)
    except KeyboardInterrupt:
        pg.quit()
        exit()
