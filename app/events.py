from datetime import datetime as dt

import pygame

from . import buffer

HORIZ_CYCLE_EVENT = pygame.USEREVENT
VERT_CYCLE_EVENT = pygame.USEREVENT + 1
CURRENT_CYCLE_CONV_EVENT = pygame.USEREVENT + 2
CURRENT_CYCLE_VERT_EVENT = pygame.USEREVENT + 3
CURRENT_CYCLE_XFER_EVENT = pygame.USEREVENT + 4


def handle_event(event: pygame.event.Event) -> None:

    if event.type == pygame.QUIT:
        pygame.quit()
        exit()

    elif event.type == pygame.KEYDOWN:
        handle_input(event=event)

    elif buffer.autorun and buffer.logic == 0:
        if event.type == HORIZ_CYCLE_EVENT:
            buffer.horizontal_cycle()
        if event.type == VERT_CYCLE_EVENT:
            buffer.vertical_cycle()

    elif buffer.autorun and buffer.logic != 0:
        if event.type == CURRENT_CYCLE_CONV_EVENT:
            buffer.current_cycle_conv()
        if event.type == CURRENT_CYCLE_VERT_EVENT:
            buffer.current_cycle_vert()
        if event.type == CURRENT_CYCLE_XFER_EVENT:
            buffer.current_cycle_xfer()


def handle_input(event: pygame.event.Event) -> None:

    MANUAL_CONTROLS = {
        pygame.K_u: buffer.index_conveyor,
        pygame.K_i: buffer.index_inlet,
        pygame.K_o: buffer.index_outlet,
        pygame.K_p: buffer.transfer_push,
        pygame.K_LEFTBRACKET: buffer.move_xfer_down,
        pygame.K_RIGHTBRACKET: buffer.move_xfer_up
    }

    # this calls the manual_control method which checks if autorun is active,
    # if not then it executes the passed command
    if event.key in MANUAL_CONTROLS.keys():
        buffer.manual_control(MANUAL_CONTROLS[event.key])

    LOGIC_CONTROLS = {
        pygame.K_0,
        pygame.K_1,
        pygame.K_2,
        pygame.K_3
    }

    if event.key in LOGIC_CONTROLS:
        buffer.set_logic(int(event.unicode))
        reset_timers(buffer.cycle_time)

    AUTO_CONTROLS = {
        pygame.K_a: buffer.toggle_autorun,
        pygame.K_d: buffer.toggle_downstream,
        pygame.K_f: buffer.toggle_upstream,
        pygame.K_r: buffer.reset_buffer,
        pygame.K_q: buffer.quit,
        pygame.K_e: speed_up,
        pygame.K_w: speed_down
    }

    if event.key in AUTO_CONTROLS.keys():
        AUTO_CONTROLS[event.key]()


def speed_up() -> None:
    if buffer.cycle_time > 20:
        buffer.speed *= 2
        reset_timers(buffer.cycle_time)


def speed_down() -> None:
    if buffer.cycle_time < 6000:
        buffer.speed /= 2
        reset_timers(buffer.cycle_time)


def reset_timers(cycle_time: int) -> None:
    # current logic
    if buffer.logic != 0:
        pygame.time.set_timer(HORIZ_CYCLE_EVENT, 0)
        pygame.time.set_timer(VERT_CYCLE_EVENT, 0)

        pygame.time.set_timer(CURRENT_CYCLE_CONV_EVENT, cycle_time)
        pygame.time.delay(int(cycle_time / 3))
        pygame.time.set_timer(CURRENT_CYCLE_VERT_EVENT, cycle_time)
        pygame.time.delay(int(cycle_time / 3))
        pygame.time.set_timer(CURRENT_CYCLE_XFER_EVENT, cycle_time)

    # new logic
    if buffer.logic == 0:
        pygame.time.set_timer(CURRENT_CYCLE_CONV_EVENT, 0)
        pygame.time.set_timer(CURRENT_CYCLE_VERT_EVENT, 0)
        pygame.time.set_timer(CURRENT_CYCLE_XFER_EVENT, 0)

        pygame.time.set_timer(HORIZ_CYCLE_EVENT, cycle_time)
        pygame.time.delay(int(cycle_time / 2))
        pygame.time.set_timer(VERT_CYCLE_EVENT, cycle_time)
