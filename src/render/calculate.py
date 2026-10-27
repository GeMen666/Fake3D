# calculate.py - resenham算法 光线投射算法 + 透视投影修正 + 偏移量修正
# src\render\calculate.py

from utils import check_index_valid
import math
import config as conf
from core import game_state as st

# 优化后的Bresenham，计算射线与墙体的交点
def Bresenham(start_x, start_y, angle_rad):

    # 沿着网格线查找墙体交点
    def along_line(x1, y1, x2, y2):
        node = (float('inf'), float('inf')) # 射线与墙体的交点
        if x2 - x1 == 0: y2 += 0.0000000000000001 # 除零保护
        rate = (y2 - y1) / (x2 - x1)
        correction = 1 if x1 < x2 else -1
        for cur_x in range(int(x1 / conf.TILE_SIZE) * conf.TILE_SIZE, int(x2), conf.TILE_SIZE * correction):
            if not (min(x1, x2) < cur_x < max(x1, x2)): continue
            cur_y = (cur_x - x1) * rate + y1
            if check_hit(cur_x, cur_y): # 在命中墙壁的交点中找出离玩家最近的一个交点
                if get_closest_point(x1, y1, node[0], node[1], cur_x, cur_y):
                    node = (cur_x, cur_y)
        correction = 1 if y1 < y2 else -1
        for cur_y in range(int(y1 / conf.TILE_SIZE) * conf.TILE_SIZE, int(y2), conf.TILE_SIZE * correction):
            if not (min(y1, y2) < cur_y < max(y1, y2)): continue
            cur_x = (cur_y - y1) / rate + x1
            if check_hit(cur_x, cur_y):
                if get_closest_point(x1, y1, node[0], node[1], cur_x, cur_y):
                    node = (cur_x, cur_y)
        return node

    # 获取离玩家最近的点
    def get_closest_point(x1, y1, x2, y2, x3, y3):
        distance1 = (x2 - x1)**2 + (y2 - y1)**2
        distance2 = (x3 - x1)**2 + (y3 - y1)**2
        return distance1 >= distance2
    
    # 检查是否命中墙壁
    def check_hit(x, y):
        if x % conf.TILE_SIZE == 0:
            index_x1, index_x2, index_y = int(x / conf.TILE_SIZE), int(x / conf.TILE_SIZE) - 1, int(y / conf.TILE_SIZE)
            if check_index_valid(index_x1, index_y) and st.map_data[index_y][index_x1] == 1:
                return True
            if check_index_valid(index_x2, index_y) and st.map_data[index_y][index_x2] == 1:
                return True
        elif y % conf.TILE_SIZE == 0:
            index_y1, index_y2, index_x = int(y / conf.TILE_SIZE), int(y / conf.TILE_SIZE) - 1, int(x / conf.TILE_SIZE)
            if check_index_valid(index_x, index_y1) and st.map_data[index_y1][index_x] == 1:
                return True
            if check_index_valid(index_x, index_y2) and st.map_data[index_y2][index_x] == 1:
                return True
        return False
    

    max_distance = math.sqrt(len((st.map_data[0]) * conf.TILE_SIZE) ** 2 + (len(st.map_data) * conf.TILE_SIZE) ** 2) # 最长距离
    end_x = start_x + math.cos(angle_rad) * max_distance # 最远点
    end_y = start_y + math.sin(angle_rad) * max_distance # 最远点

    node = along_line(start_x, start_y, end_x, end_y)

    distance = math.sqrt((node[0] - start_x)**2 + (node[1] - start_y)**2)


    return distance, node[0], node[1]

        
# 光线投射算法 + 透视投影修正 + 偏移量修正
def compute_perspective(distance, ray_angle_rad):
    # 修正鱼眼效应
    view_angle_rad = math.radians(st.view_angle)  # 转换为弧度
    angle_diff = ray_angle_rad - view_angle_rad
    
    # 规范化角度差到 -π 到 π 范围
    while angle_diff > math.pi:
        angle_diff -= 2 * math.pi
    while angle_diff < -math.pi:
        angle_diff += 2 * math.pi
    
    distance *= math.cos(angle_diff)

    height = conf.WALL_HEIGHT * conf.WINDOW_HEIGHT / distance

    # 跳跃屏幕偏移
    offset = st.jump_height + st.crouch_height

    offset = offset * (conf.PROJECTION_CONST / distance)

    # 绘制3D墙（在主视图上）
    y1 = (conf.HORIZON - height) / 2 + conf.BASED_HEIGHT  + st.vertical_view
    y2 = y1 + height

    return height, offset, y1, y2
    
