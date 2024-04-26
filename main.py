from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
import pandas as pd
import numpy as np

DATA = pd.read_csv('data/data-1.csv').to_numpy()[32]


class Cell:
    def __init__(self, screen, x, y, value):
        self.rect = pg.Rect(x, y, 60, 60)
        self.screen = screen
        self.x = x
        self.y = y
        self.value = value

    def draw_cell(self):
        font = pg.font.Font(None, 45)
        text = font.render(str(self.value), True, (0, 0, 0))
        self.screen.blit(text, (self.x * 60 + 20, self.y * 60 + 10))

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.board = np.reshape([int(c) for c in DATA[0]], (9, 9))

    def draw_board(self):
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
                if self.board[i][j] != 0:
                    cell = Cell(self.screen, j, i, self.board[i][j])
                    cell.draw_cell()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((540, 540))
    screen.fill((255, 255, 255))
    pg.display.set_caption('Sudoku')
    board = Board(screen)
    running = True
    while running:
        board.draw_board()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
        pg.display.flip()
        pg.time.Clock().tick(60)
