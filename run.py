import pygame

from app import FPS, WINDOW
from app.buffer import BufferSystem, HORIZONTAL_CYCLE_EVENT
from app.colors import BG_COLOR
from app.events import handle_event


def main() -> None:

    clock = pygame.time.Clock()
    buffer = BufferSystem(40)
    pygame.time.set_timer(HORIZONTAL_CYCLE_EVENT, buffer.cycle_time)

    run = True
    while run:

        clock.tick(FPS)

        WINDOW.fill(BG_COLOR)

        buffer.draw(WINDOW)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            handle_event(buffer, event)

    pygame.quit()


if __name__ == '__main__':
    main()
