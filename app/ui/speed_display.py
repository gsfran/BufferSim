import pygame
from pygame import Rect, draw
from pygame.font import Font
from pygame.surface import Surface

from app import buffer
from app.colors import BLACK, LIGHT_GREY
from app.config import SCREEN_HEIGHT, SCREEN_WIDTH

SPEED_DISPLAY_FONT: Font = pygame.font.SysFont("Courier New", 30, bold=True)


class SpeedDisplay:
    """Display block showing the current simulation speed."""

    def __init__(self) -> None:
        self.bg_color = LIGHT_GREY
        self.outline_color = BLACK
        self.text_color = BLACK

        self.width = SCREEN_WIDTH * 0.3
        self.height = SCREEN_HEIGHT * 0.10

    def draw(self, window: Surface) -> None:

        self.x_pos = (SCREEN_WIDTH * 0.95) - self.width
        self.y_pos = (SCREEN_HEIGHT * 0.025)

        self.rect = Rect(self.x_pos, self.y_pos, self.width, self.height)

        draw.rect(window, self.bg_color, self.rect)

        corners = [
            self.rect.topleft, self.rect.topright,
            self.rect.bottomright, self.rect.bottomleft
        ]
        draw.lines(window, self.outline_color, True, corners)

        speed_text = f'Speed Multiplier: {buffer.speed}x'
        cycle_time_text = f'Cycle Time: {buffer.cycle_time}ms'

        text_surface = SPEED_DISPLAY_FONT.render(
            speed_text, True, self.text_color
        )
        cycle_time_surface = SPEED_DISPLAY_FONT.render(
            cycle_time_text, True, self.text_color
        )

        x_padding = self.width * 0.1
        y_padding = self.height * 0.1

        speed_location = (self.rect.left + x_padding,
                          self.rect.top + y_padding)
        cycle_time_location = (self.rect.left + x_padding,
                               self.rect.centery + y_padding)

        window.blit(text_surface, speed_location)
        window.blit(cycle_time_surface, cycle_time_location)
