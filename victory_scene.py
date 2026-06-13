import pygame

from scene import Scene


class VictoryScene(Scene):
    def __init__(self, main_scene=None):
        super().__init__()
        self.name = "Victory Scene"
        self.main_scene = main_scene
        self.enter_was_down = True  # require a fresh press to dismiss

    def render(self, screen, dt):
        screen.fill((20, 40, 20))

        title_font = pygame.font.Font(None, 140)
        title = title_font.render("VICTORY!", True, (255, 230, 120))
        screen.blit(title, (
            screen.get_width() // 2 - title.get_width() // 2,
            screen.get_height() // 2 - title.get_height() - 20,
        ))

        sub_font = pygame.font.Font(None, 48)
        sub = sub_font.render("You woke up the bear!", True, "white")
        screen.blit(sub, (
            screen.get_width() // 2 - sub.get_width() // 2,
            screen.get_height() // 2 + 20,
        ))

        prompt_font = pygame.font.Font(None, 36)
        prompt = prompt_font.render("Press Enter to continue, Esc to quit", True, (200, 200, 200))
        screen.blit(prompt, (
            screen.get_width() // 2 - prompt.get_width() // 2,
            screen.get_height() - 80,
        ))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return None

        enter_pressed = keys[pygame.K_RETURN]
        if enter_pressed and not self.enter_was_down:
            if self.main_scene is not None:
                self.main_scene.score += 1
            return self.main_scene
        self.enter_was_down = enter_pressed

        return self
