import pygame
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False