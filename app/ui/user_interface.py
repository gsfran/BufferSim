from pygame.surface import Surface

from . import ControlsDisplay, SpeedDisplay


class UserInterface:

    def __init__(self) -> None:
        self.speed_block = SpeedDisplay()
        self.controls_block = ControlsDisplay()

    def draw(self, window: Surface) -> None:
        self.speed_block.draw(window=window)
        self.controls_block.draw(window=window)