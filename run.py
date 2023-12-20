import pygame

from app import buffer, clock
from app.buffer_system import BASE_CYCLE_TIME
from app.colors import BG_COLOR
from app.config import FPS, WINDOW
from app.events import handle_event, reset_timers
from app.ui import ui


def main() -> None:

    reset_timers(BASE_CYCLE_TIME)

    while True:

        for event in pygame.event.get():
            print(event)
            handle_event(event)

        clock.tick(FPS)
        WINDOW.fill(BG_COLOR)
        buffer.draw(WINDOW)
        ui.draw(WINDOW)
        pygame.display.update()


if __name__ == '__main__':
    main()
