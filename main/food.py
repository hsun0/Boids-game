import pygame
import source as src

class Food():
    def __init__(self, x: float, y: float)->None:
        self.x = x
        self.y = y

    def display(self, window: pygame.Surface)->None:
        pygame.draw.circle(window, src.Colors['lime'], (int(self.x), int(self.y)), 2)