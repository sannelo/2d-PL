from typing import Sequence, Tuple, Union
from pygame import Color, Vector2
import time, pygame

# "file_path": path
LOAD_FILE = pygame.locals.USEREVENT + 8  # type: ignore
SAVE_FILE = pygame.locals.USEREVENT + 9  # type: ignore

Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]

def str2Vec(str2vec: str):
    str_x, str_y = str2vec.split(":")
    return Vector2(float(str_x), float(str_y))

def vec2str(pos: Vector2):
    return f"{pos.x}:{pos.y}"

def time_of_function(function):
    def wrapped(*args, **params):
        start_time = time.perf_counter_ns() / 1000000
        res = function(*args, **params)
        delta = round((time.perf_counter_ns() / 1000000) - start_time, 6)
        print(delta)
        return res
    return wrapped

def rgb(r, g, b, a=255):
    return Color(r, g, b, a=a)