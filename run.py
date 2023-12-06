import pygame

from app import FPS, WINDOW
from app.buffer import BufferSystem
from app.colors import BG_COLOR
from app.events import handle_event


def main() -> None:

    clock = pygame.time.Clock()
    buffer = BufferSystem(20)

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
