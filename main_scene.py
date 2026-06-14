from minigame_scene import MiniGameScene
from tutorial_scene import TutorialScene


import pygame
import pytmx
import pyscroll
from collections import defaultdict

from scene import Scene
from ending_scene import EndingScene
from minigame_scene import MiniGameScene

DOWN = "down"
UP = "up"
LEFT = "left"
RIGHT = "right"
IDLE = "idle"
WALK_1 = "walk_1"  
WALK_2 = "walk_2"
PLAYER_SPRITESHEET_SIZE = 36
PLAYER_MAP_SIZE = 16           # displayed sprite size in map-pixel coords (one tile)
PLAYER_COLLISION_SIZE = 4      # slightly smaller for forgiving collisions

class Sprite(pygame.sprite.Sprite):
    """
    Simple Sprite class for on-screen things
    
    """
    def __init__(self, surface, rect) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.image = surface
        self.rect = rect

def draw_map(screen, map_data, player_sprite, player_rect):
    # Make the scrolling layer
    screen_size = (1280, 720)
    map_layer = pyscroll.BufferedRenderer(map_data, screen_size, zoom=3)

    # make the PyGame SpriteGroup with a scrolling map
    group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)

    display_rect = player_sprite.get_rect(center=player_rect.center)
    group.add(Sprite(player_sprite, display_rect))

    # Center the layer and sprites on a sprite
    group.center(player_rect.center)

    # Draw the layer
    group.draw(screen)


def build_wall_rects_from_layer(tmx_data, layer_name):
    """Build collision rectangles from non-zero tiles in a TMX layer."""
    layer = None
    for l in tmx_data.visible_layers:
        if hasattr(l, 'data') and l.name == layer_name:
            layer = l
            break
    if layer is None:
        return []

    tw = tmx_data.tilewidth
    th = tmx_data.tileheight
    rects = []
    for y in range(tmx_data.height):
        for x in range(tmx_data.width):
            gid = layer.data[y][x]
            if gid != 0:
                rects.append(pygame.Rect(x * tw, y * th, tw, th))
    return rects

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
                frame = self.player_spritesheet_img.subsurface(pygame.Rect(PLAYER_SPRITESHEET_SIZE*x, PLAYER_SPRITESHEET_SIZE*y, PLAYER_SPRITESHEET_SIZE, PLAYER_SPRITESHEET_SIZE))
                self.player_sprites[y_names[y]][x_names[x]] = pygame.transform.scale(frame, (PLAYER_MAP_SIZE, PLAYER_MAP_SIZE))

        # --- Load TMX Map ---
        tmx_data = pytmx.load_pygame("map/thin_hedges.tmx")
        # Make data source for the map
        self.map_data = pyscroll.TiledMapData(tmx_data)

        # Build collision rects from the "Lake and Hedges" layer
        self.wall_rects = build_wall_rects_from_layer(tmx_data, "Lake and Hedges")

        # Player rect in map-pixel coordinates (start in a walkable area)
        self.player_rect = pygame.Rect(
            3 * tmx_data.tilewidth,
            15 * tmx_data.tileheight,
            PLAYER_COLLISION_SIZE,
            PLAYER_COLLISION_SIZE,
        )

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
            self.player_rect.y -= 300 * dt
            moving = True
            self.last_player_direction = UP
            if collidelist := self.player_rect.collidelistall(self.wall_rects):
                self.player_rect.top = self.wall_rects[collidelist[0]].bottom
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player_rect.y += 300 * dt
            moving = True
            self.last_player_direction = DOWN
            if collidelist := self.player_rect.collidelistall(self.wall_rects):
                self.player_rect.bottom = self.wall_rects[collidelist[0]].top
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_rect.x -= 300 * dt
            moving = True
            self.last_player_direction = LEFT
            if collidelist := self.player_rect.collidelistall(self.wall_rects):
                self.player_rect.left = self.wall_rects[collidelist[0]].right
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_rect.x += 300 * dt
            moving = True
            self.last_player_direction = RIGHT
            if collidelist := self.player_rect.collidelistall(self.wall_rects):
                self.player_rect.right = self.wall_rects[collidelist[0]].left
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

        draw_map(screen, self.map_data, self.player_sprites[self.last_player_direction][self.player_position], self.player_rect)

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