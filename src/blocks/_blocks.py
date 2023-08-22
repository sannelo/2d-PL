from typing import Any
from bitstring import Bits, BitArray
from pygame import Surface, Vector2, Color
import pygame
from src.code.code_session import CodeSession
from src.blocks.IBlock import IBlock

class NewVar(IBlock):
    NAME = "NEW_VAR"

    image: Surface = pygame.image.load(f"./imgs/{NAME.lower()}.png")#.convert_alpha()
    color = Color(127, 0, 127)

    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)
    
    
    def update(self) -> bool:
        print("I am New Varible")
        return False
    
    def exec(self, session: CodeSession, **params):
        pass
    
class NoneBlock(IBlock):

    NAME = "NONE"
    image: Surface = pygame.image.load(f"./imgs/{NAME.lower()}.png")

    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)
    
    def update(self) -> bool:
        print("I am None block")
        return False
    
    def exec(self, session: CodeSession, **params):
        print("None")
        pass

class Start(IBlock):
    NAME = "START"

    image: Surface = pygame.image.load(f"./imgs/{NAME.lower()}.png")
    color = Color(0, 200, 200)

    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)
    
    def update(self) -> bool:
        print("I am New Varible")
        return False
    
    def exec(self, session: CodeSession, **params):
        self.next(session)
    
class Print(IBlock):
    NAME = "PRINT"

    image: Surface = pygame.image.load(f"./imgs/{NAME.lower()}.png")
    color = Color(0, 255, 0)

    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)
    
    def update(self) -> bool:
        print("I am New Varible")
        return False
    
    def exec(self, session: CodeSession, **params):
        left = (self.direction - 1) % 4
        self.next_no_wait(left)
        # print("Direction:", self.direction)
        # print("Left:",left)
        left_block = self.blocks_around[left]
        # print("Left block:", left_block)

        data: BitArray = left_block.exec(session, data="")

        try:
            print(data.tobytes().decode("utf-8"), end="\a")
        except UnicodeDecodeError:
            print(f"Bin: {data.bin} Int: {data.int}")

        self.next(session)

    # def get_direct(self):
    #     return self.blocks_around[self.direction], self.direction

class Zero(IBlock):
    NAME = "ZERO"

    EXECUTABLE = False

    image: Surface = pygame.image.load(f"./imgs/{NAME.lower()}.png")
    color = Color(255, 255, 255)

    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)
    
    def update(self) -> bool:
        print("I am New Varible")
        return False
    
    def exec(self, session: CodeSession, **params):
        data: str = params["data"]
        data = data + "0"
        left = (self.direction - 1) % 4
        self.next_no_wait(self.direction)
        return self.blocks_around[self.direction].exec(session, data=data)

    def get_direct(self):
        return self.blocks_around[self.direction], self.direction

class One(IBlock):
    NAME = "One"

    EXECUTABLE = False

    image: Surface = pygame.image.load(f"./imgs/{NAME.lower()}.png")
    color = Color(0, 0, 0)

    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)
    
    def update(self) -> bool:
        print("I am New Varible")
        return False
    
    def exec(self, session: CodeSession, **params):
        data: BitArray = params["data"]
        data = data + "1"
        left = (self.direction - 1) % 4
        self.next_no_wait(self.direction)
        return self.blocks_around[self.direction].exec(session, data=data)
    
    def get_direct(self):
        return self.blocks_around[self.direction], self.direction
    
class IOend(IBlock):
    NAME = "IOEND"

    EXECUTABLE = False

    image: Surface = pygame.image.load(f"./imgs/{NAME.lower()}.png")
    color = Color(255, 0, 0)

    def __init__(self, pos: Vector2, size: Vector2) -> None:
        super().__init__(pos, size)
    
    def update(self) -> bool:
        print("I am New Varible")
        return False
    
    def exec(self, session: CodeSession, **params):
        data: str = params["data"]
        data = data[::-1]
        return BitArray(bin="0b" + data)
    
    def get_direct(self):
        return self.blocks_around[self.direction], self.direction