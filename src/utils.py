# utils 提供一些通用的函数

import status as st
import math


def get_ceil_position(x, y):
    pos_x = math.ceil(x / st.TILE_SIZE)
    pos_y = math.ceil(y / st.TILE_SIZE)
    return pos_x, pos_y

# 获取节点的所在格子向下取整（像素坐标 -> 方格引索）
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



# 获取格子的边界 （方格引索 -> 像素坐标）
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
    elif direction == 2 and x < len(st.map_data[0]) - 1:
        return (x + 1) * st.TILE_SIZE, y * st.TILE_SIZE
    # 3：右下
    elif direction == 3 and y < len(st.map_data) - 1:
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
    
def check_index_valid(x, y):
    return 0 <= x < len(st.map_data[0]) and 0 <= y < len(st.map_data)
     


def check_line_intersect(a1, a2, b1, b2):

    # 计算叉积
    def cross_product(p1, p2):
        return p1[0] * p2[1] - p2[0] * p1[1]

    # 计算向量
    def vector(a, b):
        return (b[0] - a[0], b[1] - a[1])

    # 判断点是否在线段上
    def point_on_segment(p, a, b):
        in_x_range = min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
        in_y_range = min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
        collinear = cross_product(vector(a, b), vector(a, p)) == 0
        return in_x_range and in_y_range and collinear

    # 核心判断逻辑
    c1 = cross_product(vector(a1, b1), vector(a1, b2))
    c2 = cross_product(vector(a2, b1), vector(a2, b2))
    c3 = cross_product(vector(b1, a1), vector(b1, a2))
    c4 = cross_product(vector(b2, a1), vector(b2, a2))

    # 严格跨立（非共线交叉）
    if (c1 * c2 < 0) and (c3 * c4 < 0):
        return True

    # 共线/端点重合场景
    if c1 == 0 and point_on_segment(b1, a1, a2):
        return True
    if c2 == 0 and point_on_segment(b2, a1, a2):
        return True
    if c3 == 0 and point_on_segment(a1, b1, b2):
        return True
    if c4 == 0 and point_on_segment(a2, b1, b2):
        return True

    # 不相交
    return False
