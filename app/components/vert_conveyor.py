from __future__ import annotations

from pygame import Rect, draw
from pygame.surface import Surface

from app import SCREEN_HEIGHT, SCREEN_WIDTH
from app.colors import BLACK, GREY, WHITE


class VertConveyor:
    """
    A vertical indexing conveyor which raises and lowers parts
    from the main horizontal conveyor.

    The buffer system consists of two (2) vertical conveyors, 
    along with a mechanism capable of transferring a part
    from one of these vertical conveyors to the other.

    The inlet side lifts parts up from the main conveyor,
    staging them for transfer to the outlet conveyor. 

    The outlet conveyor receives parts from the inlet conveyor,
    and lowers them onto the main horizontal conveyor when it can.

    The transfer mechanism sits upon a carriage capable of
    moving up and down as necessary as the vertical conveyors index.

    """

    def __init__(self, capacity: int, part_height: int) -> None:
        self.capacity = capacity
        self.part_height = part_height
        self.build()

    def build(self) -> None:
        self.contents: list[bool] = []
        for _ in range(self.capacity):
            self.contents.append(False)

    def draw(self, window: Surface, conv_pos: int) -> None:

        self.width = SCREEN_WIDTH / 10
        self.height = SCREEN_HEIGHT * 0.8
        self.x_pos = SCREEN_WIDTH - ((conv_pos + 1) * self.width)
        self.y_pos = (SCREEN_HEIGHT - self.height) / 2

        self.rect = Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.pitch_height = self.height / self.capacity

        draw.rect(window, GREY, self.rect)
        self.draw_contents(window=window)

    def draw_contents(self, window: Surface) -> None:

        for i, part in enumerate(self.contents):
            # +1 is to account for y_pos being the top of the rect
            y_pos = self.rect.bottom - (self.pitch_height * (i + 1))
            r = Rect(self.rect.left, y_pos, self.width, self.pitch_height)
            corners = [r.topleft, r.topright, r.bottomright, r.bottomleft]
            if part:
                part_y = r.bottom - self.part_height
                part_r = Rect(self.rect.left, part_y,
                              self.width, self.part_height)
                draw.rect(window, WHITE, part_r)
                draw.line(window, BLACK, part_r.topleft, part_r.topright)
            draw.lines(window, BLACK, True, corners)

    def index_up(self) -> None:
        new_contents = [False] + self.contents[:-1]
        self.contents = new_contents

    def index_down(self) -> None:
        if self.contents[0]:
            raise Exception("Crash, part at position 0 when indexing down.")

        new_contents = self.contents[1:] + [False]
        self.contents = new_contents
