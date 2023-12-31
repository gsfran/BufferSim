
import pygame

pygame.init()

# screen size
(SCREEN_WIDTH, SCREEN_HEIGHT) = (1920, 1080)
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# window caption
pygame.display.set_caption("BufferSim")

# simulation frames rendered per second
FPS = 144

# indexing conveyor capacity (scales object widths)
HORIZ_CONV_CAPACITY = 16

# total capacity of the buffer tower
BUFFER_CAPACITY = 150
