import pygame
from scene import Scene

class MiniGameScene(Scene):
    def __init__(self, main_scene=None):
        self.name = "Mini Game Scene"
        self.main_scene = main_scene

    def render(self, screen, dt):
        global score, current_screen
        global current_screen, running, start_ticks


        screen.fill("black")
        font = pygame.font.Font(None, 100)
        minigametext = font.render("MINIGAME", True, "white")
        screen.blit(minigametext, ([screen.get_width() // 2 - minigametext.get_width() // 2, 50]))

        font = pygame.font.Font(None, 40)
        title_text = """Welcome to the minigame! In this minigame, you need to control the player's bar
        to hover over the bears to wake them up. You can move the bar left and right using the A and D keys. 
        You start at 10 points, and you lose 1 point every second, but you gain a point for every second you hover over a bear. 
        You need to get 50 points to wake up the bear and get back to the main game. You can also press Esc to exit
        the minigame and return to the main game, but you won't get any points for that.
    """
        title_vertical_offset = 0
        for line in title_text.splitlines():
            text = font.render(line, True, "black")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100 + title_vertical_offset))
            screen.blit(text, text_rect)
            title_vertical_offset += 30

        pygame.draw.rect(screen, (0, 255, 255), #CHANGES THE COLOR OF THE RECTANGLE
                 [screen.get_width() // 2 - screen.get_width() // 4, screen.get_height() // 2 - 100, screen.get_width() // 2, 200]) # CHANGES THE SIZE AND POSITION OF THE RECTANGLE
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            start_ticks = pygame.time.get_ticks()
            return self.main_scene

        if keys[pygame.K_ESCAPE]:
            return None
        
        return self
