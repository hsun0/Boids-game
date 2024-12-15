import pygame
import source as src
from shark import Shark
from bird import Bird
import random
import math
from food import Food
from obstacle import Obstacle
import pygame
import source as src

class SettingsUI:
    def __init__(self, window: pygame.Surface):
        self.window = window
        self.settings = {
            'speed': src.speed,
            'viewDistance': src.viewDistance,
            'collisionDistance': src.collisionDistance,
            'sepFactor': src.sepFactor,
            'aliFactor': src.aliFactor,
            'cohFactor': src.cohFactor,
            'foodFactor': src.foodFactor,
            'birdNum': src.birdNum,
            'foodNum': src.foodNum,
            'groupNum': src.groupNum,
            'foodPerSecond': src.foodPerSecond,
            'foodPerClick': src.foodPerClick,
            'enable_shark': False
        }
        self.sliders = self._create_sliders()
        self.font = pygame.font.Font(None, 32)
        
    def _create_sliders(self):
        sliders = {}
        y = 50
        for key, value in self.settings.items():
            if key != 'enable_shark':
                sliders[key] = {
                    'rect': pygame.Rect(300, y, 200, 10),
                    'btn_rect': pygame.Rect(300 + (value/self._get_max_value(key))*200, y-5, 20, 20),
                    'dragging': False
                }
                y += 40
        return sliders
    
    def _get_max_value(self, key):
        max_values = {
            'speed': 5,
            'viewDistance': 200,
            'collisionDistance': 30,
            'sepFactor': 0.1,
            'aliFactor': 0.2,
            'cohFactor': 0.2,
            'foodFactor': 0.2,
            'birdNum': 200,
            'foodNum': 200,
            'groupNum': 5,
            'foodPerSecond': 30,
            'foodPerClick': 10
        }
        return max_values.get(key, 100)

    def run(self):
        running = True
        while running:
            self.window.fill(src.Colors['background'])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                    
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if pygame.Rect(350, 550, 100, 40).collidepoint(event.pos):
                        return self.settings
                        
                    for key, slider in self.sliders.items():
                        if slider['btn_rect'].collidepoint(event.pos):
                            slider['dragging'] = True
                            
                if event.type == pygame.MOUSEBUTTONUP: 
                    for slider in self.sliders.values():
                        slider['dragging'] = False
                        
                if event.type == pygame.MOUSEMOTION:
                    for key, slider in self.sliders.items():
                        if slider['dragging']:
                            slider['btn_rect'].centerx = max(slider['rect'].left, 
                                min(event.pos[0], slider['rect'].right))
                            value = ((slider['btn_rect'].centerx - slider['rect'].left) 
                                / slider['rect'].width * self._get_max_value(key))
                            # 確保groupNum為1-8的整數
                            if key == 'groupNum':
                                value = max(1, min(8, round(value)))
                            self.settings[key] = value
                            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.settings['enable_shark'] = not self.settings['enable_shark']
            
            # 繪製所有slider和文字
            y = 50
            for key, value in self.settings.items():
                if key != 'enable_shark':
                    text = self.font.render(f"{key}: {value:.2f}", True, src.Colors['black'])
                    self.window.blit(text, (20, y-10))
                    pygame.draw.rect(self.window, src.Colors['black'], self.sliders[key]['rect'])
                    pygame.draw.rect(self.window, src.Colors['red'], self.sliders[key]['btn_rect'])
                    y += 40
            
            # 繪製鯊魚模式開關
            
            
            # 繪製開始按鈕
            pygame.draw.rect(self.window, src.Colors['green'], (350, 550, 100, 40))
            start_text = self.font.render("Start", True, src.Colors['black'])
            self.window.blit(start_text, (370, 560))
            
            pygame.display.flip()
        return self.settings



def main()->None:
    # 要有這個不然無法使用 pygame 的功能
    pygame.init()

    # 設定視窗
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Boids Simulation')

     # 顯示設定介面
    settings_ui = SettingsUI(window)
    settings = settings_ui.run()
    
    if settings is None:  # 如果使用者關閉視窗
        pygame.quit()
        return
    # 更新設定
    src.speed = settings['speed']
    src.viewDistance = settings['viewDistance']
    src.collisionDistance = settings['collisionDistance']
    src.sepFactor = settings['sepFactor']
    src.aliFactor = settings['aliFactor']
    src.cohFactor = settings['cohFactor']
    src.foodFactor = settings['foodFactor']
    src.birdNum = int(settings['birdNum'])
    src.foodNum = int(settings['foodNum'])
    src.groupNum = int(settings['groupNum'])
    src.foodPerSecond = int(settings['foodPerSecond'])
    src.foodPerClick = int(settings['foodPerClick'])

    
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