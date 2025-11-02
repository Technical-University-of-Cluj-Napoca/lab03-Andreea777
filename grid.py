from utils import *
from spot import Spot
import pygame

class Grid:
    def __init__(self, win: pygame.Surface, rows: int, cols: int, width: int, height: int):
        self.win: pygame.Surface = win
        self.rows: int = rows
        self.cols: int = cols
        self.width: int = width
        self.height: int = height
        self.grid: list[list[Spot]] = self._make_grid()

    def _make_grid(self) -> list[list[Spot]]:
        grid = []
        spot_width = self.width // self.rows
        spot_height = self.height // self.cols
        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                spot = Spot(i, j, spot_width, spot_height, self.rows)
                grid[i].append(spot)
        return grid

    def draw_grid_lines(self) -> None:
        spot_width = self.width // self.rows
        spot_height = self.height // self.cols
        for i in range(self.rows):
            pygame.draw.line(self.win, COLORS['GREY'], (0, i * spot_height), (self.width, i * spot_height))
        for j in range(self.cols):
            pygame.draw.line(self.win, COLORS['GREY'], (j * spot_width, 0), (j * spot_width, self.height))

    def draw(self) -> None:
        self.win.fill(COLORS['WHITE'])
        for row in self.grid:
            for spot in row:
                spot.draw(self.win)
        self.draw_grid_lines()

    def get_clicked_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        spot_width = self.width // self.cols
        spot_height = self.height // self.rows
        x, y = pos

        row = y // spot_height  
        col = x // spot_width 

        return row, col  


    def reset(self) -> None:
        for row in self.grid:
            for spot in row:
                spot.reset()

    def reset_visual(self) -> None:
        for row in self.grid:
            for spot in row:
                if not spot.is_barrier() and not spot.is_start() and not spot.is_end():
                    spot.reset()
