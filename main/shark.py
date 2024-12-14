import pygame
import source as src
import math

class Shark:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.radius = 10
    
    def generate_shark_points(self) -> list:
        # 生成不規則多邊形的頂點
        points = []
        num_points = 8
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points # 360度分成num_points份
            radius = self.radius * (0.8 + 0.4 * math.sin(3 * angle)) # 三角函數生成不規則多邊形
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        return points

    def display(self, window: pygame.Surface) -> None:
        point = self.generate_shark_points()
        pygame.draw.polygon(window, src.Colors['red'], point)