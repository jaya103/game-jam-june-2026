import pygame
from scene import Scene
from main_scene import MainScene

class StartingScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "Starting Scene"

    def render(self, screen, dt):
        background = pygame.image.load("img/Start_Menu_Background.png").convert()
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
        imagerect = background.get_rect()
        screen.blit(background, imagerect)

        # Draw title text, dropshadow first
        font = pygame.font.Font(None, 100)
        shadow_text = font.render("The Great Bearwakening", True, "grey")
        text_rect = shadow_text.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(shadow_text, text_rect)
        text = font.render("The Great Bearwakening", True, "white")
        text_rect.left -= 4
        text_rect.top -= 4
        screen.blit(text, text_rect)

        # Create a background semi-transparent surface for the center text
        # Can't use "draw" functions for alpha - have to create a separate surface, draw on it, then blit it onto the main screen
        background_rect = pygame.Rect(20, 220, screen.get_width()*.97, 200)
        shape_surf = pygame.Surface(pygame.Rect(background_rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, (128, 128, 128, 168), shape_surf.get_rect())
        screen.blit(shape_surf, background_rect)

        # Main game text
        font = pygame.font.Font(None, 40)
        title_text = """Welcome to the Great Bear Awakening! It’s the start of spring, and as the first one to awake
    as a groundhog, you have to wake up all the bears from their winter hibernation to gather all
    the forest animals for a spring feast to kick off spring. Your goal is to wake up at
    least 10 bears before the time runs out to make the meal a success.
    Use the W-A-S-D keys to move and Esc to exit the game.
    """
        title_vertical_offset = 0
        for line in title_text.splitlines():
            text = font.render(line.strip(), True, "white")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100 + title_vertical_offset))
            screen.blit(text, text_rect)
            title_vertical_offset += 30

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return MainScene()
        if keys[pygame.K_ESCAPE]:
            return None
        
        return self