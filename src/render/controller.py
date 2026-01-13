# controller.py - 修正后的控制器

from core import game_state as st
from .calculate import Bresenham
import config as conf
import math

nodes = {}

def all_calculate():
    nodes.clear()
    
    # 计算每条射线
    for i in range(0, conf.WINDOW_WIDTH, conf.RAY_STEP):
        # 注意：FOV 是角度，view_angle 是角度
        # 计算当前射线的角度（角度）
        ray_angle_deg = (st.view_angle - conf.FOV / 2 + (conf.FOV * i / conf.WINDOW_WIDTH)) % 360
        
        # 转换为弧度用于三角函数
        ray_angle_rad = math.radians(ray_angle_deg)
        
        # 使用简化的DDA算法（传入弧度）
        distance, hit_x, hit_y = Bresenham(
            st.player_x, 
            st.player_y, 
            ray_angle_rad  # 传入弧度
        )
        
        # 修正鱼眼效应
        view_angle_rad = math.radians(st.view_angle)  # 转换为弧度
        angle_diff = ray_angle_rad - view_angle_rad
        
        # 规范化角度差到 -π 到 π 范围
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        
        distance *= math.cos(angle_diff)

        height = conf.WALL_SCALE * conf.WINDOW_HEIGHT / distance
        
        # 存储结果
        for j in range(0, conf.RAY_STEP):
            nodes[i-j] = ( hit_x, hit_y, height, distance)
