import pygame

from datetime import datetime as dt

from app.buffer import BufferSystem, HORIZ_CYCLE_EVENT, VERT_CYCLE_EVENT


def handle_event(buffer: BufferSystem, event: pygame.event.Event) -> None:

    if event.type == pygame.KEYDOWN:
        handle_input(buffer=buffer, event=event)

    elif buffer.auto_cycle:
        if event.type == HORIZ_CYCLE_EVENT:
            print(f'{dt.now()} Horizontal Cycle')
            buffer.horizontal_cycle()

        if event.type == VERT_CYCLE_EVENT:
            print(f'{dt.now()} Vertical Cycle')
            buffer.vertical_cycle()


def handle_input(buffer: BufferSystem, event: pygame.event.Event) -> None:

    INPUT_DICT = {
        pygame.K_SPACE: buffer.index_conveyor,
        pygame.K_d: buffer.index_inlet,
        pygame.K_a: buffer.index_outlet,
        pygame.K_LEFT: buffer.transfer_push,
        pygame.K_UP: buffer.move_xfer_up,
        pygame.K_DOWN: buffer.move_xfer_down,
        pygame.K_p: buffer.toggle_autocycle,
        pygame.K_f: buffer.toggle_fault
    }

    if event.key in INPUT_DICT.keys():
        INPUT_DICT[event.key]()
