from random import randint

import pygame
from pygame import Rect, draw
from pygame.surface import Surface

from . import SCREEN_HEIGHT, SCREEN_WIDTH
from .colors import BLACK, GREY
from .components import HorizConveyor, VertConveyor, XferCarriage


HORIZ_CYCLE_EVENT = pygame.USEREVENT
VERT_CYCLE_EVENT = pygame.USEREVENT + 1


class BufferSystem:

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.max_pos = (capacity / 2) - 1
        self.cycle_time = 500  # ms

        self.width = SCREEN_WIDTH / 5
        self.height = SCREEN_HEIGHT * 0.8
        self.pitch_height = self.height / (self.capacity / 2)
        self.part_height = self.pitch_height / 5

        self.inlet_pos = 4
        self.outlet_pos = 5
        self.auto_cycle: bool = True
        self.downstream_fault: bool = False
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

    @property
    def part_at_inlet_bottom(self) -> bool:
        return self.conveyor.contents[self.inlet_pos]

    @property
    def part_at_outlet_bottom(self) -> bool:
        return self.conveyor.contents[self.outlet_pos]

    @property
    def part_at_inlet_top(self) -> bool:
        return self.inlet.contents[self.xfer.position]

    @property
    def part_at_outlet_top(self) -> bool:
        return self.outlet.contents[self.xfer.position]

    @property
    def buffer_full(self) -> bool:
        if self.xfer.position == self.max_pos and (
            self.part_at_inlet_top and self.part_at_outlet_top
        ):
            return True
        return False

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

        if self.part_at_inlet_top:
            self.move_xfer_up()

        if any(self.inlet.contents[self.xfer.position:]):
            raise Exception(
                "Part on inlet conveyor crashed into transfer carriage "
                "or is currently above the transfer carriage."
            )

        self.inlet.contents[0] = self.part_at_inlet_bottom
        self.inlet.index_up()
        self.conveyor.contents[self.inlet_pos] = False

    def index_outlet(self) -> None:

        if self.outlet.contents[0] or self.part_at_outlet_bottom:
            raise Exception(
                "Part on outlet conveyor crashed into horizontal conveyor "
                "during index."
            )
        self.outlet.index_down()
        self.conveyor.contents[self.outlet_pos] = self.outlet.contents[0]
        self.outlet.contents[0] = False

    def transfer_push(self) -> None:

        if (self.part_at_inlet_top and self.part_at_outlet_top):
            raise Exception(
                "Part crashed into another part during transfer push."
            )

        if self.part_at_inlet_top:
            self.outlet.contents[self.xfer.position] = True
            self.inlet.contents[self.xfer.position] = False

    def index_conveyor(self) -> None:

        if randint(0, 100) % 3:
            new_part = True
        else:
            new_part = False

        self.conveyor.index(new_part=new_part)

    def move_xfer_up(self) -> None:
        if self.xfer.position == (self.capacity / 2) - 1:
            print("Transfer Carriage already at end of travel")
        else:
            self.xfer.move_up()

    def move_xfer_down(self) -> None:
        if self.xfer.position == 1:
            print("Transfer Carriage already at end of travel")
        else:
            self.xfer.move_down()

    def toggle_autocycle(self) -> None:
        self.auto_cycle = not self.auto_cycle

    def toggle_fault(self) -> None:
        self.downstream_fault = not self.downstream_fault

    def horizontal_cycle(self) -> None:

        if not self.buffer_full:
            self.index_conveyor()

        if self.part_at_inlet_top and not self.part_at_outlet_top:
            self.transfer_push()

        pygame.time.delay(self.cycle_time // 4)
        vertical_cycle_event = pygame.event.Event(VERT_CYCLE_EVENT, {})
        pygame.event.post(vertical_cycle_event)

    def vertical_cycle(self) -> None:

        if not self.part_at_outlet_bottom and not self.downstream_fault:
            self.index_outlet()

        if self.xfer.position < self.max_pos and (
            self.part_at_inlet_top and self.part_at_outlet_top
        ):
            self.move_xfer_up()

        if self.part_at_inlet_bottom and self.downstream_fault:
            self.index_inlet()

        if self.xfer.position > 1 and not (
            self.part_at_inlet_top or self.part_at_outlet_top
        ):
            self.move_xfer_down()
