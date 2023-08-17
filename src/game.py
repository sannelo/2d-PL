from pygame import Color, Surface, Vector2
from src.IBlock import IBlock
from src.blocks import NoneBlock, Blocks
from src.utils.engine import Engine
from src.utils.drawer import get_grid
from src.utils.other import rgb, str2Vec, vec2str, Coordinate
import pygame


class Game(Engine):

    blocks: Blocks[str, IBlock] = Blocks[str, IBlock]()

    player_pos = Vector2(0, 0)
    player_scale = 1.0

    DEBUG = True

    BLOCK_SIZE = 100
    SPEED = 10
    SPRENT_SPEED = 10

    MAX_SCALE = 2
    MIN_SCALE = .1

    CURSOR_COLOR = rgb(149, 151, 170)
    BACKGROUND_COLOR = rgb(249, 213, 206)
    GRID_COLOR = rgb(243, 164, 169)

    coursore_color_adder = -.01
    coursore_color = .9

    def __init__(self, 
                size: Coordinate = (0, 0),
                flags: int = 0,
                depth: int = 0,
                display: int = 0,
                vsync: int = 0,
                FPS: int = 0) -> None:
        
        pygame.init()
        win = pygame.display.set_mode(size, flags, depth, display, vsync)

        super().__init__(win)
        self.FPS = FPS

    def fixed_update(self):
        # print(round(time.time()))
        pass

    def update(self, _):
        pygame.display.set_caption(f"Scale: {round(self.player_scale, 2)} Position: {self.player_pos} FPS: {self.FPS_NOW} MAX FPS: {self.FPS_MAX} MAX FPS: {self.FPS_MIN}")

        self.width = self.win.get_width()
        self.height = self.win.get_height()
        self.win_size = Vector2(self.width, self.height)

        if self.coursore_color > .99: self.coursore_color_adder *= -1
        elif self.coursore_color < .099: self.coursore_color_adder *= -1

        self.coursore_color += self.coursore_color_adder

        self.mouse_pos = Vector2(pygame.mouse.get_pos())

        self.block_size = round(self.BLOCK_SIZE * self.player_scale)

        self.block_pos = self.grid_alignment(self.mouse_pos)        

    def input(self, keys_down: list[int], keys_up: list[int], mouse_down: list[int], mouse_up: list[int]):

        if self.get_input(pygame.K_UP): self.player_scale += .02
        elif self.get_input(pygame.K_DOWN): self.player_scale -= .02
        self.player_scale = round(max(self.MIN_SCALE, min(self.player_scale, self.MAX_SCALE)), 2)

        if self.get_input(pygame.K_w): self.player_pos.y += self.SPRENT_SPEED if self.get_input(pygame.K_LSHIFT) else round(self.SPEED * self.player_scale)
        if self.get_input(pygame.K_a): self.player_pos.x += self.SPRENT_SPEED if self.get_input(pygame.K_LSHIFT) else round(self.SPEED * self.player_scale)
        if self.get_input(pygame.K_s): self.player_pos.y -= self.SPRENT_SPEED if self.get_input(pygame.K_LSHIFT) else round(self.SPEED * self.player_scale)
        if self.get_input(pygame.K_d): self.player_pos.x -= self.SPRENT_SPEED if self.get_input(pygame.K_LSHIFT) else round(self.SPEED * self.player_scale)

        if self.get_hotkey(pygame.K_LCTRL, pygame.K_h):
            self.player_pos = Vector2(0, 0)
        if self.get_hotkey(pygame.K_LSHIFT, pygame.K_m):
            self.player_scale = 1.0
        if self.get_hotkey(pygame.K_LCTRL, pygame.K_c):
            self.blocks.clear()
        if pygame.K_F1 in keys_down:
            self.DEBUG = not self.DEBUG

        if 1 in mouse_down:
            self.add_block()
        
        if self.get_hotkey(pygame.K_LSHIFT, pygame.K_1, pygame.K_2, pygame.K_3):
            print("Hello world!")
        
        if self.get_input(pygame.K_RSHIFT): self.add_block()
    
    def add_block(self):
        # ((offset // block_size) * block_size)
        pos = Vector2(
            (round((self.block_pos.x - self.player_pos.x) / self.player_scale) // self.BLOCK_SIZE) * self.BLOCK_SIZE,
            (round((self.block_pos.y - self.player_pos.y) / self.player_scale) // self.BLOCK_SIZE) * self.BLOCK_SIZE,
        ) 
        # round(self.block_pos / self.player_scale) - self.player_pos # + self.screen_vec2

        pos_key = vec2str(pos)

        if self.blocks.get(pos_key): return
        
        size = Vector2(
            self.BLOCK_SIZE,
            self.BLOCK_SIZE
        )

        self.blocks[pos_key] = NoneBlock(pos, size)
        print("Block added in pos:", pos_key)

    def draw(self):
        self.win.fill(self.BACKGROUND_COLOR)
        self.draw_blocks()
        self.draw_mouse()
        self.draw_grid()
        
    def draw_blocks(self):
        # [block.draw(self.win, block.toLocalPos(self.player_pos, self.player_scale), self.player_scale) for block in self.blocks.values() if block.toLocalPos(self.player_pos, self.player_scale).x + self.block_size > 0 and block.toLocalPos(self.player_pos, self.player_scale).x < self.width and block.toLocalPos(self.player_pos, self.player_scale).y + self.block_size > 0 and block.toLocalPos(self.player_pos, self.player_scale).y < self.height]
        # blocks_to_
        for block in self.blocks.values():
            local_pos = block.toLocalPos(self.player_pos, self.player_scale)

            if local_pos.x + self.block_size > 0 and local_pos.x < self.width and local_pos.y + self.block_size > 0 and local_pos.y < self.height:
                block.draw(self.win, local_pos, self.player_scale)
                if self.DEBUG:
                    self.draw_text(local_pos, block.pos, 
                                font_scale=round(14*self.player_scale), 
                                pos_x=local_pos.x + 5 * self.player_scale, 
                                pos_y=local_pos.y + 5 * self.player_scale)


    
    """
    class Block:
        pos = (0, 0) # (x, y)
        def __init__(self, pos: tuple[int, int]): # pos - (x, y)
            self.pos = pos
        
        def draw(self):
            ...
    
    width, height = (500, 500)
    block_size = 50

    block_out = Block((-150, 150)) # Блок вне экрана
    block_in = Block((150, 150)) # Блок на экрана

    blocks = {
    f"{block_out.pos[0]}:{block_out.pos[1]}": block_out,
    f"{block_in.pos[0]}:{block_in.pos[1]}": block_in
    }
    for pos, block in blocks.items():
        \"""
        Если блок вне экрана, то мы его пропускаем
        Если блок на экране, вызываем block.draw()
        \"""

    """

    def draw_mouse(self):
        s = pygame.Surface((self.block_size, self.block_size), pygame.SRCALPHA)
        color = (
            self.CURSOR_COLOR.r, 
            self.CURSOR_COLOR.g, 
            self.CURSOR_COLOR.b, 
            round(255 * self.coursore_color)
            )
        
        s.fill(color=color)

        self.win.blit(s, (self.block_pos.x, self.block_pos.y))
        if self.DEBUG:
            self.draw_text(self.block_pos, self.mouse_pos, 
                        font_scale=round(14*self.player_scale), 
                        pos_x=self.block_pos.x + 5 * self.player_scale, 
                        pos_y=self.block_pos.y + 5 * self.player_scale)

    def draw_text(self, *text_lines, font_scale: int, pos_x: float, pos_y: float, color: Color = Color(0, 0, 0)):
        font = pygame.font.Font(None, font_scale)
        text_surfaces: list[Surface] = [font.render(str(line), True, color) for line in text_lines]
        [self.win.blit(surface, (pos_x, pos_y := 10 + pos_y)) for surface in text_surfaces]


    def draw_grid(self):
        offset = (
            round(self.player_pos.x % self.block_size),
            round(self.player_pos.y % self.block_size)
        )
        lines_cord = get_grid(offset, self.block_size, (self.width, self.height))
        pygame.draw.lines(self.win, self.GRID_COLOR, False, lines_cord, width=round(6*self.player_scale))
    
    def grid_alignment(self, pos: Vector2):
        offset = Vector2(
            round(self.player_pos.x % self.block_size),
            round(self.player_pos.y % self.block_size)
        )

        return Vector2(
            (((pos.x - offset.x) // self.block_size) * self.block_size) + offset.x,
            (((pos.y - offset.y) // self.block_size) * self.block_size) + offset.y,
        )
    
"""

Как увеличить количество кадров?
Если на экране больше 50 блоков, то fps падает до 5-15
pygame, python 3.11
Код:
for block in self.blocks.values():
    local_pos = block.toLocalPos(self.player_pos, self.player_scale)
    if local_pos.x + self.block_size > 0 and local_pos.x < self.width and local_pos.y + self.block_size > 0 and local_pos.y < self.height:
        # pygame draw rect code


"""