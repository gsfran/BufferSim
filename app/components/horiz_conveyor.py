from __future__ import annotations

from pygame import Rect, draw
from pygame.surface import Surface

from app.colors import BLACK, DARK_GREY, WHITE
from app.config import HORIZ_CONV_CAPACITY, SCREEN_HEIGHT, SCREEN_WIDTH


class HorizConveyor:
    """
    A horizontal indexing conveyor feeding parts
    to a palletizing cell.

    In the event this palletizing cell goes down, the
    inlet vertical conveyor lifts parts from this
    horizontal main conveyor to avoid upstream stoppage.

    When the palletizing cell is returned to production,
    the outlet vertical conveyor backfills voids on this
    horizontal conveyor to empty out the buffer's contents.

    """

    def __init__(self, part_height: int) -> None:
        self.capacity = HORIZ_CONV_CAPACITY
        self.part_height = part_height
        self.build()

    def build(self) -> None:
        self.contents = []
        for _ in range(self.capacity):
            self.contents.append(False)

    def index(self, new_part: bool) -> None:
        new_contents = [new_part] + self.contents[:-1]
        self.contents = new_contents
        pass

    def draw(self, window: Surface) -> None:
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT * 0.05
        self.pitch_width = self.width / self.capacity

        x_pos = 0
        y_pos = SCREEN_HEIGHT * 0.9
        self.rect = Rect(x_pos, y_pos, self.width, self.height)

        corners = [
            self.rect.topleft, self.rect.topright,
            self.rect.bottomright, self.rect.bottomleft
        ]

        # background
        draw.rect(window, DARK_GREY, self.rect)
        # border
        draw.lines(window, BLACK, True, corners)

        self.draw_contents(window=window)

    def draw_contents(self, window: Surface) -> None:

        for i, part in enumerate(self.contents):
            x_pos = self.rect.right - (self.pitch_width * (i + 1))
            r = Rect(x_pos, self.rect.top - self.part_height,
                     self.pitch_width, self.part_height)
            corners = [r.topleft, r.topright, r.bottomright, r.bottomleft]
            if part:
                draw.rect(window, WHITE, r)
                draw.lines(window, BLACK, True, corners)
