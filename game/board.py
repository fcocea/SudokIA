import importlib.util
import pygame as pg
from back.utils import is_complete, get_unassigned_locations, get_possible_values, combined_heuristic
from game.cell import Cell
import pandas as pd
import numpy as np
import genetic.genes as gn
import genetic.genetic_algorithm as ga
import genetic.fitness as ft
import random as rndm
from cnn.test import denorm, norm
# Population size
POPULATION = 1000
# Number of generations
REPETITION = 1000
# Probability of mutation
PM = 0.1
# Probability of crossover
PC = 0.95

DATA = pd.read_csv('data/test.csv').to_numpy()
keras = None

METHODS = {
    'cnn': 'Redes Neuronales Convolucionales',
    'classic': 'Backtracking Clásico',
    'gen': 'Algoritmo Genético',
    'combined': 'Heurística Combinada (LCV | MRV) - Backtracking'
}


class Board:
    def __init__(self, screen: pg.display, cnn_model=None, need_domains=False):
        self.screen = screen
        self.board = np.reshape([int(c) for c in DATA[0]], (9, 9))
        self.solved_board = np.reshape([int(c) for c in DATA[1]], (9, 9))
        self.cells = [[Cell(screen, i * 60, j * 60, self.board[i][j])
                       for j in range(9)] for i in range(9)]

        self.cnn_model = cnn_model
        self.cnn_feet = norm(self.board.copy()) if cnn_model else None
        self.finished = False
        # self.domains = None if not need_domains else utils.initialize_domains(
        #     self.board)

    def update_cell(self, x: int, y: int, value: int):
        self.board[x][y] = value
        self.cells[x][y].value = value

    def draw_board(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
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

    def classic_back_solver(self):
        self.draw_board()
        if is_complete(self.board):
            if not self.finished:
                print('Sudoku resuelto!')
            self.finished = True
            return True
        unassigned = get_unassigned_locations(self.board)
        if not unassigned:
            return False
        row, col = unassigned[0]
        for num in get_possible_values(
                self.board, row, col):
            if num != self.solved_board[row][col]:
                self.cells[row][col].update_color((255, 0, 0))
            else:
                self.cells[row][col].update_color((0, 71, 171))
            self.update_cell(row, col, num)
            self.board[row][col] = num
            pg.time.delay(52)
            self.draw_board()
            if self.classic_back_solver():
                return True
            self.board[row][col] = 0
            self.update_cell(row, col, 0)
            pg.time.delay(52)
            self.draw_board()
        return None

    def combined_solver(self):
        self.draw_board()
        if is_complete(self.board):
            if not self.finished:
                print('Sudoku resuelto!')
            self.finished = True
            return True
        next = combined_heuristic(self.board)
        if next is None:
            return False
        row, col = next

        for num in get_possible_values(
                self.board, row, col):
            if num != self.solved_board[row][col]:
                self.cells[row][col].update_color((255, 0, 0))
            else:
                self.cells[row][col].update_color((0, 71, 171))
            self.update_cell(row, col, num)
            self.board[row][col] = num
            pg.time.delay(52)
            self.draw_board()
            if self.combined_solver():
                return True
            self.board[row][col] = 0
            self.update_cell(row, col, 0)
            pg.time.delay(52)
            self.draw_board()
        return None

    def cnn_solver(self):
        self.draw_board()
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
                print('Sudoku resuelto!')
            return True
        while True:
            out = self.cnn_model.predict(
                self.cnn_feet.reshape((1, 9, 9, 1)), verbose=None).squeeze()
            pred = np.argmax(out, axis=-1) + 1
            prob = np.around(np.max(out, axis=-1), 2)
            self.cnn_feet = denorm(self.cnn_feet).reshape((9, 9))
            mask = (self.cnn_feet == 0)
            if (mask.sum() == 0):
                break
            ind = np.argmax(prob * mask)
            x, y = (ind // 9), (ind % 9)
            val = pred[x][y]
            self.cnn_feet[x][y] = val
            if val != self.solved_board[x][y]:
                print(
                    f"Error: Se esperaba {self.solved_board[x][y]} pero se obtuvo {val}")
                self.cells[x][y].update_color((255, 0, 0))
            else:
                self.cells[x][y].update_color((0, 71, 171))
            self.update_cell(x, y, val)
            self.draw_board()
            print(
                f"Actualizando la celda ({x}, {y}) con {val}")
            self.cnn_feet = norm(self.cnn_feet)

    def gen_solver(self):
        self.draw_board()
        if self.finished:
            return True
        initial = self.board.copy()
        population = gn.make_population(POPULATION, initial)
        for index in range(REPETITION):
            mating_pool = ga.r_get_mating_pool(population)
            rndm.shuffle(mating_pool)
            population = ga.get_offsprings(mating_pool, initial, PM, PC)
            fit = [ft.get_fitness(c) for c in population]
            m = max(fit)
            print(f'Generación {index + 1} - Fitness: {m}')
            for c in population:
                if ft.get_fitness(c) == m:
                    for i in range(9):
                        for j in range(9):
                            if c[i][j] != self.board[i][j]:
                                self.update_cell(i, j, c[i][j])
                                if c[i][j] != self.solved_board[i][j]:
                                    self.cells[i][j].update_color((255, 0, 0))
                                else:
                                    self.cells[i][j].update_color((0, 0, 0))
                    self.draw_board()
            if m == 0:
                self.finished = True
                break
        if not self.finished:
            print(
                f'No se pudo resolver el Sudoku en {REPETITION} repeticiones')
            self.finished = True
        else:
            print('Sudoku resuelto!')


def run_game(method, model_path=None, index=None):
    global DATA
    random_index = np.random.randint(0, len(DATA))
    if index is not None:
        if index < len(DATA):
            DATA = DATA[index]
        else:
            DATA = DATA[random_index]
    else:
        DATA = DATA[random_index]
    print(f"Resolviendo Sudoku con el método {METHODS[method]}")
    model = None
    if method == 'cnn':
        global keras
        print(f'Cargando modelo de red neuronal... ({model_path})')
        spec = importlib.util.find_spec('keras')
        if spec is not None:
            keras = importlib.import_module('keras')
        if keras is None:
            print('No se encontró el módulo keras')
            exit(1)
        if model_path is None:
            print('No se especificó el modelo de CNN')
            exit(1)
        model = keras.models.load_model(model_path)
    try:
        pg.init()
        screen = pg.display.set_mode((540, 540))
        screen.fill((255, 255, 255))
        pg.display.set_caption(
            f'SudokIA | {METHODS[method]} | {random_index if index is None else index}')
        board = Board(screen, cnn_model=model)
        running = True
        while running:
            board.draw_board()
            if method == 'classic':
                board.classic_back_solver()
            if method == 'combined':
                board.combined_solver()
            elif method == 'cnn':
                board.cnn_solver()
            elif method == 'gen':
                board.gen_solver()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
            pg.time.Clock().tick(60)
    except KeyboardInterrupt:
        pg.quit()
        exit()
