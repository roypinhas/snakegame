import random
from abc import ABC

from Direction import Direction
from MapObject import MapObject
from config import GRID_WIDTH, GRID_HEIGHT


class Apple(MapObject, ABC):
    def __init__(self, snake):
        self.position = (0, 0)
        self.bonus_direction = random.choice(list(Direction))
        self.move(snake)

    def move(self, snake=None):
        if snake is None:
            return

        available_positions = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in snake.body
        ]

        if available_positions:
            self.position = random.choice(available_positions)
            self.bonus_direction = random.choice(list(Direction))

    def draw(self, screen):
        pass
