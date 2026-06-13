import pygame
import argparse
from events import handle_events
from starting_scene import StartingScene
from ending_scene import EndingScene
from main_scene import MainScene
from minigame_scene import MiniGameScene

pygame.init()
pygame.display.set_caption("The Great Bearwakening")
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0
current_screen = None
font = pygame.font.Font(None, 36)


parser = argparse.ArgumentParser(
                    prog='The Great Bearwakening',
                    description='Our game jam game')
parser.add_argument('-s', '--scene',
                    default='starting_scene')  # on/off flag
args = parser.parse_args()

scene_mapping = {
    'starting_scene': StartingScene,
    'main_scene': MainScene,
    'ending_scene': EndingScene,
    'minigame_scene': MiniGameScene
}

current_scene = scene_mapping.get(args.scene, StartingScene)()
while current_scene: 

    handle_events()

    current_scene = current_scene.render(screen, dt)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()