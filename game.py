import sys

import pygame

from Direction import Direction
from apple import Apple
from config import GRID_HEIGHT, GRID_WIDTH, GREEN_LIGHT, GREEN_DARK, TILE_SIZE, WHITE, RED, SCREEN_WIDTH, \
    SCREEN_HEIGHT, FPS
from snake import Snake
from uiUtilities import draw_text


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        # load assets
        self.head_img = pygame.image.load("assets/snakehead.png").convert_alpha()
        self.trophy_img = pygame.image.load("assets/trophy.png").convert_alpha()
        self.trophy_img = pygame.transform.scale(self.trophy_img, (30, 30))
        self.apple_counter_img = pygame.image.load("assets/apple.png").convert_alpha()
        self.apple_counter_img = pygame.transform.scale(self.apple_counter_img, (30, 30))
        self.arrow_img = pygame.image.load("assets/thinarrow.png").convert_alpha()
        arrow_size = int(TILE_SIZE * 0.8)
        self.arrow_img = pygame.transform.scale(self.arrow_img, (arrow_size, arrow_size))
        apple_img = pygame.image.load("assets/apple.png").convert_alpha()
        apple_size = int(TILE_SIZE * 0.9)
        self.apple_img = pygame.transform.scale(apple_img, (apple_size, apple_size))

        self.start_body = [(7, 5), (6, 5), (5, 5)]
        self.snake = Snake(self.start_body.copy(), Direction.RIGHT, self.head_img)
        self.apple = Apple(self.snake, self.apple_img, self.arrow_img)
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.move_delay_milli = 150
        self.last_move_time = pygame.time.get_ticks()

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = GREEN_LIGHT if (x + y) % 2 == 0 else GREEN_DARK
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if not self.game_over:
                    if event.key == pygame.K_UP:
                        self.snake.set_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.set_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.set_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.set_direction(Direction.RIGHT)
                else:
                    self.reset()

    def reset(self):
        self.score = 0
        self.game_over = False
        self.snake = Snake(self.start_body.copy(), Direction.RIGHT, self.head_img)
        self.apple.move(self.snake)

    def update(self):
        if self.game_over:
            return

        current_time = pygame.time.get_ticks()

        if current_time - self.last_move_time < self.move_delay_milli:
            return

        self.last_move_time = current_time
        head_x, head_y = self.snake.body[0]
        direction_x, direction_y = self.snake.direction.vector
        next_head = (head_x + direction_x, head_y + direction_y)

        if self.snake.check_collision(next_head):
            self.game_over = True
            return

        self.snake.move()

        if self.snake.body[0] == self.apple.position:
            if self.snake.direction == self.apple.bonus_direction:
                self.score += 2
            else:
                self.score += 1

            self.high_score = max(self.score, self.high_score)
            self.snake.grow()
            self.apple.move(self.snake)

    def draw_score(self):
        self.screen.blit(self.trophy_img, (10, 10))
        draw_text(str(self.high_score), True, WHITE, (50,15), 24, self.screen)

        self.screen.blit(self.apple_counter_img, (10, 45))
        draw_text(str(self.score), True, WHITE, (50, 50), 24, self.screen)

    def draw_game_over(self):
        draw_text("Game Over", True, RED, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20), 48, self.screen)
        draw_text("Press any key to restart",
                  True, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20), 24, self.screen)

    def run(self):
        while True:
            self.handle_input()
            self.update()

            self.draw_grid()
            self.apple.draw(self.screen)
            self.snake.draw(self.screen)
            self.draw_score()

            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(FPS)
