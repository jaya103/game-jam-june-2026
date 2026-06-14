import pygame
from scene import Scene
from text_utils import wrap_text
from victory_scene import VictoryScene
from failure_scene import FailureScene
import time
import random

from utils import get_main_font

class MiniGameScene(Scene):
    def __init__(self, main_scene=None):
        self.name = "Mini Game Scene"
        self.main_scene = main_scene
        self.score = 0
        self.capture_bar_position = 0
        self.acceleration = 0
        self.velocity = 0

        self.bear_position = None  # set on first render once bar_width is known
        self.bear_velocity = 0
        self.bear_acceleration = 0
        self.bear_target_direction = 1  # -1 left, 0 paused, 1 right
        self.bear_change_timer = 0

        # Progress tracker (0..100). Stay on the bear to fill it; falls off otherwise.
        self.progress = 0.0
        self.progress_gain_per_sec = 30.0   # how fast you fill while hovering
        self.progress_loss_per_sec = 18.0   # how fast you lose while off the bear

        # Score drain: the main scene score ticks down once per second once the
        # player first touches the bear.  Reaching 0 = failure.
        self.score_drain_timer = 0.0
        self.score_drain_active = False
        self.score_drain_grace = 5.0  # seconds before drain starts after first bear contact
        self.score_drain_grace_started = False

        # Bear doesn't move until the player starts moving.
        self.player_started = False

        
    def render(self, screen, dt):
        global score, current_screen
        global current_screen, running, start_ticks


        screen.fill("black")
        font = get_main_font(100)
        minigametext = font.render("MINIGAME", True, "white")
        screen.blit(minigametext, ([screen.get_width() // 2 - minigametext.get_width() // 2, 50]))

        bear_width, bear_height = 60, 60
        cursor_width, cursor_height = 110, 90
        bar_width = screen.get_width()
        bar_height = 100
        bar_x = 0
        bar_y = screen.get_height() // 2 + 100

        if self.bear_position is None:
            self.bear_position = (bar_width - bear_width) / 2

        # Bear only moves once the player has started.
        if self.player_started:
            self.bear_change_timer -= dt

            if self.bear_change_timer <= 0:
                # Roughly 1-in-3 chance to pause for a beat, otherwise pick a direction.
                roll = random.random()
                if roll < 0.33:
                    self.bear_target_direction = 0
                    self.bear_change_timer = random.uniform(0.6, 1.4)
                else:
                    self.bear_target_direction = random.choice([-1, 1])
                    self.bear_change_timer = random.uniform(1.2, 2.6)

            # Apply acceleration toward target direction (0 = drift to a stop).
            bear_accel_strength = 0.45
            self.bear_acceleration = self.bear_target_direction * bear_accel_strength

            if self.bear_target_direction == 0:
                # Friction when paused so the bear actually slows and rests.
                self.bear_velocity *= 0.9
                if abs(self.bear_velocity) < 0.05:
                    self.bear_velocity = 0
            else:
                self.bear_velocity += self.bear_acceleration

            # Clamp max velocity
            max_bear_speed = 3.5
            if self.bear_velocity > max_bear_speed:
                self.bear_velocity = max_bear_speed
            elif self.bear_velocity < -max_bear_speed:
                self.bear_velocity = -max_bear_speed

            # Update position
            self.bear_position += self.bear_velocity

            # Boundary collision with bounce
            if self.bear_position > bar_width - bear_width:
                self.bear_position = bar_width - bear_width
                self.bear_velocity *= -0.6
                self.bear_target_direction = -1
            elif self.bear_position < 0:
                self.bear_position = 0
                self.bear_velocity *= -0.6
                self.bear_target_direction = 1

        pygame.draw.rect(screen, (0, 255, 255), #CHANGES THE COLOR OF THE RECTANGLE
                 [bar_x, bar_y, bar_width, bar_height]) # CHANGES THE SIZE AND POSITION OF THE RECTANGLE

        cursor_rect = pygame.Rect(
            bar_x + self.capture_bar_position,
            bar_y + (bar_height - cursor_height) // 2,
            cursor_width, cursor_height,
        )
        bear_x = bar_x + self.bear_position
        bear_y = bar_y + (bar_height // 2) - (bear_height // 2)
        bear_rect = pygame.Rect(bear_x, bear_y, bear_width, bear_height)

        hovering_bear = cursor_rect.colliderect(bear_rect)

        # Start the grace countdown the first time the cursor touches the bear.
        if hovering_bear and not self.score_drain_grace_started:
            self.score_drain_grace_started = True

        # Tick down the grace period, then activate the drain.
        if self.score_drain_grace_started and not self.score_drain_active:
            self.score_drain_grace -= dt
            if self.score_drain_grace <= 0:
                self.score_drain_active = True

        # Update progress based on whether the cursor is on the bear.
        if hovering_bear:
            self.progress += self.progress_gain_per_sec * dt
        else:
            self.progress -= self.progress_loss_per_sec * dt
        if self.progress < 0:
            self.progress = 0
        elif self.progress > 100:
            self.progress = 100

        cursor_color = (255, 215, 60) if hovering_bear else (172, 216, 39)
        pygame.draw.rect(screen, cursor_color, cursor_rect)
        pygame.draw.rect(screen, (139, 69, 19), bear_rect)

        # Progress bar below the gameplay bar.
        progress_bar_w = bar_width - 80
        progress_bar_h = 28
        progress_bar_x = bar_x + 40
        progress_bar_y = bar_y + bar_height + 24
        pygame.draw.rect(screen, (50, 50, 50),
                         [progress_bar_x, progress_bar_y, progress_bar_w, progress_bar_h])
        fill_w = int(progress_bar_w * (self.progress / 100))
        # Color shifts from red (low) to green (high) based on progress.
        fill_color = (
            int(220 * (1 - self.progress / 100) + 60 * (self.progress / 100)),
            int(60 * (1 - self.progress / 100) + 200 * (self.progress / 100)),
            60,
        )
        if fill_w > 0:
            pygame.draw.rect(screen, fill_color,
                             [progress_bar_x, progress_bar_y, fill_w, progress_bar_h])
        pygame.draw.rect(screen, (255, 255, 255),
                         [progress_bar_x, progress_bar_y, progress_bar_w, progress_bar_h], width=2)

     
        # Corner tutorial box (top-right) - quick reminder of the controls.
        corner_font = get_main_font(30)
        corner_title_font = get_main_font(36)
        corner_w = 360
        corner_padding = 14
        corner_x = screen.get_width() - corner_w - 12
        corner_y = 12
        corner_lines = wrap_text(
            "Hold Z to push the cursor right. "
            "Keep your cursor on the bear to fill the progress bar. "
            "Slip off and the progress drains. ",
            corner_font,
            corner_w - corner_padding * 2,
        )
        title_surf = corner_title_font.render("Tutorial", True, (255, 230, 120))
        line_h = corner_font.get_linesize()
        corner_h = corner_padding * 2 + title_surf.get_height() + 6 + line_h * len(corner_lines)
        corner_rect = pygame.Rect(corner_x, corner_y, corner_w, corner_h)
        pygame.draw.rect(screen, (20, 20, 20), corner_rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), corner_rect, width=2, border_radius=8)
        screen.blit(title_surf, (corner_x + corner_padding, corner_y + corner_padding))
        text_y = corner_y + corner_padding + title_surf.get_height() + 6
        for line in corner_lines:
            line_surf = corner_font.render(line, True, "white")
            screen.blit(line_surf, (corner_x + corner_padding, text_y))
            text_y += line_h

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            start_ticks = pygame.time.get_ticks()
            return self.main_scene
        
        if keys[pygame.K_z]:
            if not self.player_started:
                self.player_started = True
            self.acceleration += (2.5)
            if self.acceleration > 8:
                self.acceleration = 8
        else:
            self.acceleration -= (0.5)

        self.capture_bar_position += self.acceleration
        max_cursor_pos = screen.get_width() - cursor_width
        if self.capture_bar_position > max_cursor_pos: 
            self.capture_bar_position, self.acceleration = max_cursor_pos, -self.acceleration * 0.6
        if self.capture_bar_position < 0:
            self.capture_bar_position, self.acceleration = 0, -self.acceleration * 0.6

        # Drain the progress bar by 1 every second after first bear contact.
        if self.score_drain_active and self.progress is not None:
            self.score_drain_timer += dt
            while self.score_drain_timer >= 1.0:
                self.score_drain_timer -= 1.0
                self.progress -= 1
                if self.progress < 0:
                    self.progress = 0

        if keys[pygame.K_ESCAPE]:
            return None

        # Win condition: progress maxed out.
        if self.progress >= 100:
            return VictoryScene(self.main_scene)

        # Lose condition: progress hit 0 after drain started.
        if self.progress is not None and self.progress <= 0 and self.score_drain_active:
            return FailureScene(self.main_scene)

        return self
    
