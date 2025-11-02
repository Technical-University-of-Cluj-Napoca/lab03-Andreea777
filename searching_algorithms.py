import pygame
import math
from utils import *
from collections import deque
from queue import PriorityQueue
from grid import Grid
from spot import Spot

def bfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Breadth-First Search (BFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """

    if start is None or end is None:
        return False

    queue = deque([start])
    visited = {start}
    came_from = {}

    while queue:
        # Allow quitting the window while searching
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = queue.popleft()

        # If path is found
        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

def dfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Depdth-First Search (DFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    
    if start is None or end is None:
        return False

    stack = [start]
    visited = {start}
    came_from = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = stack.pop()

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

def h_manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Manhattan distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def h_euclidian_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Euclidian distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def reconstruct_path(came_from, current, draw, start):
    while current in came_from:
        current = came_from[current]
        if current != start:
            current.make_path()
        draw()
    start.make_start()

def astar(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    A* Pathfinding Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """

    if not start or not end:
        return False

    count = 0
    open_heap = PriorityQueue()
    open_heap.put((0, count, start))

    g_score = {spot: float("inf") for row in grid.grid for spot in row}
    f_score = {spot: float("inf") for row in grid.grid for spot in row}
    g_score[start] = 0
    f_score[start] = h_manhattan_distance(start.get_position(), end.get_position())

    came_from = {}
    open_set = {start}

    while not open_heap.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = open_heap.get()[2]
        open_set.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor.is_barrier():
                continue

            temp_g = g_score[current] + 1

            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f = temp_g + h_manhattan_distance(neighbor.get_position(), end.get_position())
                f_score[neighbor] = f

                if neighbor not in open_set:
                    count += 1
                    open_heap.put((f, count, neighbor))
                    open_set.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

def dls(draw, grid, start, end, limit):
    stack = [(start, 0)]
    visited = {start}
    came_from = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current, depth = stack.pop()

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            return True

        if depth < limit:
            for neighbor in current.neighbors:
                if neighbor not in visited and not neighbor.is_barrier():
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    stack.append((neighbor, depth + 1))
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

def iddfs(draw, grid, start, end, max_depth=50):
    for depth in range(max_depth):
        grid.reset_visual()  
        if dls(draw, grid, start, end, depth):
            return True
    return False


def ucs(draw, grid, start, end):
    open_heap = PriorityQueue()
    open_heap.put((0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while not open_heap.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current_cost, current = open_heap.get()

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            return True

        for neighbor in current.neighbors:
            if neighbor.is_barrier():
                continue

            new_cost = current_cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                open_heap.put((new_cost, neighbor))
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False


def greedy(draw, grid, start, end):
    open_heap = PriorityQueue()
    open_heap.put((h_manhattan_distance(start.get_position(), end.get_position()), start))
    came_from = {}
    visited = {start}

    while not open_heap.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        _, current = open_heap.get()

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                open_heap.put((h_manhattan_distance(neighbor.get_position(), end.get_position()), neighbor))
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False


def ida_star(draw, grid, start, end):
    bound = h_manhattan_distance(start.get_position(), end.get_position())

    def search(path, g, bound):
        current = path[-1]
        f = g + h_manhattan_distance(current.get_position(), end.get_position())

        if f > bound:
            return f
        if current == end:
            return True

        min_bound = float('inf')

        for neighbor in current.neighbors:
            if neighbor not in path and not neighbor.is_barrier():
                path.append(neighbor)
                t = search(path, g + 1, bound)
                if t is True:
                    return True
                if t < min_bound:
                    min_bound = t
                path.pop()

        return min_bound

    path = [start]
    while True:
        t = search(path, 0, bound)
        if t is True:
            for spot in path:
                if spot != start and spot != end:
                    spot.make_path()
                    draw()
            return True
        if t == float('inf'):
            return False
        bound = t