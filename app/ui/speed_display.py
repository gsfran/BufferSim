from __future__ import annotations

import pygame
from pygame import Rect, draw
from pygame.font import Font
from pygame.surface import Surface

from app import buffer
from app.colors import BLACK, GREY
from app.config import SCREEN_HEIGHT, SCREEN_WIDTH

SPEED_DISPLAY_FONT: Font = pygame.font.SysFont("Helvetica", 30, bold=True)


class SpeedDisplay:
    """
    Display block showing the current simulation speed.
    """

    def __init__(self) -> None:
        self.bg_color = GREY
        self.outline_color = BLACK
        self.text_color = BLACK

        self.width = SCREEN_WIDTH * 0.15
        self.height = SCREEN_HEIGHT * 0.10

    def draw(self, window: Surface) -> None:

        self.x_pos = (SCREEN_WIDTH * 0.975) - self.width
        self.y_pos = (SCREEN_HEIGHT * 0.025)

        self.rect = Rect(self.x_pos, self.y_pos, self.width, self.height)

        draw.rect(window, self.bg_color, self.rect)

        corners = [
            self.rect.topleft, self.rect.topright,
            self.rect.bottomright, self.rect.bottomleft
        ]
        draw.lines(window, self.outline_color, True, corners)

        text = f'SPEED: {buffer.speed}'

        text_surface = SPEED_DISPLAY_FONT.render(
           text, True, self.text_color
        )
        txt_padding = (self.width * 0.125, self.height * 0.125)
        location = self.rect.topleft + txt_padding
        window.blit(text_surface, location)
