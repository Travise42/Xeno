import pygame

import program.constants as constants

def draw_separator(length: int) -> pygame.Surface:
    surf = pygame.Surface((25, length), pygame.SRCALPHA)
    for i in range(2, 33):
        pygame.draw.line(surf, constants.PALETTE_HIGHLIGHT + (i**2 // 4 - 1,), (12, (i/100.0)*length), (12, (1-i/100.0)*length), 3)
    pygame.draw.polygon(surf, constants.PALETTE_HIGHLIGHT + (255,), [(12, length//2 - 16), (4, length//2), (12, length//2 + 16), (20, length//2)])
    return surf

def draw_label(width: int, height: int, text, font: pygame.font.Font, color: tuple[int, int, int] = constants.PALETTE_HIGHLIGHT) -> pygame.Surface:
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surf, constants.PALETTE_SHADOW, (4, 4, width-8, height-8), 0, 12)
    pygame.draw.rect(surf, color, (4, 4, width-8, height-8), 3, 12)
    text_surf = font.render(text, 1, color)
    surf.blit(text_surf, (width // 2 - text_surf.get_width() // 2, height // 2 - text_surf.get_height() // 2))
    return surf

def draw_label_on(surf: pygame.Surface, width: int, height: int, text, font: pygame.font.Font, color=constants.PALETTE_HIGHLIGHT):
    pygame.draw.rect(surf, constants.PALETTE_SHADOW, (4, 4, width-8, height-8), 0, 12)
    pygame.draw.rect(surf, color, (4, 4, width-8, height-8), 3, 12)
    text_surf = font.render(text, 1, color)
    surf.blit(text_surf, (width // 2 - text_surf.get_width() // 2, height // 2 - text_surf.get_height() // 2))

def hovering_label(mouse_pos: tuple[int, int], rect: tuple[int, int, int, int]):
    return 0 < mouse_pos[0] - rect[0] < rect[2] and 0 < mouse_pos[1] - rect[1] < rect[3]