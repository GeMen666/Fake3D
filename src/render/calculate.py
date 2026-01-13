# calculate.py - Bresenham算法

from utils import check_index_valid
import math
import config as conf
from core import game_state as st

def dda_simple(start_x, start_y, angle_rad):
    """
    超简化版DDA
    参数 angle_rad: 射线角度（弧度）
    """
    # 射线方向（使用弧度计算）
    ray_dir_x = math.cos(angle_rad)
    ray_dir_y = math.sin(angle_rad)
    
    # 起始点
    x = start_x
    y = start_y
    
    # 每次前进的步长
    step = 2
    
    # 最大步数限制
    max_steps = int(conf.TILE_SIZE * 20 / step)
    
    for i in range(max_steps):
        # 检查当前网格
        map_x = int(x // conf.TILE_SIZE)
        map_y = int(y // conf.TILE_SIZE)
        
        # 边界检查
        if (map_x < 0 or map_x >= len(st.map_data[0]) or 
            map_y < 0 or map_y >= len(st.map_data)):
            distance = math.sqrt((x - start_x)**2 + (y - start_y)**2)
            return distance, x, y
        
        # 检查是否击中墙体
        if st.map_data[map_y][map_x] > 0:
            distance = math.sqrt((x - start_x)**2 + (y - start_y)**2)
            return distance, x, y
        
        # 向前移动
        x += ray_dir_x * step
        y += ray_dir_y * step
    
    # 达到最大步数，返回最大距离
    distance = math.sqrt((x - start_x)**2 + (y - start_y)**2)
    return distance, x, y



def Bresenham(start_x, start_y, angle_rad):

    def along_line(x1, y1, x2, y2):
        node = (float('inf'), float('inf'))
        rate = (y2 - y1) / (x2 - x1)
        correction = 1 if x1 < x2 else -1
        for cur_x in range(int(x1 / conf.TILE_SIZE) * conf.TILE_SIZE, int(x2), conf.TILE_SIZE * correction):
            if not (min(x1, x2) < cur_x < max(x1, x2)): continue
            cur_y = (cur_x - x1) * rate + y1
            if check_hit(cur_x, cur_y):
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

    def get_closest_point(x1, y1, x2, y2, x3, y3):
        distance1 = (x2 - x1)**2 + (y2 - y1)**2
        distance2 = (x3 - x1)**2 + (y3 - y1)**2
        return distance1 >= distance2
        
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
    

    max_distance = math.sqrt(len((st.map_data[0]) * conf.TILE_SIZE) ** 2 + (len(st.map_data) * conf.TILE_SIZE) ** 2)
    end_x = start_x + math.cos(angle_rad) * max_distance
    end_y = start_y + math.sin(angle_rad) * max_distance

    node = along_line(start_x, start_y, end_x, end_y)
    if end_x - start_x == 0: end_y += 0.0000000000000001

    distance = math.sqrt((node[0] - start_x)**2 + (node[1] - start_y)**2)


    return distance, node[0], node[1]





