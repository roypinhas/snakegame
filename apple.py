import random
from abc import ABC
import pygame
from Direction import Direction
from MapObject import MapObject
from config import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE


class Apple(MapObject, ABC):
    def __init__(self, snake, apple_img, arrow_img):
        self.position = (0, 0)
        self.bonus_direction = random.choice(list(Direction))
        self.move(snake)
        self.apple_img = apple_img
        self.arrow_img = arrow_img

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
        x, y = self.position
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        apple_rect = self.apple_img.get_rect(center=rect.center)
        screen.blit(self.apple_img, apple_rect)

        # Adjust this if your arrow points right by default
        rotation = (self.bonus_direction.rotation - 90) % 360

        rotated_arrow = pygame.transform.rotate(self.arrow_img, rotation)
        arrow_rect = rotated_arrow.get_rect()

        dx, dy = self.bonus_direction.vector
        arrow_rect.center = (
            rect.centerx + dx * (rect.width // 2 + arrow_rect.width // 2),
            rect.centery + dy * (rect.height // 2 + arrow_rect.height // 2)
        )

        screen.blit(rotated_arrow, arrow_rect)
