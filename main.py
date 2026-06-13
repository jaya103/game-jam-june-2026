# Example file showing a basic pygame "game loop"
import pygame
from gameformini import minigame
from events import handle_events
from starting_scene import StartingScene

# pygame setup!
pygame.init()
pygame.display.set_caption("The Great Bearwakening")
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0
current_screen = None
font = pygame.font.Font(None, 36)

current_scene = StartingScene()
while current_scene:  # This will be None if the user pressed Esc
    # poll for events
    handle_events()

    current_scene = current_scene.render(screen, dt)

    # flip() the display to put your work on screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()