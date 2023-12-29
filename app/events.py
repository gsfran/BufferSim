import pygame as pg

from . import buffer

CONV_CYCLE_EVENT = pg.USEREVENT
VERT_CYCLE_EVENT = pg.USEREVENT + 1
XFER_CYCLE_EVENT = pg.USEREVENT + 2


def handle_event(event: pg.event.Event) -> None:

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

    MANUAL_CONTROLS = {
        pg.K_u: buffer.cycle_conveyor,
        pg.K_i: buffer.index_inlet,
        pg.K_o: buffer.index_outlet,
        pg.K_p: buffer.transfer_push,
        pg.K_LEFTBRACKET: buffer.move_xfer_down,
        pg.K_RIGHTBRACKET: buffer.move_xfer_up
    }

    # this calls the manual_control method which checks if autorun is active,
    # if not then it executes the passed command
    if event.key in MANUAL_CONTROLS.keys():
        buffer.manual_input(MANUAL_CONTROLS[event.key])

    CONFIG_CHANGE = {
        pg.K_0,
        pg.K_1,
        pg.K_2,
        pg.K_3,
        pg.K_4,
        pg.K_5,
        pg.K_6,
        pg.K_7,
        pg.K_8
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
    # if buffer.cycle_time > 20:
    if True:
        buffer.speed *= 2
        reset_timers(buffer.cycle_time)


def speed_down() -> None:
    if buffer.cycle_time < 6000:
        buffer.speed /= 2
        reset_timers(buffer.cycle_time)


def reset_timers(cycle_time: int) -> None:
    # current logic

    pg.time.set_timer(CONV_CYCLE_EVENT, cycle_time)
    pg.time.delay(int(cycle_time / 3))
    pg.time.set_timer(VERT_CYCLE_EVENT, cycle_time)
    pg.time.delay(int(cycle_time / 3))
    pg.time.set_timer(XFER_CYCLE_EVENT, cycle_time)