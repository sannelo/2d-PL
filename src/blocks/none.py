from pygame import Surface, Vector2
from src.IBlock import IBlock

class NoneBlock(IBlock):
    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)
    
    def get_dict(self):
        return super().get_dict()
    
    def update(self) -> bool:
        print("I am None block")
        return False
        