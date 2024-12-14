import pygame
import source as src
from shark import Shark
from bird import Bird
import random
import math
from food import Food
from obstacle import Obstacle
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
    obstacles = []
    birds_per_group = src.birdNum // src.groupNum
    for group_id in range(src.groupNum):
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

    # 初始化鯊魚
    shark = Shark(400, 300, windowSize)

    # Main Loop
    running = True
    currentEnabled = False
    currentDirection = (0, -1)
    clock = pygame.time.Clock()
    while running:
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_d]:
            shark.move("up", obstacles)
        elif keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d]:
            shark.move("down", obstacles)
        elif keys[pygame.K_a] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            shark.move("left", obstacles)
        elif keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s]:
            shark.move("right", obstacles)
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            shark.move("upleft", obstacles)
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            shark.move("upright", obstacles)
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            shark.move("downleft", obstacles)
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            shark.move("downright", obstacles)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # 按下 ESC 鍵結束程式
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_o:
                    pos = pygame.mouse.get_pos()
                    obstacles.append(Obstacle(pos[0], pos[1]))
                if event.key == pygame.K_SPACE:
                    currentEnabled = not currentEnabled
                if event.key == pygame.K_UP:
                    currentDirection = (0, -1)
                if event.key == pygame.K_RIGHT:
                    currentDirection = (1, 0)
                if event.key == pygame.K_DOWN:  
                    currentDirection = (0, 1)
                if event.key == pygame.K_LEFT:
                    currentDirection = (-1, 0)

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
        
        # enable current
        if currentEnabled:
            dPos = (currentDirection[0] * src.currentForce, currentDirection[1] * src.currentForce)
            def move(obj):
                if(type(obj) == Obstacle or type(obj) == Shark):
                    obj.x += dPos[0] / 2
                    obj.y += dPos[1] / 2
                elif(type(obj) == Bird):
                    # 計算風向角度
                    wind_angle = math.atan2(dPos[1], dPos[0])
                    # 計算當前角度和風向的差異
                    angle_diff = src.normalizeAngle(wind_angle - obj.angle)
                    # 根據風力大小調整角度
                    angle_change = angle_diff * src.currentAngleFactor
                    # 更新鳥的角度
                    obj.angle = src.normalizeAngle(obj.angle + angle_change)
                    # 移動位置
                    obj.x += dPos[0]
                    obj.y += dPos[1] 

                else:
                    obj.x += dPos[0]
                    obj.y += dPos[1]
                if obj.x < 0:
                    obj.x = obj.x + windowSize[0]
                if obj.x > windowSize[0]:
                    obj.x = obj.x - windowSize[0]
                if obj.y < 0:
                    obj.y = obj.y + windowSize[1]
                if obj.y > windowSize[1]:
                    obj.y = obj.y - windowSize[1]
            for bird in birds:
                move(bird)
            for food in foods:
                move(food)
            for obstacle in obstacles:
                move(obstacle)
            move(shark)
        
        # Note: pygame 會將所有的東西畫在緩衝區，然後再透過 flip() 顯示到螢幕上
        # 清除畫面
        window.fill(src.Colors['background'])

        removeList = []

        for obstacle in obstacles:
            obstacle.display(window)
        shark.display(window)

        # 畫出所有的鳥
        for bird in birds:
            # 更新鳥的座標
            bird.move(birds, foods, obstacles, shark)
            bird.eat(foods)
            bird.beEaten(shark)
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
        text = font.render(f'Current Enabled: {currentEnabled}', True, src.Colors['black'])
        window.blit(text, (10, 30))
        for i in range(src.groupNum):
            text = font.render(f'Group {i + 1}: {numbreOfBirds[i]}', True, src.COLORS_BY_GROUP[i])
            window.blit(text, (10, 50 + 20 * i))

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