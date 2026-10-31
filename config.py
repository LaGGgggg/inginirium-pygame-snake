from logging import DEBUG
from pathlib import Path
from typing import TypeAlias


Color: TypeAlias = tuple[int, int, int]

WINDOW_TITLE: str = 'Змейка'

GRID_WIDTH: int = 20
GRID_HEIGHT: int = 20
CELL_SIZE: int = 25
HUD_HEIGHT: int = 30

WINDOW_WIDTH: int = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT: int = GRID_HEIGHT * CELL_SIZE + HUD_HEIGHT

TICK_MS: int = 150
FPS: int = 60

POINTS_PER_FOOD: int = 10
WIN_SCORE: int = 200
MAX_NICKNAME_LENGTH: int = 16
SCOREBOARD_LIMIT: int = 5

DB_PATH: Path = Path(__file__).resolve().parent / 'snake.db'

FONT_SIZE_LARGE: int = 56
FONT_SIZE_MEDIUM: int = 32
FONT_SIZE_SMALL: int = 24

COLOR_BACKGROUND: Color = (20, 20, 20)
COLOR_HUD: Color = (40, 40, 40)
COLOR_SNAKE_HEAD: Color = (120, 220, 120)
COLOR_SNAKE_BODY: Color = (60, 170, 60)
COLOR_FOOD: Color = (220, 60, 60)
COLOR_TEXT: Color = (235, 235, 235)
COLOR_TEXT_DIM: Color = (150, 150, 150)
COLOR_ERROR: Color = (230, 90, 90)
COLOR_SUCCESS: Color = (120, 220, 120)
COLOR_INPUT_BOX: Color = (60, 60, 60)

IS_USE_ANTIALIAS: bool = True

# use values from logging module
LOGGING_LEVEL: int = DEBUG
