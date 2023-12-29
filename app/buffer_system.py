from abc import ABC
from random import randint
from types import MethodType

from pygame import Rect, draw, quit
from pygame.surface import Surface

from .colors import BLACK, GREY
from .components import HorizConveyor, VertConveyor, XferCarriage
from .config import HORIZ_CONV_CAPACITY, SCREEN_HEIGHT, SCREEN_WIDTH

BASE_CYCLE_TIME = 3000  # ms
TOTAL_CAPACITY = 150


class BufferSystem:

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.max_pos = (capacity / 2) - 1  # uppermost transfer position
        self.min_pos = 1  # lowermost transfer position
        self.speed = 1.0  # sim speed
        self.config = 0  # buffer configuration and logic

        self.width = SCREEN_WIDTH / (HORIZ_CONV_CAPACITY / 2)
        self.height = SCREEN_HEIGHT * 0.8
        self.pitch_height = self.height / (self.capacity / 2)  # 1 pitch = 10mm
        self.scale = self.pitch_height / 10  # pixels per 1 mm
        self.part_height = self.pitch_height / 1

        self.inlet_pos = int(HORIZ_CONV_CAPACITY / 2) - 1
        self.outlet_pos = int(HORIZ_CONV_CAPACITY / 2)

        self.autorun: bool = False
        self.downstream_stoppage: bool = False
        self.part_inflow: bool = False

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

    def reset_buffer(self) -> None:
        self.build()

    def quit(self) -> None:
        quit()
        exit()

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
        draw.line(window, BLACK, self.rect.midtop, self.rect.midbottom)

    def manual_input(self, move_command: MethodType) -> None:
        """
        Checks if autorun is active before executing manual controls.

        """
        if not self.autorun:
            move_command()

    def index_inlet(self) -> None:
        """
        Indexes the inlet-side vertical conveyor upwards.

        """
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

    def cycle_conveyor(self) -> None:

        if randint(0, 100) % 3 and (
            self.part_inflow and not self.upstream_inhibit
        ):
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

    def toggle_autorun(self) -> None:
        self.autorun = not self.autorun

    def enable_step_mode(self) -> None:
        pass

    def set_config(self, config: int) -> None:

        self.config = config
        if config == 0:
            self.min_pos = 1

        else:
            self.min_pos = 2

        self.part_inflow = False
        self.downstream_stoppage = False
        self.reset_buffer()

    def toggle_downstream_fault(self) -> None:
        self.downstream_stoppage = not self.downstream_stoppage

    def toggle_part_inflow(self) -> None:
        self.part_inflow = not self.part_inflow

    def cycle_verticals(self) -> None:

        inlet_cycle, outlet_cycle = self.vert_strategy

        if inlet_cycle:
            self.index_inlet()

        if outlet_cycle:
            self.index_outlet()

    def cycle_xfer_push(self) -> None:
        if self.xfer.position > self.min_pos and not (
            self.part_at_inlet_top or self.part_at_outlet_top
        ):
            self.move_xfer_down()
        # Pusher
        if self.part_at_inlet_top and not self.part_at_outlet_top:
            self.transfer_push()

    @property
    def cycle_time(self) -> int:
        self._cycle_time = int(BASE_CYCLE_TIME / self.speed)
        # print(self._cycle_time)
        return self._cycle_time

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
    def infeed_part_count(self) -> int:
        return self.conveyor.contents[:self.outlet_pos].count(True)

    @property
    def upstream_inhibit(self) -> bool:
        if (
            2 * (self.xfer.position) + self.infeed_part_count
        ) >= (self.capacity - 2):
            return True
        return False

    @property
    def vert_strategy(self) -> (bool, bool):

        inlet = outlet = False

        if self.config == 0:

            if self.part_at_inlet_bottom and self.downstream_stoppage:
                inlet = True

        if self.config == 1:

            # original config, inlet cycles as long as no crash will occur
            if not self.part_at_inlet_top or self.xfer.position < self.max_pos:
                inlet = True

        elif self.config == 2:

            # next revision, inlet cycles conditionally if part is present
            if not self.part_at_inlet_top or self.xfer.position < self.max_pos:
                if self.part_at_inlet_bottom:
                    inlet = True

        elif self.config == 3:

            if not self.part_at_inlet_top or self.xfer.position < self.max_pos:
                if self.part_at_inlet_bottom:
                    inlet = True

            # fix for leaving part at inaccessible slot
            if not (
                (
                    self.part_at_inlet_bottom or self.part_at_inlet_top
                ) or self.part_at_outlet_top
            ):
                inlet = True

        # outlet logic, unchanged from the start
        if not self.downstream_stoppage and not self.part_at_outlet_bottom:
            outlet = True

        return inlet, outlet
