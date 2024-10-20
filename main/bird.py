import math
import source as src

class Bird():
    def __init__(self, x: float, y: float, angle: float)->None:
        self.x = x
        self.y = y
        self.angle = angle # 速度方向(角度)

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

    # 判斷 bird 是否在視野內
    # 1. 是否在視線角度內
    # 2. 是否在視線距離內
    def isInSight(self, bird: 'Bird')->bool:
        vBird = (bird.x - self.x, bird.y - self.y) # 以self為原點，平移過的座標(向量)
        vVel = (math.cos(self.angle), math.sin(self.angle)) # 速度方向(向量)

        # 是否在視線角度內
        if self.vectorAngle(vBird, vVel) > src.viewAngle / 2:
            return False
        
        # 是否在視線距離內
        dx = min(abs(bird.x - self.x), src.windowSize[0] - abs(bird.x - self.x))
        dy = min(abs(bird.y - self.y), src.windowSize[1] - abs(bird.y - self.y))
        if src.vectorLength((dx, dy)) > src.viewDistance:
            return False
        
        return True
    
    ################################
    #以下三個 function 都是回傳改變的角度
    ################################

    # 避免碰撞
    def separation(self, birdsInSight: list)->float:
        dAngel = 0

        for bird in birdsInSight:
            dx = bird.x - self.x
            dy = bird.y - self.y

            # 處理在邊界兩邊的情況
            if abs(dx) > src.windowSize[0] - abs(dx):
                dx = -1 * src.getSign(dx) * (src.windowSize[0] - abs(dx))
            if abs(dy) > src.windowSize[1] - abs(dy):
                dy = -1 * src.getSign(dy) * (src.windowSize[1] - abs(dy))

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
            
            # 正規化角度差到 -π 到 π 的範圍
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
                
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
            if abs(dx) > src.windowSize[0] / 2:
                dx = dx - src.getSign(dx) * src.windowSize[0]
            if abs(dy) > src.windowSize[1] / 2:
                dy = dy - src.getSign(dy) * src.windowSize[1]
                
            avgX += dx
            avgY += dy
        
        # 計算平均位置（相對於當前鳥的位置）
        avgX /= len(birdsInSight)
        avgY /= len(birdsInSight)
        
        # 計算到中心點的距離
        distance = math.sqrt(avgX * avgX + avgY * avgY)
        
        # 如果距離為0，表示鳥群已經在同一點，不需要轉向
        if distance < 0.0001:  # 使用小數避免浮點數精確度問題
            return 0
            
        # 計算目標方向
        target_angle = math.atan2(avgY, avgX)
        
        # 計算需要轉向的角度
        angle_diff = target_angle - self.angle
        
        # 正規化角度到 -π 到 π 的範圍
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        
        # 根據距離調整cohesion強度
        # 距離越遠，cohesion力越大，但設定上限避免過度轉向
        distance_factor = min(distance / 100.0, 1.0)  # 可以根據需求調整參數
        
        return src.cohFactor * angle_diff * distance_factor
    
    # 更新 bird 的座標，會跟動到 angle, x, y
    def move(self, birds: list)->None:
        birdsInSight = []
        for bird in birds:
            if bird == self:
                continue
            if self.isInSight(bird):
                birdsInSight.append(bird)
        
        # 更新角度
        self.angle += self.separation(birdsInSight)
        self.angle += self.alignment(birdsInSight)
        self.angle += self.cohesion(birdsInSight)

        # 更新座標
        self.x = (self.x + src.speed * math.cos(self.angle)) % src.windowSize[0]
        self.y = (self.y + src.speed * math.sin(self.angle)) % src.windowSize[1]