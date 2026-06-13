from minigame_scene import MiniGameScene
from tutorial_scene import TutorialScene
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
        self.show_minigame_popup = False
        self.space_was_down = False
        self.mouse_was_down = True
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
        if seconds > 100: 
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
        space_pressed = keys[pygame.K_SPACE]
        if space_pressed and not self.space_was_down:
            self.space_was_down = True
            return MiniGameScene(self)
        self.space_was_down = space_pressed

        for tile in wall_rects:
            pygame.draw.rect(screen, (100, 100, 100), tile)
        screen.blit(self.player_sprites[self.last_player_direction][self.player_position], player_rect)

        # Minigame popup: shown after the tutorial has been dismissed.
        if self.show_minigame_popup:
            popup_w, popup_h = 360, 140
            popup_x = screen.get_width() - popup_w - 20
            popup_y = 20
            popup_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)
            pygame.draw.rect(screen, (30, 30, 30), popup_rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), popup_rect, width=2, border_radius=8)

            popup_font = pygame.font.Font(None, 32)
            line1 = popup_font.render("Ready for the minigame?", True, "white")
            screen.blit(line1, (popup_x + (popup_w - line1.get_width()) // 2, popup_y + 16))

            btn_w, btn_h = 200, 56
            btn_rect = pygame.Rect(
                popup_x + (popup_w - btn_w) // 2,
                popup_y + popup_h - btn_h - 16,
                btn_w, btn_h,
            )
            mouse_pos = pygame.mouse.get_pos()
            hovering = btn_rect.collidepoint(mouse_pos)
            btn_color = (90, 160, 90) if hovering else (60, 120, 60)
            pygame.draw.rect(screen, btn_color, btn_rect, border_radius=6)
            pygame.draw.rect(screen, "white", btn_rect, width=2, border_radius=6)
            btn_label = popup_font.render("Start Minigame", True, "white")
            screen.blit(btn_label, (
                btn_rect.x + (btn_w - btn_label.get_width()) // 2,
                btn_rect.y + (btn_h - btn_label.get_height()) // 2,
            ))

            mouse_down = pygame.mouse.get_pressed()[0]
            clicked = mouse_down and not self.mouse_was_down
            self.mouse_was_down = mouse_down
            if clicked and hovering:
                self.show_minigame_popup = False
                return TutorialScene(self)

        return self