from __future__ import annotations

from pygame import draw, Rect
from pygame.surface import Surface


class HorizConveyor:
    def __init__(self) -> None:
        self.size = 10
        self.build()

    def build(self):
        self.contents = []
        for _ in range(self.size):
            self.contents.append(False)

    def index(self, new_part: bool = False) -> None:
        pass


class VertConveyor:
    def __init__(self, size: int) -> None:
        self.size = size
        self.build()

    def build(self):
        self.contents = []
        for _ in range(self.size):
            self.contents.append(False)

    def index_up(self, new_part: bool):
        new_contents = new_part + self.contents[:-1]
        self.contents = new_contents

    def index_down(self):
        if self.contents[0]:
            raise Exception("Crash, part at position 0 when indexing down.")
        new_contents = self.contents[1:] + False
        self.contents = new_contents

    def draw(self, window: Surface, conv_pos: int) -> None:
        screen_width, screen_height = window.get_size()

        self.width = screen_width / 10
        self.height = screen_height * 0.75
        x_pos = screen_width - ((conv_pos + 1) * self.width)
        y_pos = (screen_height - self.height) / 2

        self.rect = Rect(x_pos, y_pos, self.width, self.height)

        draw.rect(window, (20, 20, 20), Rect(self.rect))
        
        # for pitch in self.contents:
        #     rect = Rect()


class TransferCarriage:
    def __init__(self, initial_pos: int) -> None:
        self.position = initial_pos

    def move_up(self) -> None:
        self.position += 1

    def move_down(self) -> None:
        self.position -= 1

    def draw(self, window: pygame.display):
        pass
