from contextlib import suppress
from enum import Enum, auto
from logging import basicConfig
from sqlite3 import Error as SQLiteError

import pygame

from config import (
    DB_PATH,
    FPS,
    GRID_HEIGHT,
    GRID_WIDTH,
    LOGGING_LEVEL,
    MAX_NICKNAME_LENGTH,
    SCOREBOARD_LIMIT,
    TICK_MS,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)
from db import ScoreRepository
from game import Direction, Game
from ui import Renderer


KEY_DIRECTIONS: dict[int, Direction] = {
    pygame.K_UP: Direction.UP,
    pygame.K_w: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_s: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_a: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
    pygame.K_d: Direction.RIGHT,
}

ENTER_KEYS: tuple[int, ...] = (pygame.K_RETURN, pygame.K_KP_ENTER)


class GameState(Enum):

    MENU = auto()
    GAME = auto()
    GAME_OVER = auto()
    SCOREBOARD = auto()


class App:

    def __init__(self, screen: pygame.Surface, repository: ScoreRepository) -> None:

        self._renderer = Renderer(screen)
        self._repository = repository
        self._clock = pygame.time.Clock()
        self._is_running = True
        self._state = GameState.MENU

        self._nickname_input = ''
        self._menu_error = ''
        self._nickname = ''

        self._game = Game(GRID_WIDTH, GRID_HEIGHT)
        self._tick_elapsed = 0
        self._scoreboard: list[tuple[str, int]] = []

    def _handle_event(self, event: pygame.event.Event) -> None:

        if event.type == pygame.QUIT:
            self._is_running = False
            return

        if event.type != pygame.KEYDOWN:
            return

        if self._state is GameState.MENU:
            self._handle_menu_key(event)

        elif self._state is GameState.GAME:

            direction = KEY_DIRECTIONS.get(event.key)

            if direction is not None:
                self._game.change_direction(direction)

        elif self._state is GameState.GAME_OVER:

            if event.key in ENTER_KEYS:
                self._state = GameState.MENU

            elif event.key == pygame.K_s:
                self._open_scoreboard()

            elif event.key == pygame.K_q:
                self._is_running = False

        elif self._state is GameState.SCOREBOARD and event.key == pygame.K_ESCAPE:
            self._state = GameState.MENU

    def _handle_menu_key(self, event: pygame.event.Event) -> None:

        if event.key in ENTER_KEYS:

            nickname = self._nickname_input.strip()

            if not nickname:
                self._menu_error = 'Имя не может быть пустым'
                return

            self._start_game(nickname)

        elif event.key == pygame.K_BACKSPACE:
            self._nickname_input = self._nickname_input[:-1]

        elif event.unicode.isprintable() and event.unicode:

            if len(self._nickname_input) < MAX_NICKNAME_LENGTH:
                self._nickname_input += event.unicode

            self._menu_error = ''

    def _start_game(self, nickname: str) -> None:

        self._nickname = nickname
        self._nickname_input = nickname
        self._menu_error = ''
        self._game = Game(GRID_WIDTH, GRID_HEIGHT)
        self._tick_elapsed = 0
        self._state = GameState.GAME

    def _finish_game(self) -> None:

        with suppress(SQLiteError):
            self._repository.save_result(self._nickname, self._game.score)

        self._state = GameState.GAME_OVER

    def _open_scoreboard(self) -> None:

        try:
            self._scoreboard = self._repository.get_top_players(SCOREBOARD_LIMIT)

        except SQLiteError:
            self._scoreboard = []

        self._state = GameState.SCOREBOARD

    def _update(self, elapsed: int) -> None:

        if self._state is not GameState.GAME:
            return

        self._tick_elapsed += elapsed

        if self._tick_elapsed >= TICK_MS:

            self._tick_elapsed -= TICK_MS
            self._game.step()

            if self._game.is_over:
                self._finish_game()

    def _draw(self) -> None:

        if self._state is GameState.MENU:
            self._renderer.draw_menu(self._nickname_input, self._menu_error)

        elif self._state is GameState.GAME:
            self._renderer.draw_game(self._game, self._nickname)

        elif self._state is GameState.GAME_OVER:
            self._renderer.draw_game_over(self._game.score, is_won=self._game.is_won)

        else:
            self._renderer.draw_scoreboard(self._scoreboard)

    def run(self) -> None:
        while self._is_running:

            elapsed = self._clock.tick(FPS)

            for event in pygame.event.get():
                self._handle_event(event)

            self._update(elapsed)
            self._draw()

            pygame.display.flip()


def main() -> None:
    """
    Run the Snake game.
    """

    basicConfig(level=LOGGING_LEVEL, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    pygame.init()

    pygame.display.set_caption(WINDOW_TITLE)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    repository = ScoreRepository(DB_PATH)

    try:
        App(screen, repository).run()

    finally:

        repository.close()
        pygame.quit()


if __name__ == '__main__':
    main()
