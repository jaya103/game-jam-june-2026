from minigame_scene import MiniGameScene
import pygame
from collections import defaultdict

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
TILE_SIZE = 36
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

DOWN = "down"
UP = "up"
LEFT = "left"
RIGHT = "right"
IDLE = "idle"
WALK_1 = "walk_1"  
WALK_2 = "walk_2"
PLAYER_SPRITESHEET_SIZE = 36

class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.name = "Main Scene"
        self.score = 0
        self.start_ticks = pygame.time.get_ticks()
        self.player_spritesheet_img = pygame.image.load("img/GroundHog.png").convert_alpha()
        self.player_sprites = defaultdict(dict)
        self.last_player_direction = DOWN
        self.player_position = IDLE
        self.player_walk_cycle_secs = 0.3
        self.player_time_moving = 0
        y_names = {0: DOWN, 1: LEFT, 2: RIGHT, 3: UP}
        x_names = {0: IDLE, 1: WALK_1, 2: WALK_2}
        for y in range(4):
            for x in range(3):
                self.player_sprites[y_names[y]][x_names[x]] = self.player_spritesheet_img.subsurface(pygame.Rect(PLAYER_SPRITESHEET_SIZE*x, PLAYER_SPRITESHEET_SIZE*y, PLAYER_SPRITESHEET_SIZE, PLAYER_SPRITESHEET_SIZE))

    def render(self, screen, dt):
        screen.fill("purple")

        font = pygame.font.Font(None, 48)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10)) 

        seconds = (pygame.time.get_ticks() - self.start_ticks)/1000
        if seconds > 20: 
            return EndingScene()
        
        timer_text = font.render(f'Seconds: {seconds}', True, (200, 255, 255))
        screen.blit(timer_text, (10, 50))
        
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_rect.y -= 300 * dt
            moving = True
            self.last_player_direction = UP
            if collidelist := player_rect.collidelistall(wall_rects):
                player_rect.top = wall_rects[collidelist[0]].bottom
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_rect.y += 300 * dt
            moving = True
            self.last_player_direction = DOWN
            if collidelist := player_rect.collidelistall(wall_rects):
                player_rect.bottom = wall_rects[collidelist[0]].top
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_rect.x -= 300 * dt
            moving = True
            self.last_player_direction = LEFT
            if collidelist := player_rect.collidelistall(wall_rects):
                player_rect.left = wall_rects[collidelist[0]].right
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_rect.x += 300 * dt
            moving = True
            self.last_player_direction = RIGHT
            if collidelist := player_rect.collidelistall(wall_rects):
                player_rect.right = wall_rects[collidelist[0]].left
        else:
            self.player_time_moving = 0
            self.player_position = IDLE

        if moving:
            self.player_time_moving += dt
            if self.player_time_moving % self.player_walk_cycle_secs < self.player_walk_cycle_secs / 2:
                self.player_position = WALK_1
            else:
                self.player_position = WALK_2

        if keys[pygame.K_ESCAPE]:
            return None
        if keys[pygame.K_SPACE]:
            return MiniGameScene(self)

        for tile in wall_rects:
            pygame.draw.rect(screen, (100, 100, 100), tile)
        screen.blit(self.player_sprites[self.last_player_direction][self.player_position], player_rect)

        return self