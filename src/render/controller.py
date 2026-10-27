# controller.py - 渲染控制器
# src\render\controller.py

from core import game_state as st
from .calculate import Bresenham, compute_perspective
import config as conf
import math

ray_data = {}

# 计算射线
def generate_camera_rays():
    
    # 计算每条射线
    for i in range(conf.RAY_STEP, conf.WINDOW_WIDTH, conf.RAY_STEP):
        # RAY_STEP为射线步长，按照画布总像素宽度，按每RAY_STEP列像素计算一次射线
        # FOV ：视野范围角度，view_angle ：视线角度
        # 计算当前射线的角度（角度）
        ray_angle_deg = (st.view_angle - conf.FOV / 2 + (conf.FOV * i / conf.WINDOW_WIDTH)) % 360
        
        # 转换为弧度用于三角函数
        ray_angle_rad = math.radians(ray_angle_deg)
        
        # 优化后的Bresenham 算法（传入弧度）
        distance, hit_x, hit_y = Bresenham(st.player_x, st.player_y, ray_angle_rad)

        # 计算透视效果
        height, offset, y1, y2 = compute_perspective(distance, ray_angle_rad)


        # 存储结果
        for j in range(0, conf.RAY_STEP):
            ray_data[i-j] = {
                'y1': y1,
                'y2': y2,
                'height': height,
                'hit_x': hit_x,
                'hit_y': hit_y,
                'distance': distance,
                'offset': offset
            }



def all_calculate():
    ray_data.clear()
    generate_camera_rays()
