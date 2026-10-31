import random
from enum import Enum
from typing import TypeAlias

from config import POINTS_PER_FOOD, WIN_SCORE


Cell: TypeAlias = tuple[int, int]


class Direction(Enum):

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def is_opposite(self, other: 'Direction') -> bool:
        """
        Return ``True`` if the two directions point 180 degrees apart.
        """

        return self.value[0] == -other.value[0] and self.value[1] == -other.value[1]


class Game:

    def _spawn_food_cell(self) -> Cell | None:
        """
        Pick a random cell not used by the snake; end the game if none is left.
        """

        used = set(self.snake)

        free_cells = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if (x, y) not in used
        ]

        if not free_cells:

            self.is_won = True
            self.is_over = True

            return None

        return self._random_generator.choice(free_cells)

    def __init__(self, width: int, height: int) -> None:

        self.width = width
        self.height = height

        self._random_generator = random.Random()  # noqa: S311  # not used for cryptography

        center_x, center_y = width // 2, height // 2

        self.snake: list[Cell] = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]

        self.direction = Direction.RIGHT
        self._next_direction = Direction.RIGHT

        self.score = 0
        self.is_won = False
        self.is_over = False
        self.food_cell = self._spawn_food_cell()

    def change_direction(self, direction: Direction) -> None:
        """
        Queue a direction change for the next step, ignoring 180-degree reversals.
        """

        if not direction.is_opposite(self.direction):
            self._next_direction = direction

    def step(self) -> None:
        """
        Move the snake by one cell and resolve food and collisions.
        """

        if self.is_over:
            return

        self.direction = self._next_direction

        head_x, head_y = self.snake[0]
        delta_x, delta_y = self.direction.value

        new_head = (head_x + delta_x, head_y + delta_y)

        if not (0 <= new_head[0] < self.width and 0 <= new_head[1] < self.height):
            self.is_over = True
            return

        is_grows = new_head == self.food_cell

        body = self.snake if is_grows else self.snake[:-1]

        if new_head in body:
            self.is_over = True
            return

        self.snake.insert(0, new_head)

        if is_grows:

            self.score += POINTS_PER_FOOD

            if self.score >= WIN_SCORE:

                self.is_won = True
                self.is_over = True

                return

            self.food_cell = self._spawn_food_cell()

        else:
            self.snake.pop()
