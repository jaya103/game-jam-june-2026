# Example file showing a basic pygame "game loop"
import pygame
from events import handle_events

# pygame setup!
pygame.init()
pygame.display.set_caption("The Great Bearwakening")
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
current_screen = None
score = 0
score_increment = 10
start_ticks = 0
font = pygame.font.Font(None, 36)

def starting_menu(screen, dt):
    global current_screen, running, start_ticks
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
        start_ticks = pygame.time.get_ticks()
        current_screen = main_game
    if keys[pygame.K_ESCAPE]:
        running = False
    
    return True

def ending_screen(screen, dt):
    global current_screen, running
    screen.fill("black")
    font = pygame.font.Font(None, 100)
    text = font.render("Game Over", True, "white")
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 100))
    screen.blit(text, text_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        running = False
    
    return True

level = [
    ".....................",
    ".....................",
    ".....................",
    "WWWWWWWWWWWWWWWWWWWWW",
    "W...................W",
    "W......WWWWWW...PWWWW",
    "W...........WWWWWW..W",
    "WWWWWWWWW........WW.W",
    "W...................W",
    "WWWWWWWWWWWWWWWWWWWWW"
]
TILE_SIZE = 50
def build_level(level_data):
    tiles = []
    for y, row in enumerate(level_data):
        for x, tile in enumerate(row):
            if tile == "W":
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                tiles.append(rect)
            if tile == "P":
                player_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    return tiles, player_rect
wall_rects, player_rect = build_level(level)

def main_game(screen, dt):
    global running
    global current_screen
    global score, start_ticks
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    font = pygame.font.Font(None, 48)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10)) 

    seconds = (pygame.time.get_ticks() - start_ticks)/1000
    if seconds > 100: 
        current_screen = ending_screen
    
    timer_text = font.render(f'Seconds: {seconds}', True, (200, 255, 255))
    screen.blit(timer_text, (10, 50))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_rect.y -= 300 * dt
        if collidelist := player_rect.collidelistall(wall_rects):
            player_rect.top = wall_rects[collidelist[0]].bottom
    if keys[pygame.K_s]:
        player_rect.y += 300 * dt
        if collidelist := player_rect.collidelistall(wall_rects):
            player_rect.bottom = wall_rects[collidelist[0]].top
    if keys[pygame.K_a]:
        player_rect.x -= 300 * dt
        if collidelist := player_rect.collidelistall(wall_rects):
            player_rect.left = wall_rects[collidelist[0]].right
    if keys[pygame.K_d]:
        player_rect.x += 300 * dt
        if collidelist := player_rect.collidelistall(wall_rects):
            player_rect.right = wall_rects[collidelist[0]].left
    if keys[pygame.K_ESCAPE]:
        running = False

    for tile in wall_rects:
        pygame.draw.rect(screen, (100, 100, 100), tile)    
    pygame.draw.rect(screen, (0, 255, 0), player_rect)

current_screen = starting_menu
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    handle_events()

    current_screen(screen, dt)
 
    # flip() the display to put your work on screen
    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()