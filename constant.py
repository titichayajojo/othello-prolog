try:
    import pygame
except ImportError as i:
    print('File: "constant.py" cannot import :', i.name)

''' SCREEN SETTING '''
WIDTH = 560
HEIGHT = 660
MAZE_WIDTH = WIDTH
MAZE_HEIGHT = HEIGHT - 40
FPS = 60
PAC_SIZE = 30
GRID_SIZE = 20
PAC_FONT = 'resources/PAC-FONT.TTF'
ARC_FONT = 'resources/ARCADE_R.TTF'
START_BUT_HEIGHT = 80
START_BUT_WIDTH = 200
START_BUT_POS = [WIDTH / 2 - START_BUT_WIDTH / 2, 300]
EXIT_BUT_WIDTH = 150
EXIT_BUT_HEIGHT = 40
EXIT_BUT_POS = [25, 600]

''' COLORS FOR DRAWING '''
BLACK = (0,0,0)
DARK_GREY = (41,37,39)
WHITE = (255,255,255)
GREY = (107,107,107)
RED = (200,60,60)
GREEN = (0,255,0)
TURQUOISE = (100, 255 , 229)
YELLOW = (255,213,0)
PINK = (255,113,181)
ORANGE = (255,159,0)
LIGHT_BLUE = (181,211,231)
PURPLE = (201,155,203)
BLUE = (100,100,255)
FOREST_GREEN = (58, 174, 89)
BRIGHT_GREEN = (88, 204, 119)
SELECTIVE_YELLOW = (252,185,40)
MARMALADE = (242, 127,0)

''' ERROR WHEN THE FILE CANNOT BE OPEN '''
class CannotOpenFile(FileNotFoundError):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename