from pygame import Surface, Vector2, Color
import pygame
from src.IBlock import IBlock

class NewVar(IBlock):
    NAME = "NEW_VAR"
    color = Color(127, 0, 127)

    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)

    def get_dict(self):
        return super().get_dict()
    
    
    def update(self) -> bool:
        print("I am New Varible")
        return False
    
class NoneBlock(IBlock):
    NAME = "NONE"

    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)
    
    def get_dict(self):
        return super().get_dict()
    
    def update(self) -> bool:
        print("I am None block")
        return False

class Start(IBlock):
    NAME = "START"
    color = Color(0, 200, 200)

    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)

    def get_dict(self):
        return super().get_dict()
    
    
    def update(self) -> bool:
        print("I am New Varible")
        return False