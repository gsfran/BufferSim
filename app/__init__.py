import pygame

from .buffer_system import BufferSystem  # noqa
from .components import (  # noqa
    VertConveyor, HorizConveyor, TransferCarriage
)

pygame.init()

(SCREEN_WIDTH, SCREEN_HEIGHT) = (800, 600)
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BufferSim")

BACKGROUND = (10, 90, 190)
