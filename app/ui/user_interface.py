from __future__ import annotations

# from pygame import Rect, draw
from pygame.surface import Surface

# from app import buffer
# from app.colors import BLACK, GREY
# from app.config import SCREEN_HEIGHT, SCREEN_WIDTH

from . import SpeedDisplay


class UserInterface:

    def __init__(self) -> None:
        self.speed_block = SpeedDisplay()

    def draw(self, window: Surface) -> None:
        self.speed_block.draw(window=window)
