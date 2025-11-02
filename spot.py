from utils import *

class Spot:
    def __init__(self, row, col, width, height, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.x = col * width
        self.y = row * height
        self.color = COLORS['WHITE']
        self.neighbors = []
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    # checks
    def is_closed(self):
        return self.color == COLORS['RED']

    def is_open(self):
        return self.color == COLORS['GREEN']

    def is_barrier(self):
        return self.color == COLORS['BLACK']

    def is_start(self):
        return self.color == COLORS['ORANGE']

    def is_end(self):
        return self.color == COLORS['YELLOW']

    # setters / state changers
    def reset(self):
        self.color = COLORS['WHITE']

    def make_closed(self):
        self.color = COLORS['RED']

    def make_open(self):
        self.color = COLORS['GREEN']

    def make_barrier(self):
        self.color = COLORS['BLACK']

    def make_start(self):
        self.color = COLORS['ORANGE']

    def make_end(self):
        self.color = COLORS['YELLOW']

    def make_path(self):
        self.color = COLORS['PURPLE']

    def __lt__(self, other):
        return False

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
