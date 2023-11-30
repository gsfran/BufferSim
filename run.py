import pygame

from app import WINDOW, BACKGROUND
from app.buffer_system import BufferSystem


def main() -> None:
    run = True
    clock = pygame.time.Clock()

    buffer = BufferSystem(10)

    while run:

        clock.tick(60)
        WINDOW.fill(BACKGROUND)

        buffer.draw(WINDOW)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


    pygame.quit()


if __name__ == '__main__':
    main()
