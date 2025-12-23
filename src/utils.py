# utils 提供一些通用的函数

import status as st
import math


def get_ceil_position(x, y):
    pos_x = math.ceil(x / st.TILE_SIZE)
    pos_y = math.ceil(y / st.TILE_SIZE)
    return pos_x, pos_y

# 获取节点的所在格子（像素坐标 -> 方格引索） （右下）
def get_floor_position(x, y):
    pos_x = math.floor(x / st.TILE_SIZE)
    pos_y = math.floor(y / st.TILE_SIZE)
    return pos_x, pos_y


# 获取格子的所有节点（4个角点, 像素坐标）
def get_tile_nodes(x, y):
    corners = [
        (0, 0), (0, 1), (1, 0), (1, 1)
    ]
    nodes = []
    for dx, dy in corners:
        node_x = (x + dx) * st.TILE_SIZE
        node_y = (y + dy) * st.TILE_SIZE
        nodes.append((node_x, node_y))
    # 节点顺序：上左0、上右1、下右2、下左3
    return nodes


# 获取格子的边界
def get_tile_border(x, y):
    # 边界顺序：上边界0、右边界1、下边界2、左边界3
    #           上边界0                    右边界1                下边界2              左边界3
    return y * st.TILE_SIZE, (x + 1) * st.TILE_SIZE, (y + 1) * st.TILE_SIZE, x * st.TILE_SIZE


# 获取格子某方向的节点的坐标（方格引索 -> 节点像素坐标） 1：左上 2：右上 3：右下 4：左下
def get_direction_node(x, y, direction):
    # 1：左上
    if direction == 1 and y > 0:
        return x * st.TILE_SIZE, y * st.TILE_SIZE
    # 2：右上
    elif direction == 2 and x < st.MAP_WIDTH - 1:
        return (x + 1) * st.TILE_SIZE, y * st.TILE_SIZE
    # 3：右下
    elif direction == 3 and y < st.MAP_HEIGHT - 1:
        return (x + 1) * st.TILE_SIZE, (y + 1) * st.TILE_SIZE
    # 4：左下
    elif direction == 4 and x > 0:
        return x * st.TILE_SIZE, (y + 1) * st.TILE_SIZE
    else:
        return -1
    

# 获取像素节点某方向的格子的坐标（节点像素坐标 -> 方格引索） 1：左上 2：右上 3：右下 4：左下
def get_direction_tile(x, y, direction):
    # 先获取节点所在的格子（右下）
    x, y = get_floor_position(x, y)
    # 1：左上
    if direction == 1 and x-1 >= 0 and y-1 >= 0:
        return x-1, y-1
    # 2：右上
    elif direction == 2 and y-1 >= 0:
        return x, y-1
    # 3：右下
    elif direction == 3:
        return x, y
    # 4：左下
    elif direction == 4 and x-1 >= 0:
        return x-1, y
    else:
        return -1
     
    