from sys import exit

import pygame

from app import FPS, WINDOW
from app.buffer import (CURRENT_CYCLE_EVENT, HORIZ_CYCLE_EVENT,
                        VERT_CYCLE_EVENT, BufferSystem)
from app.colors import BG_COLOR
from app.events import handle_event


def main() -> None:

    clock = pygame.time.Clock()
    buffer = BufferSystem(150)
    pygame.time.set_timer(CURRENT_CYCLE_EVENT, buffer.cycle_time)
    pygame.time.set_timer(HORIZ_CYCLE_EVENT, buffer.cycle_time)
    pygame.time.delay(int(buffer.cycle_time / 2))
    pygame.time.set_timer(VERT_CYCLE_EVENT, buffer.cycle_time)

    while True:

        clock.tick(FPS)

        WINDOW.fill(BG_COLOR)
        buffer.draw(WINDOW)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            handle_event(buffer, event)


if __name__ == '__main__':
    main()
