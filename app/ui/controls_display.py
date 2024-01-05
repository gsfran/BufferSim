import pygame
from pygame import Rect, draw
from pygame.font import Font
from pygame.surface import Surface

from app import buffer
from app.colors import BLACK, LIGHT_GREY
from app.config import SCREEN_HEIGHT, SCREEN_WIDTH

FONT_SIZE = 30
CONTROLS_DISPLAY_FONT: Font = pygame.font.SysFont(
    "Helvetica", FONT_SIZE, bold=True)


class ControlsDisplay:
    """Display block showing the available controls."""

    def __init__(self) -> None:
        self.bg_color = LIGHT_GREY
        self.outline_color = BLACK
        self.text_color = BLACK

        self.width = SCREEN_WIDTH * 0.25
        self.height = SCREEN_HEIGHT * 0.6

    def draw(self, window: Surface) -> None:

        self.x_pos = (SCREEN_WIDTH * 0.025)
        self.y_pos = (SCREEN_HEIGHT * 0.025)

        self.rect = Rect(self.x_pos, self.y_pos, self.width, self.height)

        draw.rect(window, self.bg_color, self.rect)

        corners = [
            self.rect.topleft, self.rect.topright,
            self.rect.bottomright, self.rect.bottomleft
        ]
        draw.lines(window, self.outline_color, True, corners)

        lines = [
            'MANUAL CONTROLS', '',
            'U -- Horizontal Conveyor',
            'I -- Inlet Conveyor',
            'O -- Outlet Conveyor',
            'P -- Transfer Push',
            '[ -- Move Transfer Down',
            '] -- Move Transfer Up'
        ]

        text = []
        for line in lines:
            text.append(CONTROLS_DISPLAY_FONT.render(
                line, True, self.text_color))

        x_padding = self.width * 0.05
        y_padding = self.height * 0.025

        location = (self.rect.left + x_padding,
                    self.rect.top + y_padding)

        for i, line in enumerate(text):
            position = (location[0], location[1] + i * (FONT_SIZE * 1.5))
            window.blit(text[i], position)
