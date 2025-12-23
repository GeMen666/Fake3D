# engine 游戏计算
import math
import status as st  # 使用别名 st
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
    
    pre_x = st.player_x
    pre_y = st.player_y

    st.player_x = st.player_x + math.cos(angle) * st.player_speed
    st.player_y = st.player_y + math.sin(angle) * st.player_speed

    limit_player_position(pre_x, pre_y)


def limit_player_position(pre_x, pre_y):

    map_width = len(st.map_data[0]) * st.TILE_SIZE * conf.SCALE
    map_height = len(st.map_data) * st.TILE_SIZE * conf.SCALE

    # player_screen_y = conf.BASED_POS[1] + st.player_y * conf.SCALE
    # 屏幕上画出来的玩家已经是缩放的，所以player_y * conf.SCALE 已经是屏幕上的坐标了
    if st.player_x < 0:
        st.player_x = 0
    elif st.player_x >= map_width:
        st.player_x = map_width - 1

    if st.player_y < 0:
        st.player_y = 0
    elif st.player_y >= map_height:
        st.player_y = map_height - 1

    player_pos = get_floor_position(st.player_x, st.player_y)
    if st.map_data[player_pos[1]][player_pos[0]] == 1:
        border = get_tile_border(player_pos[0], player_pos[1])
        per_pos = get_floor_position(pre_x, pre_y)
        if per_pos[0] != player_pos[0] and per_pos[1] != player_pos[1]:
            if player_pos[0] + 1 == per_pos[0] and player_pos[1] + 1 == per_pos[1]: # 右下
                st.player_x = border[1] + 1
            elif player_pos[0] + 1 == per_pos[0] and player_pos[1] - 1 == per_pos[1]: # 左下
                st.player_x = border[1] + 1
            elif player_pos[0] - 1 == per_pos[0] and player_pos[1] + 1 == per_pos[1]: # 左上
                st.player_x = border[3] - 1
            elif player_pos[0] - 1 == per_pos[0] and player_pos[1] - 1 == per_pos[1]: # 右上
                st.player_x = border[3] - 1
        else:
            if per_pos[0] != player_pos[0]:
                if per_pos[0] == player_pos[0] + 1:
                    st.player_x = border[1] + 1
                elif per_pos[0] == player_pos[0] - 1:
                    st.player_x = border[3] - 1
            if per_pos[1] != player_pos[1]:
                if per_pos[1] == player_pos[1] + 1:
                    st.player_y = border[2] + 1
                elif per_pos[1] == player_pos[1] - 1:
                    st.player_y = border[0] - 1





    



