# config 存放配置数据
# src\config.py

WINDOW_WIDTH = 1024   # 窗口宽度

WINDOW_HEIGHT = 576   # 窗口高度

FPS = 200      # 目标帧率

MOUSE_SENSITIVITY = 0.1  # 鼠标灵敏度（越小越慢，越大越快）

YAW_RANGE = 360        # 水平角度范围（取模360°循环）

FOV = 80            # 视野角度

SCALE = 0.15

BASED_POS = (5, 5)  # 基础位置

BASED_HEIGHT = 70   # 基础高度


RAY_STEP = 3    # 射线步进

HORIZON = WINDOW_HEIGHT // 2 - 150   # 地平线位置

WALL_HEIGHT = 128

TILE_SIZE = 64

G = 9.8

JUMP_SPEED = 80

# 投影常数（关键！）
PROJECTION_CONST = 100

# 世界到像素的转换因子
WORLD_TO_PIXEL = 50

# 最大有效距离（防止除零）
MAX_DISTANCE = 100      

