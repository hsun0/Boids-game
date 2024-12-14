import pygame
import math
import source as src

class Shark:
    def __init__(self, x: float, y: float, windowSize: tuple) -> None:
        self.x = x
        self.y = y
        self.windowSize = windowSize
        self.imgPath = "main/shark.png"
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

    def move(self, dir: str) -> None:
        if dir == "up":
            self.y -= src.sharkSpeed
            self.sharkImg = self.sharkImgs['up']
        elif dir == "down":
            self.y += src.sharkSpeed
            self.sharkImg = self.sharkImgs['down']
        elif dir == "left":
            self.x -= src.sharkSpeed
            self.sharkImg = self.sharkImgs['left']
        elif dir == "right":
            self.x += src.sharkSpeed
            self.sharkImg = self.sharkImgs['right']
        elif dir == "upleft":
            self.x -= src.sharkSpeed / math.sqrt(2)
            self.y -= src.sharkSpeed / math.sqrt(2)
            self.sharkImg = self.sharkImgs['upleft']
        elif dir == "upright":
            self.x += src.sharkSpeed / math.sqrt(2)
            self.y -= src.sharkSpeed / math.sqrt(2)
            self.sharkImg = self.sharkImgs['upright']
        elif dir == "downleft":
            self.x -= src.sharkSpeed / math.sqrt(2)
            self.y += src.sharkSpeed / math.sqrt(2)
            self.sharkImg = self.sharkImgs['downleft']
        elif dir == "downright":
            self.x += src.sharkSpeed / math.sqrt(2)
            self.y += src.sharkSpeed / math.sqrt(2)
            self.sharkImg = self.sharkImgs['downright']
        self.x %= self.windowSize[0]
        self.y %= self.windowSize[1]