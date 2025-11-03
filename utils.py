import pygame

# Window size
WIDTH = 800
HEIGHT = 800

THEMES = {
    "Pastel": {
        'WHITE': (255, 228, 235),      # grid background
        'BLACK': (200, 200, 200),      # barrier
        'ORANGE': (144, 238, 144),     # start
        'YELLOW': (255, 105, 97),      # end
        'PURPLE': (255, 20, 147),      # path
        'GREEN': (204, 255, 229),      # open node
        'RED': (255, 192, 203),        # closed node
        'GREY': (216, 191, 216),       # grid lines
        'BTN': (187, 160, 199),
        'BTN_HOVER': (167, 140, 179),
        'TEXT': (50, 0, 50),
        'UI_BAR': (245, 225, 235),
        'DD_BG': (255, 210, 230), 
        'SLIDER_BG': (187, 160, 199),
        'SLIDER_FG': (50, 0, 50)
    },

    "Ocean": {
        'WHITE': (225, 245, 255),       # grid background
        'BLACK': (200, 255, 255),       # walls = light turquoise
        'ORANGE': (0, 200, 120),        # start = green
        'YELLOW': (255, 80, 80),        # end = red
        'PURPLE': (0, 50, 120),         # path = dark blue
        'GREEN': (160, 235, 210),       
        'RED': (255, 140, 140),
        'GREY': (180, 210, 220),
        'BTN': (150, 200, 220),
        'BTN_HOVER': (130, 180, 200),
        'TEXT': (0, 50, 80),
        'UI_BAR': (200, 230, 245),
        'DD_BG': (180, 210, 230), 
        'SLIDER_BG': (150, 200, 220),
        'SLIDER_FG': (0, 50, 80)
    },

    "Dark": {
        'WHITE': (30, 30, 30),          # grid background
        'BLACK': (120, 120, 120),       # walls = light gray
        'ORANGE': (0, 200, 0),          # start = green
        'YELLOW': (220, 40, 40),        # end = red
        'PURPLE': (0, 150, 255),        # path = bright blue
        'GREEN': (90, 200, 90),
        'RED': (200, 80, 80),
        'GREY': (90, 90, 90),
        'BTN': (60, 60, 60),
        'BTN_HOVER': (90, 90, 90),
        'TEXT': (220, 220, 220),
        'TEXT1' : (0, 0, 0),
        'UI_BAR': (50, 50, 50),
        'DD_BG': (70, 70, 70), 
        'SLIDER_BG': (60, 60, 60),
        'SLIDER_FG': (220, 220, 220)

    },

    "Christmas": {
        'WHITE': (0, 100, 0),           # grid = dark green
        'BLACK': (255, 255, 255),       # walls = white
        'ORANGE': (50, 205, 50),        # start = bright green
        'YELLOW': (200, 0, 0),          # end = red
        'PURPLE': (255, 215, 0),        # solution path = gold
        'GREEN': (160, 235, 160),
        'RED': (255, 110, 110),
        'GREY': (200, 200, 200),
        'BTN': (200, 0, 0),             # button red
        'BTN_HOVER': (160, 0, 0),       
        'TEXT': (255, 255, 255),
        'UI_BAR': (150, 0, 0),
        'DD_BG': (255, 255, 255), 
        'SLIDER_BG': (200, 0, 0),
        'SLIDER_FG': (255, 255, 255)
    }
}

COLORS = dict(THEMES["Pastel"])

def set_theme(name: str):
    """Switches the global COLORS palette in-place so all modules see the change."""
    theme = THEMES.get(name, THEMES["Pastel"])
    COLORS.clear()
    COLORS.update(theme)

def get_theme_names():
    return list(THEMES.keys())
