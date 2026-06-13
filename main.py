# Example file showing a basic pygame "game loop"
import pygame
from events import handle_events

# pygame setup!
pygame.init()
pygame.display.set_caption("The Great Bearwakening")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
running = True
dt = 0
current_screen = None
score = 0
score_increment = 10
start_ticks = pygame.time.get_ticks()
font = pygame.font.Font(None, 36)

def main_menu(screen, dt):
    global current_screen
    font = pygame.font.Font(None, 100)
    text = font.render("The Great Bearwakening", True, "white")
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100))
    screen.blit(text, text_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        current_screen = main_game
    
    return True

def main_game(screen, dt):
    global running
    global current_screen
    global score, start_ticks
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)

    font = pygame.font.Font(None, 48)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10)) 

    seconds = (pygame.time.get_ticks() - start_ticks)/1000
    if seconds > 10: 
        score = 0
        start_ticks = pygame.time.get_ticks()
    
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
    return True

current_screen = main_menu
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    handle_events()

    current_screen(screen, dt)
 
    # flip() the display to put your work on screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()