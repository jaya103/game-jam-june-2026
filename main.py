# Example file showing a basic pygame "game loop"
import pygame
from events import handle_events

# pygame setup
pygame.init()
pygame.display.set_caption("The Great Bearwakening")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
running = True
dt = 0
score = 0
score_increment = 10
start_ticks = pygame.time.get_ticks()
font = pygame.font.Font(None, 36)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    handle_events()
      
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10)) 

    seconds = (pygame.time.get_ticks() - start_ticks)/1000
    if seconds > 10: 
        break
    
    timer_text = font.render(f'Seconds: {seconds}', True, (200, 255, 255))
    screen.blit(timer_text, (10, 50))
    
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

    if player_pos.x < 40:
        player_pos.x = 40
    if player_pos.x > screen.get_width() - 40:
        player_pos.x = screen.get_width() - 40
    if player_pos.y < 40:
        player_pos.y = 40
    if player_pos.y > screen.get_height() - 40:
        player_pos.y = screen.get_height() - 40
    

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()