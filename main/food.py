import pygame
import source as src
import random

class Food():
    def __init__(self, x: float, y: float)->None:
        self.x = x
        self.y = y
        self.energy = random.choices([1, 2, 3], [0.8, 0.15, 0.05])[0]

    def display(self, window: pygame.Surface)->None:
        pygame.draw.circle(window, src.FOOD_COLOR[self.energy - 1], (int(self.x), int(self.y)), src.foodSize)