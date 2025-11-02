import pygame
from utils import *
from grid import Grid
from searching_algorithms import *

pygame.init()
FONT = pygame.font.SysFont("arial", 20)
TITLE_FONT = pygame.font.SysFont("arial", 22, bold=True)
CODE_FONT = pygame.font.SysFont("consolas", 18)

UI_BAR_H = 60
SLIDER_Y = HEIGHT - 40 
SLIDER_X = 200
SLIDER_W = 400
SLIDER_H = 8
HANDLE_R = 10

# default theme on startup
set_theme("Pastel")

# Global speed (delay in milliseconds). Medium by default.
SPEED = 70

def get_delay():
    return SPEED

ALGO_INFO = {
    "BFS": {
        "title": "Breadth-First Search (BFS)",
        "desc": "BFS explores neighbors level-by-level (like ripples). It guarantees the shortest path in an unweighted grid.",
        "pseudocode": [
            "queue ← [start]",
            "visited ← {start}",
            "came_from ← {}",
            "while queue not empty:",
            "    u ← queue.pop_left()",
            "    if u == end: reconstruct_path and return",
            "    for v in neighbors(u):",
            "        if v not in visited and not barrier:",
            "            visited.add(v)",
            "            came_from[v] = u",
            "            queue.append(v)"
        ],
        "time": "O(V + E)",
        "space": "O(V)"
    },
    "DFS": {
        "title": "Depth-First Search (DFS)",
        "desc": "DFS dives as deep as possible before backtracking. It does not guarantee the shortest path in general.",
        "pseudocode": [
            "stack ← [start]",
            "visited ← {start}",
            "came_from ← {}",
            "while stack not empty:",
            "    u ← stack.pop()",
            "    if u == end: reconstruct_path and return",
            "    for v in neighbors(u):",
            "        if v not in visited and not barrier:",
            "            visited.add(v)",
            "            came_from[v] = u",
            "            stack.push(v)"
        ],
        "time": "O(V + E)",
        "space": "O(V) (worst-case recursion/stack)"
    },
    "A*": {
        "title": "A* Search",
        "desc": "A* uses both the path cost so far (g) and a heuristic (h) to the goal. With an admissible heuristic, it is optimal and complete.",
        "pseudocode": [
            "open ← priority queue with (f(start), start)",
            "g[start] = 0; came_from ← {}",
            "while open not empty:",
            "    u ← node with smallest f",
            "    if u == end: reconstruct_path and return",
            "    for v in neighbors(u):",
            "        tentative_g = g[u] + 1",
            "        if tentative_g < g[v]:",
            "            came_from[v] = u",
            "            g[v] = tentative_g",
            "            f[v] = g[v] + h(v, end)",
            "            push v into open"
        ],
        "time": "O(E) average; up to O(V^2) with array-based PQ",
        "space": "O(V)"
    },
    "UCS": {
        "title": "Uniform Cost Search (UCS)",
        "desc": "UCS (Dijkstra for uniform edges) always expands the least-cost frontier node. Guarantees optimal paths in graphs with non-negative weights.",
        "pseudocode": [
            "open ← priority queue with (0, start)",
            "cost[start] = 0; came_from ← {}",
            "while open not empty:",
            "    (c, u) ← pop(open)",
            "    if u == end: reconstruct_path and return",
            "    for v in neighbors(u):",
            "        new_cost = c + 1",
            "        if v not in cost or new_cost < cost[v]:",
            "            cost[v] = new_cost",
            "            came_from[v] = u",
            "            push (new_cost, v) into open"
        ],
        "time": "O(E log V) with a binary heap",
        "space": "O(V)"
    },
    "Greedy": {
        "title": "Greedy Best-First Search",
        "desc": "Greedy expands the node that appears closest to the goal by heuristic only. Fast in practice, but not optimal.",
        "pseudocode": [
            "open ← priority queue with (h(start), start)",
            "visited ← {start}; came_from ← {}",
            "while open not empty:",
            "    (_, u) ← pop(open)",
            "    if u == end: reconstruct_path and return",
            "    for v in neighbors(u):",
            "        if v not in visited and not barrier:",
            "            visited.add(v)",
            "            came_from[v] = u",
            "            push (h(v), v) into open"
        ],
        "time": "O(E) average; depends on heuristic",
        "space": "O(V)"
    },
    "IDDFS": {
        "title": "Iterative Deepening DFS (IDDFS)",
        "desc": "Runs DFS with increasing depth limits (0, 1, 2, ...). Finds shortest path by depth with small memory footprint.",
        "pseudocode": [
            "for depth in [0..max_depth]:",
            "    if DLS(start, depth) succeeds: return path",
            "function DLS(u, limit):",
            "    if u == end: return success",
            "    if limit == 0: return cutoff",
            "    for v in neighbors(u):",
            "        if DLS(v, limit-1) succeeds: return success",
            "    return failure/cutoff"
        ],
        "time": "O(b^d) (like BFS overall, with repetition)",
        "space": "O(bd)"
    },
    "IDA*": {
        "title": "Iterative Deepening A* (IDA*)",
        "desc": "Performs DFS-style searches bounded by increasing f = g + h thresholds. A*’s heuristic guidance with DFS memory usage.",
        "pseudocode": [
            "bound = h(start); path = [start]",
            "while True:",
            "    t = search(path, g=0, bound)",
            "    if t == FOUND: return path",
            "    if t == ∞: return failure",
            "    bound = t",
            "function search(path, g, bound):",
            "    u = last(path); f = g + h(u)",
            "    if f > bound: return f",
            "    if u == end: return FOUND",
            "    min = ∞",
            "    for v in neighbors(u):",
            "        path.push(v)",
            "        t = search(path, g+1, bound)",
            "        if t == FOUND: return FOUND",
            "        if t < min: min = t",
            "        path.pop()",
            "    return min"
        ],
        "time": "Depends on heuristic; often between DFS and A*",
        "space": "O(bd)"
    }
}

class Slider:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.handle_x = x + w // 2  
        self.dragging = False

    def draw(self, win):
        # Track
        pygame.draw.rect(win, COLORS['BTN'], self.rect, border_radius=3)
        # Handle
        pygame.draw.circle(win, COLORS['BTN_HOVER'], (self.handle_x, self.rect.centery), HANDLE_R)
        # Label
        label = FONT.render("Speed", True, COLORS['TEXT'])
        win.blit(label, (self.rect.x - 70, self.rect.centery - 10))

    def handle_event(self, event):
        global SPEED
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.handle_x) <= HANDLE_R and abs(event.pos[1] - self.rect.centery) <= HANDLE_R:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            x = event.pos[0]
            self.handle_x = max(self.rect.x, min(x, self.rect.x + self.rect.w))
            pos = (self.handle_x - self.rect.x) / self.rect.w
            SPEED = int(120 - pos * 90)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, win, hover=False):
        color = COLORS['BTN_HOVER'] if hover else COLORS['BTN']
        pygame.draw.rect(win, color, self.rect, border_radius=10)
        label = FONT.render(self.text, True, COLORS['TEXT'])
        win.blit(label, (self.rect.x + 12, self.rect.y + 10))

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)


def wrap_text(text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_info_popup_blocking(selected_algo_key):
    """
    Draws a centered, resizable modal popup with info about the selected algorithm.
    Freezes the app until closed.
    """
    if not selected_algo_key or selected_algo_key not in ALGO_INFO:
        title = "Info"
        desc = "Please select an algorithm first."
        pseudocode = []
        time_c = "-"
        space_c = "-"
    else:
        d = ALGO_INFO[selected_algo_key]
        title = d["title"]
        desc = d["desc"]
        pseudocode = d["pseudocode"]
        time_c = d["time"]
        space_c = d["space"]

    max_w = int(WIDTH * 0.75)
    inner_w = max_w - 40
    line_gap = 6
    y_gap = 12

    desc_lines = wrap_text(desc, FONT, inner_w)

    title_h = TITLE_FONT.get_height()
    desc_h = len(desc_lines) * (FONT.get_height() + line_gap)
    pseudo_h = len(pseudocode) * (CODE_FONT.get_height() + 2)
    footer_h = FONT.get_height() * 2 + 10  # time/space
    button_h = 40
    padding = 20

    total_h = (
        padding + title_h + y_gap + desc_h + y_gap +
        FONT.get_height() + 4 + pseudo_h + y_gap +
        footer_h + y_gap + button_h + padding
    )
    max_h = int(HEIGHT * 0.8)
    popup_h = min(total_h, max_h)
    popup_w = max_w

    x = (WIDTH - popup_w) // 2
    y = (HEIGHT - popup_h) // 2
    popup_rect = pygame.Rect(x, y, popup_w, popup_h)

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    WIN.blit(overlay, (0, 0))

    pygame.draw.rect(WIN, COLORS['DD_BG'], popup_rect, border_radius=12)
    title_bar = pygame.Rect(x, y, popup_w, 44)
    pygame.draw.rect(WIN, COLORS['UI_BAR'], title_bar, border_radius=12)

    # Title
    title_surf = TITLE_FONT.render(title, True, COLORS['TEXT'])
    WIN.blit(title_surf, (x + 16, y + 10))

    yy = y + 54

    for line in desc_lines:
        line_surf = FONT.render(line, True, COLORS['TEXT'])
        WIN.blit(line_surf, (x + 20, yy))
        yy += FONT.get_height() + line_gap

    yy += y_gap

    # Pseudocode header
    pc_header = FONT.render("Pseudocode:", True, COLORS['TEXT'])
    WIN.blit(pc_header, (x + 20, yy))
    yy += FONT.get_height() + 4

    # Pseudocode box
    code_bg = pygame.Rect(
        x + 16, yy - 4, inner_w + 8,
        min(pseudo_h + 8, popup_h - (yy - y) - 120)
    )
    pygame.draw.rect(WIN, COLORS['WHITE'], code_bg, border_radius=8)

    # Pseudocode lines — white in Dark mode, black otherwise
    dark_mode = (COLORS['WHITE'] == (30, 30, 30))  
    code_color = (255, 255, 255) if dark_mode else (0, 0, 0)

    code_yy = yy
    for line in pseudocode:
        line_surf = CODE_FONT.render(line, True, code_color)
        WIN.blit(line_surf, (x + 24, code_yy))
        code_yy += CODE_FONT.get_height() + 2

    yy = code_yy + y_gap

    # Complexity
    time_surf = FONT.render(f"Time:  {time_c}", True, COLORS['TEXT'])
    space_surf = FONT.render(f"Space: {space_c}", True, COLORS['TEXT'])
    WIN.blit(time_surf, (x + 20, yy))
    WIN.blit(space_surf, (x + 20, yy + FONT.get_height() + 4))
    yy += footer_h

    # Bottom Close button 
    btn_w = 120
    btn_h = 36
    btn_x = x + (popup_w - btn_w) // 2
    btn_y = y + popup_h - btn_h - padding
    bottom_close_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
    pygame.draw.rect(WIN, COLORS['BTN'], bottom_close_rect, border_radius=8)
    bcl = FONT.render("Close", True, COLORS['TEXT'])
    WIN.blit(bcl, (bottom_close_rect.x + (btn_w - bcl.get_width()) // 2, bottom_close_rect.y + 6))

    pygame.display.flip()

    # Modal loop (freeze background)
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                waiting = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if close_rect.collidepoint(e.pos) or bottom_close_rect.collidepoint(e.pos):
                    waiting = False

        pygame.time.delay(16)


def draw_ui(win, buttons, selected_algo, show_algo_dropdown, algorithms, show_theme_dropdown, themes, slider):
    pygame.draw.rect(win, COLORS['UI_BAR'], (0, 0, WIDTH, UI_BAR_H))

    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        btn.draw(win, btn.is_hovered(mouse_pos))

    label_text = f"Selected: {selected_algo}" if selected_algo else "Selected: (none)"
    text = FONT.render(label_text, True, COLORS['TEXT'])
    label_text = f"Selected: {selected_algo}" if selected_algo else "Selected: (none)"
    text = FONT.render(label_text, True, COLORS['TEXT'])
    win.blit(text, (500, 20))

    if show_algo_dropdown:
        for i, algo in enumerate(algorithms):
            rect = pygame.Rect(10, UI_BAR_H + 5 + i * 32, 150, 28)
            pygame.draw.rect(win, COLORS['DD_BG'], rect, border_radius=6)
            label = FONT.render(algo, True, COLORS['TEXT'])
            win.blit(label, (rect.x + 6, rect.y + 5))

    if show_theme_dropdown:
        for i, theme_name in enumerate(themes):
            rect = pygame.Rect(390, UI_BAR_H + 5 + i * 32, 150, 28)
            pygame.draw.rect(win, COLORS['DD_BG'], rect, border_radius=6)
            label = FONT.render(theme_name, True, COLORS['TEXT'])
            win.blit(label, (rect.x + 6, rect.y + 5))

    slider.draw(win)


if __name__ == "__main__":
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer — Themes + Speed + Info")

    ROWS, COLS = 50, 50
    grid = Grid(WIN, ROWS, COLS, WIDTH, HEIGHT)

    start = None
    end = None
    run = True
    started = False

    buttons = [
        Button(10, 10, 150, 40, "Algorithm ▼"),
        Button(170, 10, 100, 40, "Play"),
        Button(280, 10, 100, 40, "Reset"),
        Button(390, 10, 150, 40, "Theme ▼"),
        Button(WIDTH - 110, 10, 100, 40, "Info"),
    ]
    algorithms = ["BFS", "DFS", "A*", "UCS", "Greedy", "IDDFS", "IDA*"]
    themes = get_theme_names()

    selected_algo = None
    show_algo_dropdown = False
    show_theme_dropdown = False

    slider = Slider(SLIDER_X, SLIDER_Y, SLIDER_W, SLIDER_H)

    while run:
        grid.draw()
        draw_ui(WIN, buttons, selected_algo, show_algo_dropdown, algorithms, show_theme_dropdown, themes, slider)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            slider.handle_event(event)

            if started:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if y <= UI_BAR_H:
                    if buttons[0].is_hovered(event.pos):
                        show_algo_dropdown = not show_algo_dropdown
                        show_theme_dropdown = False
                        continue

                    if buttons[1].is_hovered(event.pos):
                        if selected_algo and start and end:
                            for row in grid.grid:
                                for spot in row:
                                    spot.update_neighbors(grid.grid)
                            started = True

                            func = {
                                "BFS": bfs,
                                "DFS": dfs,
                                "A*": astar,
                                "UCS": ucs,
                                "Greedy": greedy,
                                "IDDFS": iddfs,
                                "IDA*": ida_star
                            }.get(selected_algo)

                            func(lambda: (grid.draw(),
                                          draw_ui(WIN, buttons, selected_algo, show_algo_dropdown, algorithms, show_theme_dropdown, themes, slider),
                                          pygame.display.flip(),
                                          pygame.time.delay(get_delay())),
                                 grid, start, end)
                            started = False
                        continue

                    if buttons[2].is_hovered(event.pos):
                        start = None
                        end = None
                        grid.reset()
                        continue

                    if buttons[3].is_hovered(event.pos):
                        show_theme_dropdown = not show_theme_dropdown
                        show_algo_dropdown = False
                        continue

                    if buttons[4].is_hovered(event.pos):
                        draw_info_popup_blocking(selected_algo)
                        continue

                if show_algo_dropdown:
                    clicked_dropdown = False
                    for i, algo in enumerate(algorithms):
                        rect = pygame.Rect(10, UI_BAR_H + 5 + i * 32, 150, 28)
                        if rect.collidepoint(event.pos):
                            selected_algo = algo
                            show_algo_dropdown = False
                            clicked_dropdown = True
                            break
                    if clicked_dropdown:
                        continue

                if show_theme_dropdown:
                    clicked_theme = False
                    for i, theme_name in enumerate(themes):
                        rect = pygame.Rect(390, UI_BAR_H + 5 + i * 32, 150, 28)
                        if rect.collidepoint(event.pos):
                            set_theme(theme_name)
                            show_theme_dropdown = False
                            clicked_theme = True
                            break
                    if clicked_theme:
                        continue

                if y > UI_BAR_H:
                    row, col = grid.get_clicked_pos((x, y))
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        spot = grid.grid[row][col]
                        if event.button == 1:
                            if not start and spot != end:
                                start = spot
                                start.make_start()
                            elif not end and spot != start:
                                end = spot
                                end.make_end()
                            elif spot != start and spot != end:
                                spot.make_barrier()
                        elif event.button == 3:
                            spot.reset()
                            if spot == start:
                                start = None
                            elif spot == end:
                                end = None

    pygame.quit()
