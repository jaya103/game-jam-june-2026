import pygame

from scene import Scene
from utils import get_main_font

class EndingScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "Ending Scene"

    def render(self, screen, dt):
        screen.fill("black")
        font = get_main_font(72)
        text = font.render("Game Over", True, "white")
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100))
        screen.blit(text, text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_ESCAPE]:
            return None
        
        return self