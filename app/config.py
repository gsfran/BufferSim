
import pygame


pygame.init()

# screen size
(SCREEN_WIDTH, SCREEN_HEIGHT) = (2560, 1440)
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# window caption
pygame.display.set_caption("BufferSim")

# simulation frames rendered per second
FPS = 144
