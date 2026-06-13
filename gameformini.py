import pygame
from scene import Scene

class MiniGame(Scene):
    def __init__(self, main_scene=None):
        self.name = "Undefined Scene"
        self.main_scene = main_scene

    def render(self, screen, dt):
        global score, current_screen
        global current_screen, running, start_ticks
        screen.fill("black")
        font = pygame.font.Font(None, 100)
        text = font.render("MINIGAME", True, "white")
        screen.blit(text, (10, 10)) 
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            start_ticks = pygame.time.get_ticks()
            return self.main_scene

        if keys[pygame.K_ESCAPE]:
            return None
        
        return self
