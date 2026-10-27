# utils 提供一些通用的函数
# src\utils.py

import core.game_state as st
import math
import config as conf


# 获取节点的所在格子向下取整（像素坐标 -> 方格引索）
def get_floor_position(x, y):
    pos_x = math.floor(x // conf.TILE_SIZE)
    pos_y = math.floor(y // conf.TILE_SIZE)
    return pos_x, pos_y


# 获取格子的边界 （方格引索 -> 像素坐标）
def get_tile_border(x, y):
    # 边界顺序：上边界0、右边界1、下边界2、左边界3
    #           上边界0                    右边界1                下边界2              左边界3
    return y * conf.TILE_SIZE, (x + 1) * conf.TILE_SIZE, (y + 1) * conf.TILE_SIZE, x * conf.TILE_SIZE

# 检查坐标是否合法
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
