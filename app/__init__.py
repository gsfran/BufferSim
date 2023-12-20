import pygame

from app.buffer_system import BufferSystem, TOTAL_CAPACITY


buffer = BufferSystem(capacity=TOTAL_CAPACITY)
clock = pygame.time.Clock()
