from os import environ
from bck import solve, is_valid

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
import pandas as pd
import numpy as np

DATA = pd.read_csv('data/data-1.csv').to_numpy()[0]


class Cell:
    def __init__(self, screen: pg.display, x: int, y: int, value: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.value = value
        self.rect = pg.Rect(x, y, 60, 60)

    def draw(self, color: tuple[int, int, int], thickness: int = 1) -> None:
        pg.draw.rect(self.screen, color, self.rect, thickness)

    def display(self, value: int, position: tuple[int, int], color: tuple[int, int, int]) -> None:
        font = pg.font.SysFont(None, 45)
        text = font.render(str(value), True, color)
        self.screen.blit(text, position)


class Board:
    def __init__(self, screen: pg.display):
        self.screen = screen
        self.board = np.reshape([int(c) for c in DATA[0]], (9, 9))
        self.solved_board = self.board.copy()
        print(self.board)
        solve(self.solved_board)
        print(self.solved_board)
        self.cells = [[Cell(screen, i * 60, j * 60, self.board[i][j]) for j in range(9)] for i in range(9)]

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
                    _cell.display(_cell.value, (21 + j * 60, 16 + i * 60), (0, 0, 0))
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
            return True
        for nums in range(9):
            if is_valid(self.board, empty[0], empty[1], nums + 1):
                self.board[empty[0]][empty[1]] = nums + 1
                self.cells[empty[0]][empty[1]].value = nums + 1
                pg.time.delay(52)
                self.draw_board()
                if self.dfs_solver():
                    return True
                self.board[empty[0]][empty[1]] = 0
                self.cells[empty[0]][empty[1]].value = 0
                pg.time.delay(62)
                self.draw_board()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((540, 540))
    screen.fill((255, 255, 255))
    pg.display.set_caption('Sudoku')
    board = Board(screen)
    running = True
    while running:
        board.dfs_solver()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
        pg.time.Clock().tick(60)
