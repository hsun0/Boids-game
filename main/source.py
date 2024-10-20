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
windowSize: tuple = (1200, 900)
speed: float = 2
viewAngle: float = pi / 2
viewDistance: float = 100
collisionDistance: float = 25
sepFactor: float = 0.05
aliFactor: float = 0.05
cohFactor: float = 0.01
birdNum: int = 50