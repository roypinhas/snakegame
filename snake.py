import pygame

from Direction import Direction
from config import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, SNAKE_HEAD_WIDTH_SCALE, SNAKE_HEAD_HEIGHT_SCALE, BLUE, \
    SNAKE_BODY_WIDTH_SCALE, SNAKE_BODY_HEIGHT_SCALE
from directionUtilities import get_dir, vector_to_direction
from uiUtilities import draw_rounded_rect


class Snake:
    def __init__(self, body, direction, head_img):
        self.body = body
        self.direction = direction
        self.grow_next_move = False
        self.head_img = head_img

    def move(self):
        head_x, head_y = self.body[0]
        direction_x, direction_y = self.direction.vector
        new_head = (head_x + direction_x, head_y + direction_y)
        self.body.insert(0, new_head)

        if self.grow_next_move:
            self.grow_next_move = False
        else:
            self.body.pop()

    def grow(self):
        self.grow_next_move = True

    def set_direction(self, direction):
        # we can't allow the snake to go in a reversed direction
        if tuple(-x for x in direction.vector) != self.direction.vector:
            self.direction = direction

    def check_collision(self, next_head=None):
        head = next_head if next_head is not None else self.body[0]
        return (
                head in self.body[1:] or
                not (0 <= head[0] < GRID_WIDTH) or
                not (0 <= head[1] < GRID_HEIGHT)
        )

    def draw(self, screen):

        body_width = int(TILE_SIZE * SNAKE_BODY_WIDTH_SCALE)
        body_height = int(TILE_SIZE * SNAKE_BODY_HEIGHT_SCALE)

        for i, pos in enumerate(self.body):
            x, y = pos
            default_body_rect = pygame.Rect(
                x * TILE_SIZE + (TILE_SIZE - body_width) // 2,
                y * TILE_SIZE + (TILE_SIZE - body_height) // 2,
                body_width,
                body_height
            )

            if i == 0:
                self._draw_head(screen, pos, default_body_rect)
            elif i == len(self.body) - 1:
                self._draw_tail(screen, pos, i, body_width, body_height, default_body_rect)
            else:
                self._draw_body(screen, pos, i, default_body_rect)

    def _draw_head(self, screen, pos, rect):
        head_width = int(TILE_SIZE * SNAKE_HEAD_WIDTH_SCALE)
        head_height = int(TILE_SIZE * SNAKE_HEAD_HEIGHT_SCALE)

        angle = self.direction.rotation

        scaled_head = pygame.transform.scale(self.head_img, (head_width, head_height))
        rotated_head = pygame.transform.rotate(scaled_head, angle)
        head_rect = rotated_head.get_rect(center=rect.center)
        screen.blit(rotated_head, head_rect)

        if len(self.body) > 1:
            next_pos = self.body[1]
            self._draw_connection(screen, pos, next_pos)

    def _draw_tail(self, screen, pos, i, body_width, body_height, rect):
        radius = min(body_width, body_height) // 2 - 2

        prev = self.body[i - 1]
        dir_to_prev_vec = get_dir(pos, prev)
        dir_to_prev = vector_to_direction(dir_to_prev_vec)

        top_left = dir_to_prev in (Direction.DOWN, Direction.RIGHT)
        top_right = dir_to_prev in (Direction.DOWN, Direction.LEFT)
        bottom_right = dir_to_prev in (Direction.UP, Direction.LEFT)
        bottom_left = dir_to_prev in (Direction.UP, Direction.RIGHT)

        draw_rounded_rect(screen, BLUE, rect, radius,
                          (top_left, top_right, bottom_right, bottom_left))

    def _draw_body(self, screen, pos, i, rect):
        draw_rounded_rect(screen, BLUE, rect, 0, (0, 0, 0, 0))

        next_pos = self.body[i + 1]
        self._draw_connection(screen, pos, next_pos)

    def _draw_connection(self, screen, segment_a, segment_b):
        x_a, y_a = segment_a
        x_b, y_b = segment_b

        body_width = int(TILE_SIZE * SNAKE_BODY_WIDTH_SCALE)
        body_height = int(TILE_SIZE * SNAKE_BODY_HEIGHT_SCALE)

        if x_a != x_b:
            left_x = min(x_a, x_b) * TILE_SIZE + (TILE_SIZE + body_width) // 2
            top_y = y_a * TILE_SIZE + (TILE_SIZE - body_height) // 2
            width = TILE_SIZE - body_width
            height = body_height

        elif y_a != y_b:
            left_x = x_a * TILE_SIZE + (TILE_SIZE - body_width) // 2
            top_y = min(y_a, y_b) * TILE_SIZE + (TILE_SIZE + body_height) // 2
            width = body_width
            height = TILE_SIZE - body_height

        else:
            return

        connector_rect = pygame.Rect(left_x, top_y, width, height)
        pygame.draw.rect(screen, BLUE, connector_rect)

