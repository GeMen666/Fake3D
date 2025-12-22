# status.py ：全局数据层（所有跨文件共享的数据都存在这里）

# 地图数据
map_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# 游戏配置
TILE_SIZE = 64
MOVE_STEP = 1

# 玩家状态
player_x = 96.0
player_y = 96.0
player_speed = 1
view_angle = 0.0


# 游戏状态
paused = False
mouse_visible = False
mouse_grabbed = True
rel_x = 0
rel_y = 0

# 按键状态
key_states = {
    'up': False,
    'down': False,
    'left': False,
    'right': False
}


processing_grid = [
    [False for _ in range(len(map_data[0]))]
    for _ in range(len(map_data))
]
nodes = []          # 所有节点列表（像素坐标）
valid_nodes = {}    # 节点是否在视野内：{(x,y): True/False} （像素坐标）