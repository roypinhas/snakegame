import pygame

from config import FONT_NAME


def draw_text(text, is_bold, color, position, size, screen):
    font = pygame.font.SysFont(FONT_NAME, size, bold=is_bold)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=position)
    screen.blit(text_surf, text_rect)
