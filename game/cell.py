import pygame as pg


class Cell:
    def __init__(self, screen: pg.display, x: int, y: int, value: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.value = value
        self.rect = pg.Rect(x, y, 60, 60)
        self.color = (0, 0, 0)

    def draw(self, color: tuple[int, int, int], thickness: int = 1) -> None:
        pg.draw.rect(self.screen, color, self.rect, thickness)

    def display(self, value: int, position: tuple[int, int]) -> None:
        font = pg.font.SysFont(None, 45)
        text = font.render(str(value), True, self.color)
        self.screen.blit(text, position)

    def update_color(self, color: tuple[int, int, int]) -> None:
        self.color = color
