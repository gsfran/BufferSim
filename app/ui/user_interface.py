from pygame.surface import Surface

from . import SpeedDisplay


class UserInterface:

    def __init__(self) -> None:
        self.speed_block = SpeedDisplay()

    def draw(self, window: Surface) -> None:
        self.speed_block.draw(window=window)
