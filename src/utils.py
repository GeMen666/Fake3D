# utils 提供一些通用的函数

import status as st
import math


def get_ceil_position():
    pos_x = math.ceil(st.player_x / st.TILE_SIZE)
    pos_y = math.ceil(st.player_y / st.TILE_SIZE)
    return pos_x, pos_y

def get_floor_position():
    pos_x = math.floor(st.player_x / st.TILE_SIZE)
    pos_y = math.floor(st.player_y / st.TILE_SIZE)
    return pos_x, pos_y


def get_tile_nodes(x, y):
    corners = [
        (0, 0), (0, 1), (1, 0), (1, 1)
    ]
    nodes = []
    for dx, dy in corners:
        node_x = (x + dx) * st.TILE_SIZE
        node_y = (y + dy) * st.TILE_SIZE
        nodes.append((node_x, node_y))
    return nodes
    