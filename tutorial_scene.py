import pygame
from scene import Scene
from text_utils import wrap_text


class TutorialScene(Scene):
    def __init__(self, main_scene):
        self.name = "Tutorial Scene"
        self.main_scene = main_scene
        self.x_was_down = True  # require a fresh press of X to dismiss

    def render(self, screen, dt):
        screen.fill((20, 20, 40))

        # Title
        title_font = pygame.font.Font(None, 96)
        title = title_font.render("MINIGAME TUTORIAL", True, "white")
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 40))

        # Body text - wrapped to fit screen width with padding
        body_font = pygame.font.Font(None, 40)
        tutorial_text = (
            "Welcome to the minigame! In this minigame, you need to control the "
            "player's bar to hover over the bears to wake them up. You can move "
            "the bar left and right using the A and D keys.\n"
            "You start at 10 points, and you lose 1 point every second, but you "
            "gain a point for every second you hover over a bear.\n"
            "You need to get 50 points to wake up the bear and get back to the "
            "main game. You can also press Esc to exit the minigame and return "
            "to the main game, but you won't get any points for that."
        )

        padding = 60
        max_width = screen.get_width() - padding * 2
        lines = wrap_text(tutorial_text, body_font, max_width)

        line_spacing = body_font.get_linesize()
        total_height = line_spacing * len(lines)
        start_y = (screen.get_height() - total_height) // 2

        for i, line in enumerate(lines):
            if not line:
                continue
            rendered = body_font.render(line, True, "white")
            rect = rendered.get_rect(center=(screen.get_width() // 2, start_y + i * line_spacing))
            screen.blit(rendered, rect)

        # Footer prompt
        prompt_font = pygame.font.Font(None, 36)
        prompt = prompt_font.render("Press X to start the minigame", True, (200, 200, 120))
        screen.blit(prompt, (screen.get_width() // 2 - prompt.get_width() // 2,
                             screen.get_height() - 60))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return self.main_scene

        if keys[pygame.K_x] and not self.x_was_down:
            from minigame_scene import MiniGameScene  # deferred to avoid circular import
            return MiniGameScene(self.main_scene)
        self.x_was_down = keys[pygame.K_x]

        return self
