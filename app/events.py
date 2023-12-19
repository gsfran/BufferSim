from datetime import datetime as dt

import pygame

from app.buffer import (CURRENT_CYCLE_EVENT, HORIZ_CYCLE_EVENT,
                        VERT_CYCLE_EVENT, BufferSystem)


def handle_event(buffer: BufferSystem, event: pygame.event.Event) -> None:

    if event.type == pygame.KEYDOWN:
        handle_input(buffer=buffer, event=event)

    elif buffer.auto_cycle and buffer.new_cycle:
        if event.type == HORIZ_CYCLE_EVENT:
            print(f'{dt.now()} Horizontal Cycle')
            buffer.horizontal_cycle()

        if event.type == VERT_CYCLE_EVENT:
            print(f'{dt.now()} Vertical Cycle')
            buffer.vertical_cycle()

    elif buffer.auto_cycle and not buffer.new_cycle:
        if event.type == CURRENT_CYCLE_EVENT:
            print(f'{dt.now()} Current Cycle')
            buffer.old_cycle()


def handle_input(buffer: BufferSystem, event: pygame.event.Event) -> None:

    INPUT_DICT = {
        pygame.K_SPACE: buffer.index_conveyor,
        pygame.K_d: buffer.index_inlet,
        pygame.K_a: buffer.index_outlet,
        pygame.K_LEFT: buffer.transfer_push,
        pygame.K_UP: buffer.move_xfer_up,
        pygame.K_DOWN: buffer.move_xfer_down,
        pygame.K_p: buffer.toggle_autocycle,
        pygame.K_n: buffer.toggle_newcycle,
        pygame.K_f: buffer.toggle_fault,
        pygame.K_r: buffer.reset
    }

    if event.key in INPUT_DICT.keys():
        INPUT_DICT[event.key]()
