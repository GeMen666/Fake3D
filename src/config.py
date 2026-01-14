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

BASED_HEIGHT = 70

TEST_BASED = (0,0)

TEST_SCALE = 1

RAY_STEP = 3

HORIZON = WINDOW_HEIGHT / 2

WALL_SCALE = 128

TILE_SIZE = 64

G = 9.8

JUMP_SPEED = 80


# 小地图配色
MINIMAP_WALL_COLOR = (120, 100, 80)       # 墙体 - 土黄色调
MINIMAP_WALL_BORDER = (180, 150, 120)     # 墙体边框 - 浅土黄
MINIMAP_FLOOR_COLOR = (70, 70, 90)        # 空地 - 深灰蓝色
MINIMAP_FLOOR_BORDER = (100, 100, 120)    # 空地边框 - 灰蓝色

# 射线交点和3D墙配色
RAY_HIT_COLOR = (255, 200, 100)           # 射线交点 - 亮橙色
RAY_HIT_SIZE = 2                          # 交点大小

# 3D墙体颜色（基于距离的渐变）
WALL_NEAR_COLOR = (200, 180, 140)         # 近处墙 - 浅棕色
WALL_FAR_COLOR = (120, 100, 80)           # 远处墙 - 深棕色
WALL_COLOR_RANGE = 1000                   # 颜色渐变范围

# 天空和地板颜色（如果后续添加3D视图）
SKY_COLOR = (135, 206, 235)               # 天空蓝
FLOOR_COLOR = (80, 70, 60)                # 地板棕
