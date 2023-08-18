from abc import ABC, abstractclassmethod, abstractmethod
import json
from pygame import Color, Surface, Vector2
from pygame.event import Event
from src.IBlock import IBlock
from src.blocks import Blocks
from pgu import gui
from src.utils.settings import Main
from src.utils.other import LOAD_FILE, SAVE_FILE
import pygame


class Engine(ABC):

    blocks: Blocks[str, IBlock] = Blocks[str, IBlock]()

    player_pos = Vector2(0, 0)
    player_scale = 1

    BLOCK_SIZE = 50
    SPEED = 5

    FPS = 60
    FPS_NOW = 0

    FPS_MIN = 0
    FPS_MAX = 0
    FPS_AVG = 0

    _app = gui.App()
    _settings = Main(align=0,valign=0)
    SETTINGS = False

    _min_max_fps = [0]
    PER_SEC_FPS_MIN_MAX = 5


    _delta = 0

    input_keys: dict[str, bool] = {}

    def __init__(self, win: Surface) -> None:
        self.win = win

        self.width = win.get_width()
        self.height = win.get_height()

        # self._app.init(self._settings)
        
        self.clock = pygame.time.Clock()
        

    @abstractmethod
    def update(self, delta: float):
        ...

    @abstractmethod
    def input(self, keys_down: list[int], keys_up: list[int], mouse_down: list[int], mouse_up: list[int]):
        ...

    @abstractmethod
    def draw(self):
        ...
    @abstractmethod
    def fixed_update(self):
        ...

    def get_input(self, key: int) -> bool:
        return not not self.input_keys.get(str(key))
    
    def get_hotkey(self, *keys: int):
        """
        Checks if the passed arguments are hotkeys.

        :param keys: Integers representing hotkeys.
        :return: True if all passed arguments are hotkeys.
        """
        return all((self.input_keys.get(str(keys[i])) if i < len(keys) - 1 else keys[-1] in self.keys_down) for i in range(len(keys)))

    def _set_input(self, key: int, pressed=True):
        self.input_keys[str(key)] = pressed

    def open_settings(self):
        self._settings.continue_btn.connect(gui.CLICK, self.close_settings, None)
        self._background_settings = self.win.copy()
        self._app.init(self._settings)
        self.SETTINGS = True

    def close_settings(self, _ = None):
        self.SETTINGS = False
        self._app.exit(self._app)

    def _event(self, events: list[Event]):
        
        keys_down = []
        keys_up = []

        mouse_down = []
        mouse_up = []

        for event in events:
            if self.SETTINGS:
                self._app.event(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                self._set_input(event.key)
                keys_down.append(event.key)
            elif event.type == pygame.KEYUP:
                self._set_input(event.key, False)
                keys_up.append(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down.append(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_up.append(event.button)
            elif event.type == LOAD_FILE:
                self.blocks.load(event.file_path) # type: ignore
            elif event.type == SAVE_FILE:
                self.blocks.save(event.file_path) # type: ignore

        return keys_down, keys_up, mouse_down, mouse_up

    def _game_update(self, keys: tuple[list, list, list, list]):
        self.input(*keys)
        self.update(self.clock.get_time() / 1000)
        self.draw()

    def _settings_update(self):
        self.win.blit(self._background_settings, (0,0))
        self._app.paint()

    def start(self):
        while True:
            self.clock.tick(self.FPS)

            self._min_max_fps.append(self.FPS_NOW)

            self.FPS_NOW = round(self.clock.get_fps())
            self.FPS_MAX = max(self._min_max_fps)
            self.FPS_MIN = min(self._min_max_fps)
            self.FPS_AVG = max(sum(self._min_max_fps) / len(self._min_max_fps), 1)

            if len(self._min_max_fps) / self.FPS_AVG >= self.PER_SEC_FPS_MIN_MAX:
                self._min_max_fps = []

            # print(self.clock.get_time())
            self._delta += self.clock.get_time() / 1000
            if (self._delta) >= 1:
                self.fixed_update()
                self._delta = 0

            keys = self._event(pygame.event.get())
            self.keys_down, self.keys_up, self.mouse_down, self.mouse_up = keys
            if self.SETTINGS:
                self._settings_update()
            else:
                self._game_update(keys)
            pygame.display.update()
    # def _draw_grid(self):
        # lines_cord = []

        # grid_scale_x = round(self.BLOCK_SIZE * self.player_scale) # self.width / 
        # for x in range(round(self.player_pos.x % grid_scale_x), self.width, grid_scale_x):
        #     # x += self.player_pos.x
        #     y = 0 # self.player_pos.y
        #     lines_cord.append(Vector2(x, y))
        #     lines_cord.append(Vector2(x, y + self.height))
        #     lines_cord.append(Vector2(x + grid_scale_x, y + self.height))

        # lines_cord.append(Vector2(self.width, 0))
        # lines_cord.append(Vector2(0, 0))
        
        # grid_scale_y = round(self.BLOCK_SIZE * self.player_scale) # self.height / 
        # for y in range(round(self.player_pos.y % grid_scale_y), self.height, grid_scale_y):
        #     x = 0 # self.player_pos.x
        #     # y += self.player_pos.y

        #     lines_cord.append(Vector2(x, y))
        #     lines_cord.append(Vector2(self.width + x, y))
        #     lines_cord.append(Vector2(self.width + x, y + grid_scale_y))

        # pygame.draw.lines(self.win, (0, 0, 0), False, lines_cord)


"""
У меня есть класс (car) в классе есть декоратор (onKey), как мне обернуть метод класса в этот декоратор? python
Код:
class car:
    keyDown: dict[str, list] = {}
    
    def __init__() -> None:
        pass
    
    def onKey(self, key: int):
        def decorator(func):
            self.keyDown.setdefault(str(key), []).append(func)  # Добавление обработчика в соответствующий словарь
            return func
        return decorator

    @onKey(11)
    def foo(self):
        # Что-то делает... 
"""