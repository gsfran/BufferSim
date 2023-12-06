from random import randint

from pygame import Rect, draw
from pygame.surface import Surface

from . import SCREEN_HEIGHT, SCREEN_WIDTH
from .colors import BLACK, GREY
from .components import HorizConveyor, VertConveyor, XferCarriage


class BufferSystem:

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity

        self.width = SCREEN_WIDTH / 5
        self.height = SCREEN_HEIGHT * 0.8
        self.pitch_height = self.height / (self.capacity / 2)
        self.part_height = self.pitch_height / 5

        self.inlet_pos = 4
        self.outlet_pos = 5
        self.build()

    def build(self) -> None:

        self.inlet = VertConveyor(
            capacity=int(self.capacity/2), part_height=self.part_height
        )
        self.outlet = VertConveyor(
            capacity=int(self.capacity/2), part_height=self.part_height
        )
        self.conveyor = HorizConveyor(part_height=self.part_height)
        self.xfer = XferCarriage(initial_pos=int(self.capacity/2)-1)

        for _ in range(10):
            self.index_conveyor()

    def draw(self, window: Surface) -> None:

        x_pos = (SCREEN_WIDTH - self.width) / 2
        y_pos = (SCREEN_HEIGHT - self.height) / 2

        self.rect = Rect(x_pos, y_pos, self.width, self.height)
        self.corners = [
            self.rect.topleft, self.rect.topright,
            self.rect.bottomright, self.rect.bottomleft
        ]

        self.pitch_height = self.height / (self.capacity / 2)

        draw.rect(window, GREY, self.rect)
        self.inlet.draw(window=window, conv_pos=self.inlet_pos)
        self.outlet.draw(window=window, conv_pos=self.outlet_pos)
        self.conveyor.draw(window=window)
        self.xfer.draw(window=window, buffer_rect=self.rect,
                       pitch_height=self.pitch_height)

        draw.lines(window, BLACK, True, self.corners)
        center_line = [
            (self.rect.centerx, self.rect.top),
            (self.rect.centerx, self.rect.bottom)
        ]
        draw.line(window, BLACK, *center_line)

    def index_inlet(self) -> None:

        if any(self.inlet.contents[self.xfer.position:]):
            raise Exception(
                "Part on inlet conveyor crashed into transfer carriage "
                "or is currently above the transfer carriage."
            )

        self.inlet.contents[0] = self.conveyor.contents[self.inlet_pos]
        self.inlet.index_up()
        self.conveyor.contents[self.inlet_pos] = False

    def index_outlet(self) -> None:

        if self.outlet.contents[0] or self.conveyor.contents[self.outlet_pos]:
            raise Exception(
                "Part on outlet conveyor crashed into horizontal conveyor "
                "during index."
            )
        self.outlet.index_down()
        self.conveyor.contents[self.outlet_pos] = self.outlet.contents[0]
        self.outlet.contents[0] = False

    def transfer_push(self) -> None:

        part_at_inlet = self.inlet.contents[self.xfer.position]
        part_at_outlet = self.outlet.contents[self.xfer.position]

        if (part_at_inlet and part_at_outlet):
            raise Exception(
                "Part crashed into another part during transfer push."
            )

        if part_at_inlet:
            self.outlet.contents[self.xfer.position] = True
            self.inlet.contents[self.xfer.position] = False

    def index_conveyor(self) -> None:

        if randint(0, 100) % 4:
            new_part = True
        else:
            new_part = False

        self.conveyor.index(new_part=new_part)

    def move_xfer_up(self) -> None:
        if self.xfer.position == (self.capacity / 2) - 1:
            raise Exception("Transfer Carriage already at end of travel")
        self.xfer.move_up()

    def move_xfer_down(self) -> None:
        if self.xfer.position == 0:
            raise Exception("Transfer Carriage already at end of travel")
        self.xfer.move_down()
