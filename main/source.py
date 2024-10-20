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
viewAngle: float = (5 / 6) * pi
viewDistance: float = 20
collisionDistance: float = 0.1
sepFactor: float = 0.5
aliFactor: float = 5
cohFactor: float = 5
birdNum: int = 30