import pygame

pygame.init()

FPS = 60
(SCREEN_WIDTH, SCREEN_HEIGHT) = (1280, 720)
SPEEDS = [2 ** _ for _ in range(6)]
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("BufferSim")