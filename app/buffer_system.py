from pygame.surface import Surface
from pygame import draw, Rect

from .components import VertConveyor, TransferCarriage, HorizConveyor


class BufferSystem:
    def __init__(self, max_height: int, color: tuple[int] = (120, 120, 120)) -> None:
        self.max_height = max_height
        self.color = color
        self.inlet_pos = 4
        self.outlet_pos = 5
        self.build()

    def build(self) -> None:

        self.inlet = VertConveyor(self.max_height)
        self.outlet = VertConveyor(self.max_height)
        self.conveyor = HorizConveyor()
        self.xfer = TransferCarriage(self.max_height)

    def part_at_bottom_of_inlet(self) -> bool:
        return self.inlet.contents[4]

    def part_at_bottom_of_outlet(self) -> bool:
        return self.outlet.contents[5]

    def draw(self, window: Surface) -> None:
        screen_width, screen_height = window.get_size()

        self.width = screen_width / 5
        self.height = screen_height * 0.8
        x_pos = (screen_width - self.width) / 2
        y_pos = (screen_height - self.height) / 2

        self.rect = Rect(x_pos, y_pos, self.width, self.height)

        draw.rect(window, self.color, self.rect)
        self.inlet.draw(window, self.inlet_pos)
        self.outlet.draw(window, self.outlet_pos)
