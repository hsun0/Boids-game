from math import pi
Colors = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0)
}

# Arguments:
windowSize: tuple = (800, 600)
speed: float = 2
viewAngle: float = pi
viewDistance: float = 40
collisionDistance: float = 0
sepFactor: float = 0.001
aliFactor: float = 0.001
cohFactor: float = 1
birdNum: int = 20