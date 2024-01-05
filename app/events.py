import pygame as pg

from . import buffer

CONV_CYCLE_EVENT = pg.USEREVENT
VERT_CYCLE_EVENT = pg.USEREVENT + 1
XFER_CYCLE_EVENT = pg.USEREVENT + 2


def handle_event(event: pg.event.Event) -> None:
    """
    Generic event handling function which is called for each event
    and handles it according to its type.

    QUIT type will exit the simulation.
    KEYDOWN type will handle the input key.

    The other event types are triggered by timers. They handle
    the buffer components' motions while in Autorun mode.

    """

    if event.type == pg.QUIT:
        pg.quit()
        exit()

    elif event.type == pg.KEYDOWN:
        handle_input(event=event)

    elif buffer.autorun:
        if event.type == CONV_CYCLE_EVENT:
            buffer.cycle_conveyor()
        if event.type == VERT_CYCLE_EVENT:
            buffer.cycle_verticals()
        if event.type == XFER_CYCLE_EVENT:
            buffer.cycle_xfer_push()


def handle_input(event: pg.event.Event) -> None:
    """
    Inputs are handled using discrete functions/methods
    collected in dict/set objects by input type. A reference
    looks up the function by key and calls it if found, this
    makes it easier to remap hotkeys if desired.


    MANUAL_CONTROLS will index buffer components if Autorun is not active.

    CONFIG_CHANGE inputs change the buffer configuration and logic to
    several presaved options corresponding to updates made to the machine:
        0: Current State
        1: Original logic
        2: 12/11/23 update
        3: 12/18/23 update

    AUTO_CONTROLS inputs are the main controls meant to be used in Autorun.

    """

    MANUAL_CONTROLS = {
        pg.K_u: buffer.cycle_conveyor,
        pg.K_i: buffer.index_inlet,
        pg.K_o: buffer.index_outlet,
        pg.K_p: buffer.transfer_push,
        pg.K_LEFTBRACKET: buffer.move_xfer_down,
        pg.K_RIGHTBRACKET: buffer.move_xfer_up
    }

    if event.key in MANUAL_CONTROLS.keys():
        """This calls the manual_input method which checks if autorun is active,
        and if not then it executes the passed command. """
        buffer.manual_input(MANUAL_CONTROLS[event.key])

    CONFIG_CHANGE = {
        pg.K_0,
        pg.K_1,
        pg.K_2,
        pg.K_3,
        # pg.K_4,
        # pg.K_5,
        # pg.K_6,
        # pg.K_7,
        # pg.K_8,
        # pg.K_9
    }

    if event.key in CONFIG_CHANGE:
        buffer.set_config(int(event.unicode))
        reset_timers(buffer.cycle_time)

    AUTO_CONTROLS = {
        pg.K_a: buffer.toggle_autorun,
        pg.K_s: buffer.enable_step_mode,
        pg.K_d: buffer.toggle_downstream_fault,
        pg.K_f: buffer.toggle_part_inflow,
        pg.K_r: buffer.reset_buffer,
        pg.K_q: buffer.quit,
        pg.K_e: speed_up,
        pg.K_w: speed_down
    }

    if event.key in AUTO_CONTROLS.keys():
        AUTO_CONTROLS[event.key]()


def speed_up() -> None:
    """
    Increases simulation speed by a factor of 2.
    Maximum speed is 2048x = 1.4ms cycle time which rounds to 1ms.
    """
    if buffer.cycle_time > 1:
        buffer.speed *= 2
        reset_timers(buffer.cycle_time)


def speed_down() -> None:
    """
    Decreases simulation speed by a factor of 2.
    Minimum speed is 0.5x = 6 second cycle time.
    """
    if buffer.cycle_time < 6000:
        buffer.speed /= 2
        reset_timers(buffer.cycle_time)


def reset_timers(cycle_time: int) -> None:
    """
    Resets the autorun timers, is called whenever the
    buffer config or cycle time is changed.

    Args:
        cycle_time (int): New cycle time in milliseconds.
    """

    pg.time.set_timer(CONV_CYCLE_EVENT, cycle_time)
    pg.time.delay(int(cycle_time / 3))
    pg.time.set_timer(VERT_CYCLE_EVENT, cycle_time)
    pg.time.delay(int(cycle_time / 3))
    pg.time.set_timer(XFER_CYCLE_EVENT, cycle_time)
