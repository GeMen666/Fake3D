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
    # 地图边界检查（使用实际地图尺寸，不使用SCALE）
    map_width = len(st.map_data[0]) * st.TILE_SIZE
    map_height = len(st.map_data) * st.TILE_SIZE

    if st.player_x < 0:
        st.player_x = 0
    elif st.player_x >= map_width:
        st.player_x = map_width - 1

    if st.player_y < 0:
        st.player_y = 0
    elif st.player_y >= map_height:
        st.player_y = map_height - 1

    # 获取当前玩家所在瓦片位置
    player_tile_x, player_tile_y = get_floor_position(st.player_x, st.player_y)

    # 检查是否撞墙
    if (0 <= player_tile_y < len(st.map_data) and
            0 <= player_tile_x < len(st.map_data[0]) and
            st.map_data[player_tile_y][player_tile_x] == 1):

        # 获取墙体边界
        top, right, bottom, left = get_tile_border(player_tile_x, player_tile_y)

        # 获取之前位置的瓦片坐标
        prev_tile_x, prev_tile_y = get_floor_position(pre_x, pre_y)

        # 根据移动方向进行碰撞响应
        if prev_tile_x != player_tile_x:
            # 水平方向移动导致碰撞
            if prev_tile_x < player_tile_x:
                # 从左向右移动进入墙体，将玩家推回左侧
                st.player_x = left - 0.1
            else:
                # 从右向左移动进入墙体，将玩家推回右侧
                st.player_x = right + 0.1

        if prev_tile_y != player_tile_y:
            # 垂直方向移动导致碰撞
            if prev_tile_y < player_tile_y:
                # 从上向下移动进入墙体，将玩家推回上侧
                st.player_y = top - 0.1
            else:
                # 从下向上移动进入墙体，将玩家推回下侧
                st.player_y = bottom + 0.1

        # 二次检查：确保修正后的位置不在墙内
        final_tile_x, final_tile_y = get_floor_position(st.player_x, st.player_y)
        if (0 <= final_tile_y < len(st.map_data) and
                0 <= final_tile_x < len(st.map_data[0]) and
                st.map_data[final_tile_y][final_tile_x] == 1):
            # 如果仍然在墙内，回滚到之前位置
            st.player_x = pre_x
            st.player_y = pre_y



    



