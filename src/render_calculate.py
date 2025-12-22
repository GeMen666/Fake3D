# render.calculate.py   提供计算

import queue
import math
from .render_utils import *
from .. import config as conf
from .. import status as st
from ..utils import get_player_position

processing_grid = [
    [
        False for _ in range(len(st.map_data[0]))  # 列数
    ]
    for _ in range(len(st.map_data))  # 行数
]

visited_grid = [
    [
        False for _ in range(len(st.map_data[0]))  # 列数
    ]
    for _ in range(len(st.map_data))  # 行数
]

q = queue.Queue()


def select_forward_tile ():
    global q
    player_pos = get_player_position()
    if 315 <= st.view_angle < 360 or st.view_angle < 45:
        q.put((player_pos[0]+1,player_pos[1]))
    elif 45 <= st.view_angle < 135:
        q.put((player_pos[0],player_pos[1]+1))
    elif 135 <= st.view_angle < 225:
        q.put((player_pos[0]-1,player_pos[1]))
    elif 225 <= st.view_angle < 315:
        q.put((player_pos[0],player_pos[1]-1))



def bfs_select_tile():
    global q, processing_grid, visited_grid
    reset_grids()
    while not q.empty():
        cur_pos = q.get()
        visited_grid[cur_pos[0]][cur_pos[1]] = True
        if check_current_tile(cur_pos):
            processing_grid[cur_pos[0]][cur_pos[1]] = True
            if cur_pos[0]+1 < len(st.map_data) and visited_grid[cur_pos[0]+1][cur_pos[1]] == False:
                q.put((cur_pos[0]+1,cur_pos[1]))
            elif cur_pos[1]+1 < len(st.map_data[0]) and visited_grid[cur_pos[0]][cur_pos[1]+1] == False:
                q.put((cur_pos[0],cur_pos[1]+1))
            elif cur_pos[0]-1 >= 0 and visited_grid[cur_pos[0]-1][cur_pos[1]] == False:
                q.put((cur_pos[0]-1,cur_pos[1]))
            elif cur_pos[1]-1 >= 0 and visited_grid[cur_pos[0]][cur_pos[1]-1] == False:
                q.put((cur_pos[0],cur_pos[1]-1))
        else:
            continue
    print_visited_grid()


def check_current_tile(tile_pos):
    tile_x, tile_y = tile_pos[1], tile_pos[0]
    corners = [
        (0, 0),  # 左上
        (1, 0),  # 右上
        (1, 1),  # 右下
        (0, 1)   # 左下
    ]
    view_angle_rad = math.radians(st.view_angle)
    fov_rad = math.radians(conf.FOV)
    angle_left = (view_angle_rad - fov_rad / 2) % (2 * math.pi)
    angle_right = (view_angle_rad + fov_rad / 2) % (2 * math.pi)

    for dx, dy in corners:
        node_x = (tile_x + dx) * st.TILE_SIZE
        node_y = (tile_y + dy) * st.TILE_SIZE
        delta_x = node_x - st.player_x
        delta_y = node_y - st.player_y
        node_angle = math.atan2(delta_y, delta_x) % (2 * math.pi)
        if angle_left <= angle_right:
            if angle_left <= node_angle <= angle_right:
                return True
        else:
            if node_angle >= angle_left or node_angle <= angle_right:
                return True

    return False


