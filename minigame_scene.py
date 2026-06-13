import pygame
from scene import Scene
import time

class MiniGameScene(Scene):
    def __init__(self, main_scene=None):
        self.name = "Mini Game Scene"
        self.main_scene = main_scene
        self.score = 0
        self.capture_bar_position = 0
        self.acceleration = 0
        self.velocity = 0
        
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
        
        font = pygame.font.Font(None, 48)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10)) 

        
        title_vertical_offset = 0
        for line in title_text.splitlines():
            text = font.render(line.strip(), True, "white")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100 + title_vertical_offset))
            screen.blit(text, text_rect)
            title_vertical_offset += 30

        pygame.draw.rect(screen, (0, 255, 255), #CHANGES THE COLOR OF THE RECTANGLE
                 [screen.get_width() // 2 - 300, screen.get_height() // 2 + 100, 800, 100]) # CHANGES THE SIZE AND POSITION OF THE RECTANGLE
        
        pygame.draw.rect(screen, (172, 216, 39), #CHANGES THE COLOR OF THE CAPTURE BAR
                         [screen.get_width() // 2 - 300 + self.capture_bar_position, screen.get_height() // 2 + 110, 50, 80]) # CHANGES THE SIZE AND POSITION OF THE CAPTURE BAR
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            start_ticks = pygame.time.get_ticks()
            return self.main_scene
        
        if keys[pygame.K_z]:
            self.acceleration += (2.5)
            if self.acceleration > 8:
                self.acceleration = 8
        else:
            self.acceleration -= (0.5)

        self.capture_bar_position += self.acceleration
        if self.capture_bar_position > 750: 
            self.capture_bar_position, self.acceleration = 750, -self.acceleration * 0.6
        if self.capture_bar_position < 0:
            self.capture_bar_position, self.acceleration = 0, -self.acceleration * 0.6

        if keys[pygame.K_ESCAPE]:
            return None
        
        if keys[pygame.K_a]:
            self.score += 1

        return self
    
