import pygame

from app.buffer import (BufferSystem, HORIZ_CYCLE_EVENT,
                        VERT_CYCLE_EVENT)


def handle_event(buffer: BufferSystem, event: pygame.event.Event) -> None:

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            buffer.index_conveyor()
        if event.key == pygame.K_d:
            buffer.index_inlet()
        if event.key == pygame.K_a:
            buffer.index_outlet()
        if event.key == pygame.K_LEFT:
            buffer.transfer_push()
        if event.key == pygame.K_UP:
            buffer.move_xfer_up()
        if event.key == pygame.K_DOWN:
            buffer.move_xfer_down()
        if event.key == pygame.K_p:
            buffer.toggle_autocycle()
        if event.key == pygame.K_f:
            buffer.toggle_fault()

    if event.type == HORIZ_CYCLE_EVENT and buffer.auto_cycle:
        buffer.horizontal_cycle()

    if event.type == VERT_CYCLE_EVENT and buffer.auto_cycle:
        buffer.vertical_cycle()
