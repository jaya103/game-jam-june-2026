# Example file showing a basic pygame "game loop"
import pygame
from events import handle_events

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
running = True
dt = 0


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    handle_events()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)

    player_x = max(0, min(player_x, 1280 - 40))
    player_y = max(0, min(player_y, 720 - 40))  


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    if keys[pygame.K_ESCAPE]:
        running = False

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()