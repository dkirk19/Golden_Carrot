TITLE = "Golden Carrot"
# screen dims
WIDTH = 960
HEIGHT = 600
# frames per second
FPS = 60
# colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
REDDISH = (240,55,66)
SKY_BLUE = (143, 185, 252)
GOLD = (255,215,0)
FONT_NAME = 'arial'
SPRITESHEET = "spritesheet_jumper.png"
# data files
HS_FILE = "highscore.txt"
# player settings
PLAYER_ACC = 0.8
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20
# game settings
BOOST_POWER = 20
'''added individual spawn percentage varialbes for each coin and carrots'''
BRONZE_SPAWN_PCT = 12
SILVER_SPAWN_PCT = 8
GOLD_SPAWN_PCT = 4
CARROT_SPAWN_PCT = 1
SNOW_PLAT_FREQ = 10
MOB_FREQ = 5000
#layer uses numerical values to determine where each layer goes
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
BACK_LAYER = 3

# platform settings
PLATFORM_LIST = [(0, HEIGHT - 40),
                 (65, HEIGHT - 300),
                 (20, HEIGHT - 350),
                 (200, HEIGHT - 150),
                 (200, HEIGHT - 450)]
