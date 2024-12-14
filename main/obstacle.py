import pygame
import source as src
import math

class Obstacle:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.radius = src.obstacleRadius
        self.points = self.generate_rock_points()
    
    def generate_rock_points(self) -> list:
        # 生成不規則多邊形的頂點
        points = []
        num_points = 8
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points # 360度分成num_points份
            radius = self.radius * (0.8 + 0.4 * math.sin(3 * angle)) #用波動公式生成不規則多邊形，GPT給的靈感 嘻嘻
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        return points
    
    def display(self, window: pygame.Surface) -> None:
        pygame.draw.polygon(window, src.obstacleColor, self.points)
        
    def repel_force(self, bird_x: float, bird_y: float) -> tuple:
        dx = bird_x - self.x
        dy = bird_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < self.radius * 2: # 鳥在障礙物的影響範圍內
            force = (self.radius * 2 - distance) / (self.radius * 2) # 距離越近，斥力越大
            return (dx/distance * force, dy/distance * force)
        return (0, 0)