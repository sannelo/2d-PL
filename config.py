from pygame import Color


def rgb(r, g, b, a=255):
    return Color(r, g, b, a=a)


FIX_UPDATE_TIME = .1

FPS = 60
DEBUG = False

BLOCK_SIZE = 50
SPEED = 10
SPRENT_SPEED = 10

MAX_SCALE = 2
MIN_SCALE = 1
ADD_SCALE = 0#.2

CURSOR_COLOR = rgb(149, 151, 170)

BACKGROUND_COLOR = rgb(235, 235, 235)
GRID_COLOR = rgb(243, 243, 243)