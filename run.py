from sys import exit

import pygame

from app import FPS, WINDOW, SPEEDS
from app.buffer import HORIZ_CYCLE_EVENT, VERT_CYCLE_EVENT, BufferSystem
from app.colors import BG_COLOR
from app.events import handle_event


def main() -> None:

    clock = pygame.time.Clock()
    buffer = BufferSystem(136)

    pygame.time.set_timer(HORIZ_CYCLE_EVENT, int(buffer.cycle_time))
    pygame.time.delay(int(buffer.cycle_time / 2))
    pygame.time.set_timer(VERT_CYCLE_EVENT, int(buffer.cycle_time))

    running = True
    while running:

        WINDOW.fill(BG_COLOR)
        buffer.draw(WINDOW)
        pygame.display.update()
        dt = (clock.tick(FPS) / 1000 * buffer.speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            handle_event(buffer, event, dt)


    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
