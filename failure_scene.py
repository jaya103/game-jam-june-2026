import pygame

from scene import Scene


class FailureScene(Scene):
    def __init__(self, main_scene=None):
        super().__init__()
        self.name = "Failure Scene"
        self.main_scene = main_scene
        self.enter_was_down = True  # require a fresh press to dismiss
        self.failure_image = pygame.image.load("img/failure.png").convert()

    def render(self, screen, dt):
        # Blit the failure image, scaled to fit the screen width
        img_rect = self.failure_image.get_rect()
        scale = screen.get_width() / img_rect.width
        scaled_size = (int(img_rect.width * scale), int(img_rect.height * scale))
        scaled_image = pygame.transform.smoothscale(self.failure_image, scaled_size)
        scaled_rect = scaled_image.get_rect(center=screen.get_rect().center)
        screen.blit(scaled_image, scaled_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return None

        enter_pressed = keys[pygame.K_RETURN]
        if enter_pressed and not self.enter_was_down:
            return self.main_scene
        self.enter_was_down = enter_pressed

        return self
