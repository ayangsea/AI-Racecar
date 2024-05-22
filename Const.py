import math

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 826
FPS = 60
NUM_CARS_PER_GENERATION = 50

CAR_IMG = "images/car.png"
TRACK1 = "images/track1.png"

CAR_START_X = 400
CAR_START_Y = 60
CAR_MAX_SPEED = 10
CAR_ROTATE_SPEED = math.pi / 48
CAR_ACCEL = 0.1

OUT_OF_BOUNDS = -1
TRACK = 0

BRAIN_INPUT_NODES = 5
BRAIN_HIDDEN_NODES = 17
BRAIN_OUTPUT_NODES = 4

RAY_ANGLES = [-math.pi / 2, -math.pi / 4, 0, math.pi / 4, math.pi / 2]

CHECKPOINT1_POINTS = [
    ((190, 150), (350, 200)),
    ((600, 5), (610, 100)),
    ((900, 5), (890, 100)),
    ((1070, 200), (1230, 200)),
    ((1100, 500), (1230, 400)),
    ((1070, 620), (1070, 780)),
    ((700, 650), (800, 570)),
    ((650, 385), (650, 570)),
    ((475, 570), (575, 650)),
    ((350, 650), (350, 785)),
    ((100, 700), (250, 600)),
    ((25, 550), (220, 550)),
    ((100, 330), (250, 400))
]






