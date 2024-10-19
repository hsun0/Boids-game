import math

class Bird():
    def __init__(self,
                x: float,
                y: float,
                angle: float,
                speed: float,
                viewAngle: float,
                viewDistance: float,
                sepFactor: float,
                aliFactor: float,
                cohFactor: float)->None:
        self.x = x
        self.y = y
        self.angle = angle # 速度方向(角度)
        self.speed = speed
        self.viewAngle = viewAngle
        self.viewDistance = viewDistance
        self.sepFactor = sepFactor
        self.aliFactor = aliFactor
        self.cohFactor = cohFactor

    def vectorAngle(self, v1: tuple, v2: tuple)->float:
        def absVector(v: tuple)->float:
            return math.sqrt(v[0] ** 2 + v[1] ** 2)
        def dot(v1: tuple, v2: tuple)->float:
            return v1[0] * v2[0] + v1[1] * v2[1]
        
        # 兩向量的夾角(內積 = |v1||v2|cosθ)
        angle = math.acos(dot(v1, v2) / (absVector(v1) * absVector(v2)))

        return angle

    # 判斷 bird 是否在視野內
    # 1. 是否在視線角度內
    # 2. 是否在視線距離內
    def isInSight(self, bird: 'Bird')->bool:
        vBird = (bird.x - self.x, bird.y - self.y) # 以self為原點，平移過的座標(向量)
        vVel = (math.cos(self.angle), math.sin(self.angle)) # 速度方向(向量)

        # 是否在視線角度內
        if self.VectorAngle(vBird, vVel) > self.viewAngle / 2:
            return False
        
        # 是否在視線距離內
        if (vBird[0] ** 2 + vBird[1] ** 2) > (self.viewDistance ** 2):
            return False
        
        return True
    
    ################################
    #以下三個 function 都是回傳改變的角度
    ################################

    # 避免碰撞
    def separation(self, birdsInSight: list)->float:
        dAngel = 0

        for bird in birdsInSight:
            # bird相對於self的角度
            # 注意!! 因為要避開bird，所以用-=，而不是+=
            dAngel -= math.atan2(bird.y - self.y, bird.x - self.x)

        return self.sepFactor * dAngel
    
    # 跟隨
    def alignment(self, birdsInSight: list)->float:
        dAngel = 0

        for bird in birdsInSight:
            dAngel += bird.angle

        return self.aliFactor * dAngel
    
    # 集中
    def cohesion(self, birdsInSight: list)->float:
        # 平均位置
        avgVector = (0, 0)
        for bird in birdsInSight:
            avgVector = (avgVector[0] + bird.x, avgVector[1] + bird.y)
        avgVector = (avgVector[0] / len(birdsInSight), avgVector[1] / len(birdsInSight))

        dAngel = math.atan2(avgVector[1] - self.y, avgVector[0] - self.x)
        
        return self.cohFactor * dAngel
    
    # 更新 bird 的座標，會跟動到 angle, x, y
    def update(self, birds: list)->None:
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
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)