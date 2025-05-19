import pygame
from config import FONT_NAME


def draw_text(text, is_bold, color, position, size, screen):
    font = pygame.font.SysFont(FONT_NAME, size, bold=is_bold)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=position)
    screen.blit(text_surf, text_rect)


def draw_rounded_rect(surface, color, rect, radius, corners):
    shape_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    pygame.draw.rect(shape_surf, color, (0, radius, rect.width, rect.height - 2 * radius))
    pygame.draw.rect(shape_surf, color, (radius, 0, rect.width - 2 * radius, rect.height))

    circle_centers = [
        (radius, radius),
        (rect.width - radius, radius),
        (rect.width - radius, rect.height - radius),
        (radius, rect.height - radius),
    ]

    rect_areas = [
        (0, 0, radius, radius),
        (rect.width - radius, 0, radius, radius),
        (rect.width - radius, rect.height - radius, radius, radius),
        (0, rect.height - radius, radius, radius),
    ]

    for corner_flag, center, area in zip(corners, circle_centers, rect_areas):
        if corner_flag:
            pygame.draw.circle(shape_surf, color, center, radius)
        else:
            pygame.draw.rect(shape_surf, color, area)

    surface.blit(shape_surf, rect.topleft)
