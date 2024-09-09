from random import randint
from types import MethodType

from pygame import Rect, draw, quit
from pygame.surface import Surface

from .colors import BLACK, GREY
from .components import HorizConveyor, VertConveyor, XferCarriage
from .config import (BUFFER_CAPACITY, HORIZ_CONV_CAPACITY, SCREEN_HEIGHT,
                     SCREEN_WIDTH)

BASE_CYCLE_TIME = 3000  # milliseconds


class BufferSystem:
    """
    The collective buffer system, consisting of:
        1 Horizontal Conveyor component
        2 Vertical Conveyor components
        1 Transfer Carriage component
    along with methods and properties to handle all of the business logic
    as well as draw the system and its subsystems on the display window.

    """

    def __init__(self) -> None:
        self.capacity = BUFFER_CAPACITY
        self.max_pos = (self.capacity / 2) - 1  # uppermost transfer position
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
        """Initializes the system's subcomponents."""
        self.inlet = VertConveyor(
            capacity=int(self.capacity/2),
            part_height=self.part_height,
            conv_pos=self.inlet_pos
        )

        self.outlet = VertConveyor(
            capacity=int(self.capacity/2),
            part_height=self.part_height,
            conv_pos=self.outlet_pos
        )

        self.conveyor = HorizConveyor(
            part_height=self.part_height
        )

        self.xfer = XferCarriage(
            initial_pos=int(self.capacity/2)-1
        )

    def reset_buffer(self) -> None:
        self.build()

    def quit(self) -> None:
        """Quits the simulation."""
        quit()
        exit()

    def draw(self, window: Surface) -> None:
        """Handles drawing of the buffer system/components to
        the pygame window."""

        x_pos = (SCREEN_WIDTH - self.width) / 2
        y_pos = (SCREEN_HEIGHT - self.height) / 2

        self.rect = Rect(x_pos, y_pos, self.width, self.height)
        self.corners = [
            self.rect.topleft, self.rect.topright,
            self.rect.bottomright, self.rect.bottomleft
        ]

        self.pitch_height = self.height / (self.capacity / 2)

        draw.rect(window, GREY, self.rect)
        self.inlet.draw(window=window)
        self.outlet.draw(window=window)
        self.conveyor.draw(window=window)
        self.xfer.draw(window=window, buffer_rect=self.rect,
                       pitch_height=self.pitch_height)

        draw.lines(window, BLACK, True, self.corners)
        draw.line(window, BLACK, self.rect.midtop, self.rect.midbottom)

    def manual_input(self, move_command: MethodType) -> None:
        """Checks if Autorun is active before executing manual controls."""
        if not self.autorun:
            move_command()

    def index_inlet(self) -> None:
        """Indexes the inlet-side vertical conveyor upwards."""
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
        """Indexes the outlet-side vertical conveyor downwards."""
        if self.outlet.contents[0] or self.part_at_outlet_bottom:
            raise Exception(
                "Part on outlet conveyor crashed into horizontal conveyor "
                "during index."
            )
        self.outlet.index_down()
        self.conveyor.contents[self.outlet_pos] = self.outlet.contents[0]
        self.outlet.contents[0] = False

    def transfer_push(self) -> None:
        """Handles the transfer carriage pushing a part
        from inlet to outlet."""

        if (self.part_at_inlet_top and self.part_at_outlet_top):
            raise Exception(
                "Part crashed into another part during transfer push."
            )

        if self.part_at_inlet_top:
            self.outlet.contents[self.xfer.position] = True
            self.inlet.contents[self.xfer.position] = False

    def cycle_conveyor(self) -> None:
        """
        Indexes the horizontal conveyor and determines if
        a part is loaded to the first conveyor position using
        a configurable probability.

        Checks if upstream cell is inhibited due to capacity
        or if it is paused by the user. If not, rolls 0-100
        then modulo's the result with value of MOD to give
        the desired probability of A (a part is present):
            P(A) = 1 - 1/(MOD - 1)

        """
        MOD = 3  # P(A) = 67%

        if randint(0, 100) % MOD and (
            self.part_inflow and not self.upstream_inhibit
        ):
            new_part = True
        else:
            new_part = False

        self.conveyor.index(new_part=new_part)

    def move_xfer_up(self) -> None:
        """Moves the Transfer Carriage up by one position if
        not already at its maximum."""
        if self.xfer.position == self.max_pos:
            print("Transfer Carriage already at end of travel")
        else:
            self.xfer.move_up()

    def move_xfer_down(self) -> None:
        """Moves the Transfer Carriage down by one position if
        not already at its minimum."""
        if self.xfer.position == self.min_pos:
            print("Transfer Carriage already at end of travel")
        else:
            self.xfer.move_down()

    def toggle_autorun(self) -> None:
        """Toggles autorun on/off"""
        self.autorun = not self.autorun

    def enable_step_mode(self) -> None:
        """Step Mode not yet implemented."""
        pass

    def set_config(self, config: int) -> None:
        """
        Called whenever a configuration change is made.

        Sets the new configuration and minimum position,
        pauses part inflow and disables downstream stoppage,
        and calls the reset_buffer method for a fresh start.

        Args:
            config (int): New configuration number.
        """

        self.config = config
        if config == 0:
            self.min_pos = 1

        else:
            self.min_pos = 2

        self.part_inflow = False
        self.downstream_stoppage = False
        self.reset_buffer()

    def toggle_downstream_fault(self) -> None:
        """Toggles downstream fault on/off"""
        self.downstream_stoppage = not self.downstream_stoppage

    def toggle_part_inflow(self) -> None:
        """Toggles part inflow from upstream on/off"""
        self.part_inflow = not self.part_inflow

    def cycle_verticals(self) -> None:
        """Calls an implementation of the Strategy design pattern
        to handle various logic configurations. Based on the returned
        tuple, indexes the vertical conveyors appropriately."""

        inlet_cycle, outlet_cycle = self.vert_strategy

        if inlet_cycle:
            self.index_inlet()

        if outlet_cycle:
            self.index_outlet()

    def cycle_xfer_push(self) -> None:
        """Moves down one position if no part is seen by the transfer carriage,
        then pushes a part if one is seen at the inlet but not the outlet."""
        if self.xfer.position > self.min_pos and not (
            self.part_at_inlet_top or self.part_at_outlet_top
        ):
            self.move_xfer_down()
        # Pusher
        if self.part_at_inlet_top and not self.part_at_outlet_top:
            self.transfer_push()

    @property
    def cycle_time(self) -> int:
        """Simulation cycle time in milliseconds"""
        self._cycle_time = int(BASE_CYCLE_TIME / self.speed)
        return self._cycle_time

    @property
    def part_at_inlet_bottom(self) -> bool:
        """Part present at the bottom of the inlet conveyor."""
        return self.conveyor.contents[self.inlet_pos]

    @property
    def part_at_outlet_bottom(self) -> bool:
        """Part present at the bottom of the outlet conveyor."""
        return self.conveyor.contents[self.outlet_pos]

    @property
    def part_at_inlet_top(self) -> bool:
        """Part present at the inlet side of the transfer carriage."""
        return self.inlet.contents[self.xfer.position]

    @property
    def part_at_outlet_top(self) -> bool:
        """Part present at the outlet side of the transfer carriage."""
        return self.outlet.contents[self.xfer.position]

    @property
    def infeed_part_count(self) -> int:
        """Counts parts on the horizontal conveyor for capacity evaluation."""
        return self.conveyor.contents[:self.outlet_pos].count(True)

    @property
    def upstream_inhibit(self) -> bool:
        """Inhibits part inflow when capacity of the system is reached."""
        if (
            2 * (self.xfer.position) + self.infeed_part_count
        ) >= (self.capacity - 2):
            return True
        return False

    @property
    def vert_strategy(self) -> tuple[bool, bool]:
        """Determines motion of the vertical conveyors based on system state
        and configuration. Returns a tuple of booleans representing the
        two vertical conveyors.

        Returns:
            tuple[bool, bool]: Commands for cycling the vertical conveyors."""

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
