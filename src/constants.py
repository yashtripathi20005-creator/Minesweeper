"""
Game constants and configuration.
"""
# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BOARD_PADDING = 20
STATUS_BAR_HEIGHT = 60

# Board settings (Easy difficulty by default)
ROWS = 10
COLS = 10
NUM_MINES = 15

# Colors
COLOR_BG = (200, 200, 200)
COLOR_BOARD_BG = (180, 180, 180)
COLOR_CELL_HIDDEN = (120, 120, 120)
COLOR_CELL_HIDDEN_HOVER = (140, 140, 140)
COLOR_CELL_REVEALED = (220, 220, 220)
COLOR_CELL_BORDER = (160, 160, 160)
COLOR_TEXT = (0, 0, 0)
COLOR_MINE = (255, 0, 0)
COLOR_FLAG = (255, 50, 50)
COLOR_WRONG_FLAG = (255, 200, 200)
COLOR_STATUS_BG = (50, 50, 50)
COLOR_STATUS_TEXT = (255, 255, 255)
COLOR_WIN = (0, 200, 0)
COLOR_LOSE = (200, 0, 0)

# Number colors (1-8)
NUMBER_COLORS = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128),
}

# Font settings
FONT_NAME = "Arial"
FONT_SIZE_LARGE = 28
FONT_SIZE_MEDIUM = 20
FONT_SIZE_SMALL = 14

# Difficulty presets
DIFFICULTIES = {
    "Easy": {"rows": 10, "cols": 10, "mines": 15},
    "Medium": {"rows": 16, "cols": 16, "mines": 40},
    "Hard": {"rows": 20, "cols": 20, "mines": 80},
}
