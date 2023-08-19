from abc import ABC, ABCMeta, abstractmethod, abstractclassmethod, abstractproperty
from pygame import Rect, Surface
import pygame
from pygame.math import Vector2
from pygame import Color


class IBlock(ABC):

    NAME = "INTERFACE"

    
    pos: Vector2 = Vector2(0, 0)
    size: Vector2 = Vector2(50, 50)

    color: Color = Color(125, 125, 125)
    image: Surface

    blocks_around: tuple

    def __init__(self, pos: Vector2, size: Vector2, blocks_around: tuple) -> None:
        self.pos = pos
        self.size = size
        # self.image: Surface = pygame.image.load(f"./imgs/{self.NAME.lower()}.png").convert_alpha()

    @abstractmethod
    def update(self) -> bool:
        ...

    def toLocalPos(self, player_pos: Vector2, scale: float) -> Vector2: # scale 0.1-2
        block_size = self.size.x * scale


        offset = block_size / 2 / scale
        offset = offset - ((offset // block_size) * block_size)

        return Vector2(
            # self.pos.x + player_pos.x + offset.x,
            # self.pos.y + player_pos.y + offset.y,
            ((round((self.pos.x + offset) * scale) // block_size) * block_size) + player_pos.x,
            ((round((self.pos.y + offset) * scale) // block_size) * block_size) + player_pos.y,
        )
    
    def draw(self, win: Surface, block_pos: Vector2, scale: float = 1, draw_image: bool = True):
        rect = (
                block_pos.x,
                block_pos.y, 

                round(self.size.x * scale, 3), 
                round(self.size.y * scale, 3)
            )
        pygame.draw.rect(win, self.color, rect=rect)
        # self.image.set_clip(rect)
        if draw_image:
            win.blit(pygame.transform.scale(self.image, (rect[2], rect[3])), rect)
        # font = pygame.font.Font(None, round(14*scale))
        # text_surface = font.render(str(self.pos), True, (0, 0, 0))
        # text_pos = Vector2(
        #     block_pos.x + 5 * scale,
        #     block_pos.y + 5 * scale
        # )
        # win.blit(text_surface, text_pos)
    
    def set_color(self, color: Color):
        self.color = color
        return self

"""
class foo:
    name: str
    def __init__(self, name):
        self.name = name

    def hello(self):
        print("Hello", self.name)

my_dict = {
    "alex": foo("Alex"),
    "python": foo("Python"),
    "world": foo("World!!!")
}

# Какой-то код для сохранения my_dict в json файл (foos.json)

# Какой-то код для загрузки my_dict из json файла (foos.json) 
"""
