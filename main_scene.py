import pygame

from scene import Scene
from ending_scene import EndingScene

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

class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "Main Scene"
        self.score = 0
        self.start_ticks = pygame.time.get_ticks()

    def render(self, screen, dt):
        screen.fill("purple")

        font = pygame.font.Font(None, 48)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10)) 

        seconds = (pygame.time.get_ticks() - self.start_ticks)/1000
        if seconds > 10: 
            return EndingScene()
        
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
            return None

        for tile in wall_rects:
            pygame.draw.rect(screen, (100, 100, 100), tile)    
        pygame.draw.rect(screen, (0, 255, 0), player_rect)

        return self