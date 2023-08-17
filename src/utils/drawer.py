# from numba import jit, int32, carray
# import numpy as np

# @jit(nopython=True)
# def get_grid(player_pos: list[int], grid_scale: int, win_size: list[float], lines_cord: np.ndarray = []):

#     width, height = round(win_size[0]), round(win_size[1])
#     player_pos_x, player_pos_y = player_pos

#     for x in range(round(player_pos_x % grid_scale), width, grid_scale * 2):
#         # x += player_pos.x
#         y = 0 # player_pos.y
#         lines_cord = np.append(lines_cord, np.array([x, y]))
#         lines_cord = np.append(lines_cord, np.array([x, y + height]))
#         lines_cord = np.append(lines_cord, np.array([x + grid_scale, y + height]))
#         lines_cord = np.append(lines_cord, np.array([x + grid_scale, y]))

#     lines_cord = np.append(lines_cord, np.array([width, 0]))
#     lines_cord = np.append(lines_cord, np.array([0, 0]))
    
#     for y in range(round(player_pos_y % grid_scale), height, grid_scale * 2):
#         x = 0 # player_pos.x
#         # y += player_pos.y

#         lines_cord = np.append(lines_cord, np.array([x, y]))
#         lines_cord = np.append(lines_cord, np.array([width + x, y]))
#         lines_cord = np.append(lines_cord, np.array([width + x, y + grid_scale]))
#         lines_cord = np.append(lines_cord, np.array([x, y + grid_scale]))

#     return lines_cord


# """
# def draw_grid(self):
#         lines_cord = []

#         for x in range(round(self.player_pos.x % self.grid_scale), self.width, self.grid_scale * 2):
#             # x += self.player_pos.x
#             y = 0 # self.player_pos.y
#             lines_cord.append(Vector2(x, y))
#             lines_cord.append(Vector2(x, y + self.height))
#             lines_cord.append(Vector2(x + self.grid_scale, y + self.height))
#             lines_cord.append(Vector2(x + self.grid_scale, y))
#             # lines_cord.append(Vector2(x + self.grid_scale, y + self.height))

#         lines_cord.append(Vector2(self.width, 0))
#         lines_cord.append(Vector2(0, 0))
        
#         # grid_scale_y = round(self.BLOCK_SIZE * self.player_scale) # self.height / 
#         for y in range(round(self.player_pos.y % self.grid_scale), self.height, self.grid_scale * 2):
#             x = 0 # self.player_pos.x
#             # y += self.player_pos.y

#             lines_cord.append(Vector2(x, y))
#             lines_cord.append(Vector2(self.width + x, y))
#             lines_cord.append(Vector2(self.width + x, y + self.grid_scale))
#             lines_cord.append(Vector2(x, y + self.grid_scale))

#         pygame.draw.lines(self.win, (0, 0, 0), False, lines_cord)
# """

from functools import cached_property, lru_cache
from pygame import Vector2

@lru_cache(maxsize=32)
def get_grid(offset: tuple[int, int], grid_scale: int, win_size: tuple[int, int]):
        lines_cord = []

        offset_x, offset_y = offset
        width, height = win_size

        for x in range(offset_x, width, grid_scale * 2):
            # x += self.player_pos.x
            y = 0 # self.player_pos.y
            lines_cord.append(Vector2(x, y))
            lines_cord.append(Vector2(x, y + height))
            lines_cord.append(Vector2(x + grid_scale, y + height))
            lines_cord.append(Vector2(x + grid_scale, y))
            # lines_cord.append(Vector2(x + grid_scale, y + height))


        lines_cord.append(Vector2(width, 0))
        # lines_cord.append(Vector2(width, height))
        # lines_cord.append(Vector2(width, 0))
        lines_cord.append(Vector2(0, 0))
        
        # grid_scale_y = round(self.BLOCK_SIZE * self.player_scale) # height / 
        for y in range(offset_y, height, grid_scale * 2):
            x = 0 # self.player_pos.x
            # y += self.player_pos.y

            lines_cord.append(Vector2(x, y))
            lines_cord.append(Vector2(width + x, y))
            lines_cord.append(Vector2(width + x, y + grid_scale))
            lines_cord.append(Vector2(x, y + grid_scale))
        
        # lines_cord.append(Vector2(0, height))
        # lines_cord.append(Vector2(width, height))
        # lines_cord.append(Vector2(0, height))
        # lines_cord.append(Vector2(0, 0))

        return lines_cord