from __future__ import annotations
from pygame import Rect, draw

from pygame.surface import Surface

from app.colors import BLACK, RED


class XferCarriage:
    def __init__(self, initial_pos: int) -> None:
        self.position = initial_pos

    def move_up(self) -> None:
        self.position += 1

    def move_down(self) -> None:
        self.position -= 1

    def draw(self, window: Surface, buffer_rect: Rect, pitch_height: int):
        self.width = buffer_rect.width
        self.height = pitch_height / 5

        x_pos = buffer_rect.left
        y_pos = buffer_rect.bottom - (pitch_height * (self.position + 0.5))

        self.rect = Rect(x_pos, y_pos, self.width, self.height)

        corners = [
            self.rect.topleft, self.rect.topright,
            self.rect.bottomright, self.rect.bottomleft
        ]

        # background
        draw.rect(window, RED, self.rect)
        # border
        draw.lines(window, BLACK, True, corners)
