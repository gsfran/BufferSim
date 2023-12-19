from datetime import datetime as dt

import pygame

from app.buffer import (CURRENT_CYCLE_EVENT, HORIZ_CYCLE_EVENT,
                        VERT_CYCLE_EVENT, BufferSystem)


def handle_event(buffer: BufferSystem, event: pygame.event.Event) -> None:

    if event.type == pygame.KEYDOWN:
        handle_input(buffer=buffer, event=event)

    elif buffer.autorun and buffer.new_logic:
        if event.type == HORIZ_CYCLE_EVENT:
            print(f'{dt.now()} Horizontal Cycle')
            buffer.horizontal_cycle()

        if event.type == VERT_CYCLE_EVENT:
            print(f'{dt.now()} Vertical Cycle')
            buffer.vertical_cycle()

    elif buffer.autorun and not buffer.new_logic:
        if event.type == CURRENT_CYCLE_EVENT:
            print(f'{dt.now()} Current Cycle')
            buffer.old_cycle()


def handle_input(buffer: BufferSystem, event: pygame.event.Event) -> None:

    INPUT_DICT = {
        pygame.K_u: buffer.index_conveyor,
        pygame.K_i: buffer.index_inlet,
        pygame.K_o: buffer.index_outlet,
        pygame.K_p: buffer.transfer_push,
        pygame.K_LEFTBRACKET: buffer.move_xfer_up,
        pygame.K_RIGHTBRACKET: buffer.move_xfer_down,
        pygame.K_a: buffer.toggle_autorun,
        pygame.K_s: buffer.toggle_newlogic,
        pygame.K_d: buffer.toggle_downstream,
        pygame.K_f: buffer.toggle_upstream,
        pygame.K_r: buffer.reset,
        pygame.K_q: buffer.quit
    }

    if event.key in INPUT_DICT.keys():
        INPUT_DICT[event.key]()
