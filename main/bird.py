import math
import pygame
import source as src

class Bird():
    def __init__(self, x: float, y: float, angle: float, energy: int, windowSize: tuple)->None:
        self.x = x
        self.y = y
        self.angle = angle # 速度方向(角度)
        self.energy = energy
        self.windowSize = windowSize

    def display(self, window)->None:
        point = [
            (self.x + src.birdSize * 2 * math.cos(self.angle), self.y + src.birdSize * 2 * math.sin(self.angle)),
            (self.x + src.birdSize * math.cos(self.angle + 2 * math.pi / 3), self.y + src.birdSize * math.sin(self.angle + 2 * math.pi / 3)),
            (self.x + src.birdSize * math.cos(self.angle - 2 * math.pi / 3), self.y + src.birdSize * math.sin(self.angle - 2 * math.pi / 3))
        ]

        # 調整透明度
        def adjustTrans(x: int)->int:
            if x == 255:
                return 255
            return self.getTrans()
        
        color = tuple(adjustTrans(x) for x in src.Colors['red'])
        pygame.draw.polygon(window, color, point)

    def eat(self, foods: list)->None:
        removeList = []

        # 檢查是否有食物在吃的範圍內，有的話吃掉
        for food in foods:
            if src.vectorLength((food.x - self.x, food.y - self.y)) > src.foodCollisionDistance:
                continue
            self.energy += 1
            removeList.append(food)
        
        for food in removeList:
            foods.remove(food)

    def getTrans(self)->int:
        if self.energy <= 0:
            return 255
        if self.energy <= 5:
            return 150
        if self.energy <= 10:
            return 50
        return 0

    def vectorAngle(self, v1: tuple, v2: tuple)->float:
        def absVector(v: tuple)->float:
            return math.sqrt(v[0] ** 2 + v[1] ** 2)
        def dot(v1: tuple, v2: tuple)->float:
            return v1[0] * v2[0] + v1[1] * v2[1]
        
        # 兩向量的夾角(內積 = |v1||v2|cosθ)
        cos_angle = dot(v1, v2) / (absVector(v1) * absVector(v2))
        # 處理數值誤差
        cos_angle = max(-1, min(1, cos_angle))
        return math.acos(cos_angle)

    # 判斷 bird or food 是否在視野內
    # 1. 是否在視線角度內
    # 2. 是否在視線距離內
    def isInSight(self, obj)->bool:
        # 避免除以 0
        if src.vectorLength((obj.x - self.x, obj.y - self.y)) < 0.00001:
            return False
        
        vBird = (obj.x - self.x, obj.y - self.y) # 以self為原點，平移過的座標(向量)
        vVel = (math.cos(self.angle), math.sin(self.angle)) # 速度方向(向量)

        # 是否在視線角度內
        if self.vectorAngle(vBird, vVel) > src.viewAngle / 2:
            return False
        
        # 是否在視線距離內
        dx = min(abs(obj.x - self.x), self.windowSize[0] - abs(obj.x - self.x))
        dy = min(abs(obj.y - self.y), self.windowSize[1] - abs(obj.y - self.y))
        if src.vectorLength((dx, dy)) > src.viewDistance:
            return False
        
        return True
    
    def copy(self)->'Bird':
        self.energy >>= 1
        return Bird(self.x, self.y, self.angle, self.energy, self.windowSize)
    
    ################################
    #以下四個 function 都是回傳改變的角度
    ################################

    # 避免碰撞
    def separation(self, birdsInSight: list)->float:
        dAngel = 0

        for bird in birdsInSight:
            dx = bird.x - self.x
            dy = bird.y - self.y

            # 處理在邊界兩邊的情況
            if abs(dx) > self.windowSize[0] - abs(dx):
                dx = -1 * src.getSign(dx) * (self.windowSize[0] - abs(dx))
            if abs(dy) > self.windowSize[1] - abs(dy):
                dy = -1 * src.getSign(dy) * (self.windowSize[1] - abs(dy))

            if src.vectorLength((dx, dy)) > src.collisionDistance:
                continue
                
            dAngel += math.atan2(dy, dx)

        return src.sepFactor * dAngel
    
    # 跟隨
    def alignment(self, birdsInSight: list) -> float:
        if len(birdsInSight) == 0:
            return 0
            
        total_angle_diff = 0
        for bird in birdsInSight:
            # 計算角度差
            angle_diff = bird.angle - self.angle
                
            total_angle_diff += angle_diff
        
        return src.aliFactor * (total_angle_diff / len(birdsInSight))
    # 集中
    def cohesion(self, birdsInSight: list) -> float:
        if len(birdsInSight) == 0:
            return 0

        avgX = 0
        avgY = 0
        
        for bird in birdsInSight:
            dx = bird.x - self.x
            dy = bird.y - self.y
            
            # 處理環繞邊界的情況
            if abs(dx) > self.windowSize[0] / 2:
                dx = dx - src.getSign(dx) * self.windowSize[0]
            if abs(dy) > self.windowSize[1] / 2:
                dy = dy - src.getSign(dy) * self.windowSize[1]
                
            avgX += dx
            avgY += dy
        
        # 計算平均位置（相對於當前鳥的位置）
        avgX /= len(birdsInSight)
        avgY /= len(birdsInSight)
        
        # 計算到中心點的距離
        distance = math.sqrt(avgX * avgX + avgY * avgY)
            
        # 計算目標方向
        target_angle = math.atan2(avgY, avgX)
        
        # 計算需要轉向的角度
        angle_diff = target_angle - self.angle
        
        # normal angle to [-π, π]
        angle_diff = src.normalizeAngle(angle_diff)
        
        # 根據距離調整cohesion強度
        # 距離越遠，cohesion力越大，但設定上限避免過度轉向
        distance_factor = min(distance / 100.0, 1.0)

        return src.cohFactor * angle_diff * distance_factor
    
    def goToFood(self, foodsInSight: list)->float:
        if len(foodsInSight) == 0:
            return 0
        
        avgX = 0
        avgY = 0

        for food in foodsInSight:
            dx = food.x - self.x
            dy = food.y - self.y

            # 處理在邊界兩邊的情況
            if abs(dx) > self.windowSize[0] - abs(dx):
                dx = -1 * src.getSign(dx) * (self.windowSize[0] - abs(dx))
            if abs(dy) > self.windowSize[1] - abs(dy):
                dy = -1 * src.getSign(dy) * (self.windowSize[1] - abs(dy))

            avgX += dx
            avgY += dy

        # 計算平均位置（相對於當前鳥的位置）
        avgX /= len(foodsInSight)
        avgY /= len(foodsInSight)

        # 計算到中心點的距離
        distance = src.vectorLength((avgX, avgY))
        
        # 計算目標方向
        target_angle = math.atan2(avgY, avgX)
        
        # 計算需要轉向的角度
        angle_diff = target_angle - self.angle
        
        angle_diff = src.normalizeAngle(angle_diff)
        
        # 根據距離調整goToFood強度
        # 距離越遠，goToFood力越大，但設定上限避免過度轉向
        distance_factor = min(distance / 100.0, 1.0)

        return src.foodFactor * angle_diff * distance_factor
    
    # 更新 bird 的座標，會跟動到 angle, x, y
    def move(self, birds: list, foods: list)->None:

        # 找出視野內的鳥
        birdsInSight = []
        for bird in birds:
            if bird == self:
                continue
            if self.isInSight(bird):
                birdsInSight.append(bird)

        # 找出視野內的食物
        foodsInSight = []
        for food in foods:
            if self.isInSight(food):
                foodsInSight.append(food)
        
        # 更新角度
        self.angle += self.separation(birdsInSight)
        self.angle += self.alignment(birdsInSight)
        self.angle += self.cohesion(birdsInSight)
        self.angle += self.goToFood(foodsInSight)

        # 更新座標
        self.x = (self.x + src.speed * math.cos(self.angle)) % self.windowSize[0]
        self.y = (self.y + src.speed * math.sin(self.angle)) % self.windowSize[1]
