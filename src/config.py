# config 存放配置数据
# src\config.py

WINDOW_WIDTH = 1024   # 窗口宽度

WINDOW_HEIGHT = 576   # 窗口高度

FPS = 200      # 目标帧率

MOUSE_SENSITIVITY = 0.1  # 鼠标灵敏度（越小越慢，越大越快）

YAW_RANGE = 360        # 水平角度范围（取模360°循环）

FOV = 80            # 视野角度

SCALE = 0.15        # 小地图缩放

BASED_POS = (5, 5)  # 基础位置

BASED_HEIGHT = 70   # 基础高度


RAY_STEP = 3    # 射线步进

HORIZON = WINDOW_HEIGHT // 2 - 150   # 地平线位置

WALL_HEIGHT = 128       # 墙体高度

TILE_SIZE = 64          # 方格边长

G = 9.8                 # 重力加速度

JUMP_SPEED = 80         # 跳跃速度

CROUCH_SPEED = 50       # 下蹲速度

# 投影常数
PROJECTION_CONST = 100

# 最大有效距离（防止除零）
MAX_DISTANCE = 100      

