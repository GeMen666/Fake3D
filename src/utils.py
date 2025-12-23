# utils 提供一些通用的函数

import status as st
import math


def get_ceil_position(x, y):
    pos_x = math.ceil(x / st.TILE_SIZE)
    pos_y = math.ceil(y / st.TILE_SIZE)
    return pos_x, pos_y

def get_floor_position(x, y):
    pos_x = math.floor(x / st.TILE_SIZE)
    pos_y = math.floor(y / st.TILE_SIZE)
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
    
def get_tile_border(x, y):
    #           上边界0                    右边界1                下边界2              左边界3
    return y * st.TILE_SIZE, (x + 1) * st.TILE_SIZE, (y + 1) * st.TILE_SIZE, x * st.TILE_SIZE