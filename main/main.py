import pygame
import source as src
from bird import Bird
import random
import math

def main()->None:
    # 要有這個不然無法使用 pygame 的功能
    pygame.init()

    #設定視窗
    window = pygame.display.set_mode(src.windowSize)
    pygame.display.set_caption('Boids Simulation')

    # 初始化鳥群
    birds = []
    for _ in range(src.birdNum):
        x = random.uniform(0, src.windowSize[0])
        y = random.uniform(0, src.windowSize[1])
        angle = random.uniform(-math.pi, math.pi)
        birds.append(Bird(x, y, angle))

    # Main Loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Note: pygame 會將所有的東西畫在緩衝區，然後再透過 flip() 顯示到螢幕上
        # 清除畫面
        window.fill(src.Colors['black'])

        # 畫出所有的鳥
        for bird in birds:
            # 更新鳥的座標
            bird.move(birds)
            point = [
                (bird.x + src.birdSize * 2 * math.cos(bird.angle), bird.y + src.birdSize * 2 * math.sin(bird.angle)),
                (bird.x + src.birdSize * math.cos(bird.angle + 2 * math.pi / 3), bird.y + src.birdSize * math.sin(bird.angle + 2 * math.pi / 3)),
                (bird.x + src.birdSize * math.cos(bird.angle - 2 * math.pi / 3), bird.y + src.birdSize * math.sin(bird.angle - 2 * math.pi / 3))
            ]
            pygame.draw.polygon(window, src.Colors['white'], point)

        # 將緩衝區顯示到螢幕上
        pygame.display.flip() 

        # FPS
        clock.tick(src.FPS)
    pygame.quit()

if __name__ == '__main__':
    main()