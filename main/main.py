import pygame
import source as src
from bird import Bird
import random
import math
from food import Food

def main()->None:
    # 要有這個不然無法使用 pygame 的功能
    pygame.init()

    # 設定視窗
    window = pygame.display.set_mode(src.windowSize)
    pygame.display.set_caption('Boids Simulation')

    # 初始化鳥群
    birds = []
    for _ in range(src.birdNum):
        x = random.uniform(0, src.windowSize[0])
        y = random.uniform(0, src.windowSize[1])
        angle = random.uniform(-math.pi, math.pi)
        birds.append(Bird(x, y, angle, src.initEnergy))

    # 初始化食物
    foods = []
    for _ in range(src.foodNum):
        x = random.uniform(0, src.windowSize[0])
        y = random.uniform(0, src.windowSize[1])
        foods.append(Food(x, y))

    # Main Loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Note: pygame 會將所有的東西畫在緩衝區，然後再透過 flip() 顯示到螢幕上
        # 清除畫面
        window.fill(src.Colors['white'])

        removeList = []

        # 畫出所有的鳥
        for bird in birds:
            # 更新鳥的座標
            bird.move(birds, foods)
            bird.eat(foods)
            bird.display(window)

            # 移除沒有能量的鳥
            if bird.energy <= 0:
                removeList.append(bird)

            # 當鳥的能量大於一定量時，複製一隻鳥
            if bird.energy >= src.copyEnergy:
                birds.append(bird.copy())

        for food in foods:
            food.display(window)

        # 移除能量為 0 的鳥
        for bird in removeList:
            birds.remove(bird)

        # 每十秒減少一次所有鳥的能量
        if pygame.time.get_ticks() % 5000 < clock.get_time():
            for bird in birds:
                bird.energy -= 1

        if pygame.time.get_ticks() % 1000 < clock.get_time():
            print("birdNum: ", len(birds))

        # 將緩衝區顯示到螢幕上
        pygame.display.flip()

        # FPS
        clock.tick(src.FPS)
    pygame.quit()

if __name__ == '__main__':
    main()