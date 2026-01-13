# engine 游戏计算

import math
import game_state as st
import config as conf
from utils import *


def player_move(direction):
    angle = 0
    if direction == 'w':
        angle = math.radians(st.view_angle)
    elif direction == 's':
        angle = math.radians(st.view_angle + 180)
    elif direction == 'a':
        angle = math.radians(st.view_angle - 90)
    elif direction == 'd':
        angle = math.radians(st.view_angle + 90)

    try_x = st.player_x + math.cos(angle) * st.player_speed
    try_y = st.player_y + math.sin(angle) * st.player_speed


    st.player_x, st.player_y = check_player_move(try_x, try_y)

    

def check_player_move(try_x, try_y):
    map_width = len(st.map_data[0]) * st.TILE_SIZE
    map_height = len(st.map_data) * st.TILE_SIZE

    try_x = max(0, min(try_x, map_width - 1))
    try_y = max(0, min(try_y, map_height - 1))


    player_tile_x, player_tile_y = get_floor_position(try_x, try_y)

    if st.map_data[player_tile_y][player_tile_x] == 1:

        top, right, bottom, left = get_tile_border(player_tile_x, player_tile_y)
        
        border_distances = [
            try_y - top,      # 上边界距离
            right - try_x,    # 右边界距离
            bottom - try_y,   # 下边界距离
            try_x - left      # 左边界距离
        ]
        
        directions = list(range(4))
        directions.sort(key=lambda i: border_distances[i])
        
        original_try_x, original_try_y = try_x, try_y
        
        # 尝试四个方向，寻找可行的移动路径
        for direction in directions:
            temp_x, temp_y = original_try_x, original_try_y
            
            if direction == 0:  # 向上移动：从墙体顶部推出
                    temp_y = st.player_y
                    
            elif direction == 1:  # 向右移动：从墙体右侧推出
                    temp_x = st.player_x
                    
            elif direction == 2:  # 向下移动：从墙体底部推出
                    temp_y = st.player_y
                    
            elif direction == 3:  # 向左移动：从墙体左侧推出
                    temp_x = st.player_x
            
            if temp_x != original_try_x or temp_y != original_try_y:
                new_tile_x, new_tile_y = get_floor_position(temp_x, temp_y)
                if st.map_data[new_tile_y][new_tile_x] == 0:
                    try_x, try_y = temp_x, temp_y
                    break
        
        
        if try_x == original_try_x and try_y == original_try_y:
            return st.player_x, st.player_y
    
    return try_x, try_y
