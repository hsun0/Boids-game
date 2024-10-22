import math

Colors = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'lime': (50, 205, 50),
}

# Arguments:
windowSize: tuple = (800, 600)
speed: float = 2
viewAngle: float = 2 * math.pi / 3
viewDistance: float = 100
collisionDistance: float = 15
sepFactor: float = 0.02
aliFactor: float = 0.08
cohFactor: float = 0.1
birdNum: int = 100
foodNum: int = 200
FPS: int = 60
birdSize: float = 3
initEnergy: int = 7
foodCollisionDistance: float = 3

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