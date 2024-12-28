import pygame
import math
import source as src

class Shark:
    def __init__(self, x: float, y: float, windowSize: tuple) -> None:
        self.x = x
        self.y = y
        self.windowSize = windowSize
        self.imgPath = "img/shark.png"
        self.sharkImgs = {
            "up": None,
            "down": None,
            "left": None,
            "right": None,
            "upleft": None,
            "upright": None,
            "downleft": None,
            "downright": None
        }
        self.sharkImg = None
        self.load()
        self.radius = src.sharkRadius

    def load(self) -> None:
        originalShark = pygame.image.load(self.imgPath).convert_alpha()
        width = int(originalShark.get_size()[0] * src.sharkScale)
        height = int(originalShark.get_size()[1] * src.sharkScale)
        self.sharkImgs['left'] = pygame.transform.smoothscale(originalShark, (width, height))
        self.sharkImgs['right'] = pygame.transform.flip(self.sharkImgs['left'], True, False)
        self.sharkImgs['up'] = pygame.transform.rotate(self.sharkImgs['right'], 90)
        self.sharkImgs['down'] = pygame.transform.rotate(self.sharkImgs['left'], 90)
        self.sharkImgs['upleft'] = pygame.transform.rotate(self.sharkImgs['left'], -45)
        self.sharkImgs['upright'] = pygame.transform.rotate(self.sharkImgs['right'], 45)
        self.sharkImgs['downleft'] = pygame.transform.rotate(self.sharkImgs['left'], 45)
        self.sharkImgs['downright'] = pygame.transform.rotate(self.sharkImgs['right'], -45)
        self.sharkImg = self.sharkImgs['right']

    def display(self, window: pygame.Surface) -> None:
        sharkRect = self.sharkImg.get_rect(center=(self.x, self.y))
        window.blit(self.sharkImg, sharkRect)

    def move(self, dir: str, obstacles: list) -> None:
        nextX = self.x
        nextY = self.y
        if dir == "up":
            nextY -= src.sharkSpeed
            self.sharkImg = self.sharkImgs['up']
        elif dir == "down":
            nextY += src.sharkSpeed
            self.sharkImg = self.sharkImgs['down']
        elif dir == "left":
            nextX -= src.sharkSpeed
            self.sharkImg = self.sharkImgs['left']
        elif dir == "right":
            nextX += src.sharkSpeed
            self.sharkImg = self.sharkImgs['right']
        elif dir == "upleft":
            nextX -= src.sharkSpeed / math.sqrt(2)
            nextY -= src.sharkSpeed / math.sqrt(2)
            self.sharkImg = self.sharkImgs['upleft']
        elif dir == "upright":
            nextX += src.sharkSpeed / math.sqrt(2)
            nextY -= src.sharkSpeed / math.sqrt(2)
            self.sharkImg = self.sharkImgs['upright']
        elif dir == "downleft":
            nextX -= src.sharkSpeed / math.sqrt(2)
            nextY += src.sharkSpeed / math.sqrt(2)
            self.sharkImg = self.sharkImgs['downleft']
        elif dir == "downright":
            nextX += src.sharkSpeed / math.sqrt(2)
            nextY += src.sharkSpeed / math.sqrt(2)
            self.sharkImg = self.sharkImgs['downright']

        for obstacle in obstacles:
            if src.vectorLength((obstacle.x - nextX, obstacle.y - nextY)) < src.obstacleRadius + self.radius:
                return
        self.x = nextX
        self.y = nextY
        self.x %= self.windowSize[0]
        self.y %= self.windowSize[1]
    
    def repel_force(self, bird_x: float, bird_y: float) -> tuple:
        dx = bird_x - self.x
        dy = bird_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < self.radius * 3:
            force = (self.radius * 3 - distance) / (self.radius * 3)
            return (dx/distance * force, dy/distance * force)
        return (0, 0)