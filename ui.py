from typing import Any

import pygame

from config import (
    CELL_SIZE,
    COLOR_BACKGROUND,
    COLOR_ERROR,
    COLOR_FOOD,
    COLOR_HUD,
    COLOR_INPUT_BOX,
    COLOR_SNAKE_BODY,
    COLOR_SNAKE_HEAD,
    COLOR_SUCCESS,
    COLOR_TEXT,
    COLOR_TEXT_DIM,
    FONT_SIZE_LARGE,
    FONT_SIZE_MEDIUM,
    FONT_SIZE_SMALL,
    HUD_HEIGHT,
    IS_USE_ANTIALIAS,
    SCOREBOARD_LIMIT,
    WINDOW_WIDTH,
    Color,
)
from game import Cell, Game


class Renderer:

    def __init__(self, surface: pygame.Surface) -> None:

        self._surface = surface

        self._font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self._font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self._font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

    @staticmethod
    def _render(font: pygame.font.Font, text: str, color: Color) -> pygame.Surface:
        return font.render(text, IS_USE_ANTIALIAS, color)

    def _draw_cell(self, cell: Cell, color: Color) -> None:

        x, y = cell

        rect = pygame.Rect(x * CELL_SIZE, HUD_HEIGHT + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(self._surface, color, rect.inflate(-2, -2))

    def _draw_text(self, text: str, font: pygame.font.Font, color: Color, center_y: int) -> None:

        rendered_surface = self._render(font, text, color)

        self._surface.blit(rendered_surface, rendered_surface.get_rect(center=(WINDOW_WIDTH // 2, center_y)))

    def draw_menu(self, nickname: str, error_text: str) -> None:

        self._surface.fill(COLOR_BACKGROUND)

        self._draw_text('Змейка', self._font_large, COLOR_TEXT, 110)
        self._draw_text('Введите имя:', self._font_medium, COLOR_TEXT, 200)

        box = pygame.Rect(0, 0, 320, 44)

        box.center = (WINDOW_WIDTH // 2, 250)

        pygame.draw.rect(self._surface, COLOR_INPUT_BOX, box)

        self._draw_text(f'{nickname}_', self._font_medium, COLOR_TEXT, box.centery)

        if error_text:
            self._draw_text(error_text, self._font_small, COLOR_ERROR, 300)

        self._draw_text('Enter - начать', self._font_small, COLOR_TEXT_DIM, 380)

    def draw_game(self, game: Game, nickname: str) -> None:

        self._surface.fill(COLOR_BACKGROUND)

        pygame.draw.rect(self._surface, COLOR_HUD, pygame.Rect(0, 0, WINDOW_WIDTH, HUD_HEIGHT))

        player = self._render(self._font_small, f'Игрок: {nickname}', COLOR_TEXT)

        score = self._render(self._font_small, f'Счёт: {game.score}', COLOR_TEXT)

        self._surface.blit(player, player.get_rect(midleft=(10, HUD_HEIGHT // 2)))
        self._surface.blit(score, score.get_rect(midright=(WINDOW_WIDTH - 10, HUD_HEIGHT // 2)))

        if game.food_cell is not None:
            self._draw_cell(game.food_cell, COLOR_FOOD)

        for index, cell in enumerate(game.snake):
            self._draw_cell(cell, COLOR_SNAKE_HEAD if index == 0 else COLOR_SNAKE_BODY)

    def draw_game_over(self, score: int, *_: Any, is_won: bool) -> None:

        self._surface.fill(COLOR_BACKGROUND)

        if is_won:
            self._draw_text('ПОБЕДА', self._font_large, COLOR_SUCCESS, 120)

        else:
            self._draw_text('GAME OVER', self._font_large, COLOR_ERROR, 120)

        self._draw_text(f'Счёт: {score}', self._font_medium, COLOR_TEXT, 200)
        self._draw_text('Enter - меню', self._font_small, COLOR_TEXT_DIM, 340)
        self._draw_text('S - таблица лидеров', self._font_small, COLOR_TEXT_DIM, 370)
        self._draw_text('Q - выйти', self._font_small, COLOR_TEXT_DIM, 400)

    def draw_scoreboard(self, rows: list[tuple[str, int]]) -> None:

        self._surface.fill(COLOR_BACKGROUND)
        self._draw_text(f'TOP {SCOREBOARD_LIMIT}', self._font_large, COLOR_TEXT, 60)

        if not rows:
            self._draw_text('Пока нет результатов', self._font_medium, COLOR_TEXT_DIM, 200)

        for place, (nickname, best_score) in enumerate(rows, start=1):

            y = 100 + place * 30

            left = self._render(self._font_medium, f'{place:>2}. {nickname}', COLOR_TEXT)
            right = self._render(self._font_medium, str(best_score), COLOR_TEXT)

            self._surface.blit(left, left.get_rect(midleft=(80, y)))
            self._surface.blit(right, right.get_rect(midright=(WINDOW_WIDTH - 80, y)))

        self._draw_text('Escape - меню', self._font_small, COLOR_TEXT_DIM, 480)
