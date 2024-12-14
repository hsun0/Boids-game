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
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Boids Simulation')
    windowSize = window.get_size()
    # 初始化鳥群
    birds = []
    numbreOfBirds = []
    birds_per_group = src.birdNum // src.NUM_GROUPS
    for group_id in range(src.NUM_GROUPS):
        numbreOfBirds.append(birds_per_group)
        for _ in range(birds_per_group):
            x = random.uniform(0, windowSize[0])
            y = random.uniform(0, windowSize[1])
            angle = random.uniform(-math.pi, math.pi)
            birds.append(Bird(x, y, angle, src.initEnergy, windowSize, group_id))


    # 初始化食物
    foods = []
    for _ in range(src.foodNum):
        x = random.uniform(0, windowSize[0])
        y = random.uniform(0, windowSize[1])
        foods.append(Food(x, y))

    # Main Loop
    running = True
    clock = pygame.time.Clock()
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # 按下 ESC 鍵結束程式
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # 按下滑鼠左鍵，增加食物
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for _ in range(src.foodPerClick):
                    angle = random.uniform(0, 2 * math.pi)
                    foodX = x + random.uniform(0, src.giveFoodRadius) * math.cos(angle)
                    foodY = y + random.uniform(0, src.giveFoodRadius) * math.sin(angle)

                    if foodX < 0:
                        foodX = foodX + windowSize[0]
                    if foodX > windowSize[0]:
                        foodX = foodX - windowSize[0]
                    if foodY < 0:
                        foodY = foodY + windowSize[1]
                    if foodY > windowSize[1]:
                        foodY = foodY - windowSize[1]

                    foods.append(Food(foodX, foodY))
        
        # Note: pygame 會將所有的東西畫在緩衝區，然後再透過 flip() 顯示到螢幕上
        # 清除畫面
        window.fill(src.Colors['background'])

        removeList = []

        # 畫出所有的鳥
        for bird in birds:
            # 更新鳥的座標
            bird.move(birds, foods)
            bird.eat(foods)
            bird.display(window)

            # 移除沒有能量的鳥
            if bird.energy <= 0:
                numbreOfBirds[bird.group_id] -= 1
                removeList.append(bird)

            # 當鳥的能量大於一定量時，複製一隻鳥
            if bird.energy >= src.copyEnergy:
                numbreOfBirds[bird.group_id] += 1
                birds.append(bird.copy())

        for food in foods:
            food.display(window)

        # 移除能量為 0 的鳥
        for bird in removeList:
            birds.remove(bird)

        if pygame.time.get_ticks() % 1000 < clock.get_time():
            for _ in range(src.foodPerSecond):
                x = random.uniform(0, windowSize[0])
                y = random.uniform(0, windowSize[1])
                foods.append(Food(x, y))

        # 每五秒減少一次所有鳥的能量
        if pygame.time.get_ticks() % 5000 < clock.get_time():
            for bird in birds:
                bird.energy -= 1

        # 在左上角顯示鳥的數量
        font = pygame.font.Font(None, 20)
        text = font.render(f'Foods: {len(foods)}', True, src.Colors['black'])
        window.blit(text, (10, 10))
        for i in range(src.NUM_GROUPS):
            text = font.render(f'Group {i + 1}: {numbreOfBirds[i]}', True, src.COLORS_BY_GROUP[i])
            window.blit(text, (10, 30 + 20 * i))

        # 將緩衝區顯示到螢幕上
        pygame.display.flip()

        # FPS
        clock.tick(src.FPS)
        background = pygame.Surface(windowSize)
        background = background.convert()
        background.fill(src.Colors['background'])

    
    pygame.quit()

if __name__ == '__main__':
    main()