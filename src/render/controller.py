# controller.py - 渲染控制器
# src\render\controller.py

from core import game_state as st
from .calculate import Bresenham
import config as conf
import math

ray_data = {}

def generate_camera_rays():
    
    # 计算每条射线
    for i in range(0, conf.WINDOW_WIDTH, conf.RAY_STEP):
        # 注意：FOV 是角度，view_angle 是角度
        # 计算当前射线的角度（角度）
        ray_angle_deg = (st.view_angle - conf.FOV / 2 + (conf.FOV * i / conf.WINDOW_WIDTH)) % 360
        
        # 转换为弧度用于三角函数
        ray_angle_rad = math.radians(ray_angle_deg)
        
        # Bresenham 算法（传入弧度）
        distance, hit_x, hit_y = Bresenham(st.player_x, st.player_y, ray_angle_rad)

        # 计算透视效果
        height, jump_offset, y1, y2 = compute_perspective(distance, ray_angle_rad)


        # 存储结果
        for j in range(0, conf.RAY_STEP):
            ray_data[i-j] = {
                'y1': y1,
                'y2': y2,
                'height': height,
                'hit_x': hit_x,
                'hit_y': hit_y,
                'distance': distance,
                'jump_offset': jump_offset
            }
        

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
    jump_offset = st.jump_height * (conf.PROJECTION_CONST / distance)

    # 绘制3D墙（在主视图上）
    y1 = (conf.HORIZON - height) / 2 + conf.BASED_HEIGHT  + st.vertical_view
    y2 = y1 + height

    return height, jump_offset, y1, y2
    



def all_calculate():
    ray_data.clear()
    generate_camera_rays()
