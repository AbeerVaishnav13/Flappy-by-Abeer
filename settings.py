import random

TITLE = "FLAPPY!!"
WIDTH = 800
HEIGHT = 500
FPS = 60
FONT_NAME = 'arial'
WIN_SCORE = 30

#Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 120, 0)
LIGHTBLUE = (0, 130, 240)
BROWN = (100, 40, 40)
GROUND_COLOR = BROWN
BGCOLOR = LIGHTBLUE

#BIRD settings
BIRD_ACC = 0.5
BIRD_FRICTION = -0.10
BIRD_GRAVITY = 0.5
BIRD_FLY = 5
BIRD_VEL_X = 3
BIRD_IMAGE = "images/bird.png"
BIRD_SIZE = (60, 40)

#Starting pipes
PIPE_BW_GAP = 100
CONSEUTIVE_PIPE_GAP = 250
PIPE_WIDTH = 54
r_high = random.randint(0, 1)
r_low = random.randint(2, 2)
PIPE_IMAGES_LIST = ["images/green_high.png", "images/brown_high.png",
                    "images/green_low.png", "images/brown_low.png"]
PIPES_LIST = [(WIDTH, 0, PIPE_WIDTH, (HEIGHT/2 - PIPE_BW_GAP/2), PIPE_IMAGES_LIST[r_high]),
              (WIDTH, (HEIGHT/2 + PIPE_BW_GAP/2), PIPE_WIDTH, HEIGHT/2, PIPE_IMAGES_LIST[r_low]),
              (WIDTH+CONSEUTIVE_PIPE_GAP, 0, PIPE_WIDTH, (HEIGHT/2 - 2*PIPE_BW_GAP), PIPE_IMAGES_LIST[r_high]),
              (WIDTH+CONSEUTIVE_PIPE_GAP, (HEIGHT/2 + PIPE_BW_GAP), PIPE_WIDTH, HEIGHT * 3/4, PIPE_IMAGES_LIST[r_low])]

#Starting clouds
CLOUD_GAP_X = 300
CLOUD_GAP_Y = 100
CLOUD_IMAGE = "images/cloud.png"
CLOUDS_LIST = [(WIDTH/4, HEIGHT/4, 150, 50, CLOUD_IMAGE),
               (WIDTH/2, HEIGHT/2, 240, 80, CLOUD_IMAGE),
               (WIDTH * 3/4, HEIGHT/4, 150, 50, CLOUD_IMAGE)]
