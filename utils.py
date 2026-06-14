import pygame
from functools import cache

@cache
def get_main_font(size=36):
    return pygame.font.Font("font/Boiled Pasta.ttf", size)

@cache
def get_text_font(size=36):
    return pygame.font.Font(None, size)