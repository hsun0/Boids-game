import pygame
import source as src
import random
import math

class Food():
    def __init__(self, x: float, y: float)->None:
        self.x = x
        self.y = y
        self.energy = random.choices([1, 2, 3], [0.8, 0.15, 0.05])[0]

    def display(self, window: pygame.Surface)->None:
        pygame.draw.circle(window, src.FOOD_COLOR[self.energy - 1], (int(self.x), int(self.y)), src.foodSize)
    
    def is_food_collide_obstacle(food_x: float, food_y: float, obstacles: list) -> bool:
        for obstacle in obstacles:
            dx = food_x - obstacle.x
            dy = food_y - obstacle.y
            if math.sqrt(dx*dx + dy*dy) < src.obstacleRadius * 1.2:
                return True
        return False