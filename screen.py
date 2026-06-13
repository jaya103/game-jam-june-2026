import pygame

class Screen():
    def __init__(self, screen, fill="black"):
        self.screen = screen
        self.fill = fill

    def render(self):
        self.screen.fill(self.fill)
