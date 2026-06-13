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
        screen.fill("black")
        screen.blit(background, imagerect)
        font = pygame.font.Font(None, 100)
        text = font.render("The Great Bearwakening", True, "white")

        font = pygame.font.Font(None, 40)
        title_text = """Welcome to the Great Bear Awakening! It’s the start of spring, and as the first one to awake
    as a groundhog, you have to wake up all the bears from their winter hibernation to gather all
    the forest animals for a spring feast to kick off spring. Your goal is to wake up at
    least 10 bears before the time runs out to make the meal a success.
    Use the W-A-S-D keys to move and Esc to exit the game.
    """
        title_vertical_offset = 0
        for line in title_text.splitlines():
            text = font.render(line, True, "black")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100 + title_vertical_offset))
            screen.blit(text, text_rect)
            title_vertical_offset += 30

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return MainScene()
        if keys[pygame.K_ESCAPE]:
            return None
        
        return self