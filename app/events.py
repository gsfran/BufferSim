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

    if event.type == VERT_CYCLE_EVENT and buffer.auto_cycle:
        print(f'{dt.now()} Vertical Cycle')
        buffer.vertical_cycle()
