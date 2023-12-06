import pygame

from app.buffer import BufferSystem


def handle_event(buffer: BufferSystem, event: pygame.event) -> None:

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
