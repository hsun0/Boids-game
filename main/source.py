import math

Colors = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'lime': (50, 180, 50),
    'background': (255,255,255),
    'brown': (139, 69, 19),
    'purple': (138, 43, 226)
}

# Arguments:
speed: float = 2
viewAngle: float = 2 * math.pi / 3
viewDistance: float = 100
collisionDistance: float = 15
sepFactor: float = 0.02
aliFactor: float = 0.08
cohFactor: float = 0.1
foodFactor: float = 0.05
birdNum: int = 75
foodNum: int = 100
FPS: int = 60
birdSize: float = 4.5
initEnergy: int = 7
foodSize: float = 3
foodCollisionDistance: float = 5
copyEnergy: int = 14
foodPerSecond: int= 10
foodPerClick: int = 3    
giveFoodRadius: float = 30
colorEnergy1: int = 5
colorEnergy2: int = 10
currentForce: int = 0.2
currentAngleFactor = 0.01
groupNum = 3  # 群體數量
sharkSpeed = 2
COLORS_BY_GROUP = [
    (255, 0, 0),    # 紅色群體
    (0, 255, 0),    # 綠色群體
    (0, 0, 255),    # 藍色群體
]

# 障礙物參數
obstacleRadius = 20 # 障礙物半徑
obstacleFactor = 0.15
obstacleColor = Colors['brown']

FOOD_COLOR = [
    Colors['lime'],
    Colors['purple'],
    Colors['red']
]

# function
def getSign(x)->int:
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
    
def vectorLength(v: tuple)->float:
    return math.sqrt(v[0] ** 2 + v[1] ** 2)

# Normalize the angle to [-π, π]
def normalizeAngle(angle: float)->float:
    angle = (angle % (2 * math.pi) + 2 * math.pi) % (2 * math.pi)
    if angle > math.pi:
        angle -= 2 * math.pi
    return angle