import game_state as st

# 可见的格子队列
visible_grid = [
    [False for _ in range(len(st.map_data[0]))]
    for _ in range(len(st.map_data))
]

nodes = set()           # 视线方向所有节点列表（像素坐标）

in_fov_nodes = {}       # 节点是否在视野范围内：{(x,y): True/False} （像素坐标）

valid_nodes = {}        # 视野范围节点是否有效（是否是可见墙体节点）：{(x,y): True/False} （像素坐标）

wall_line = set()      # 可以看见的墙体线段 [((),()),(()()),(()())]

visible_line = set()

visible_nodes = set()

is_ray_node = {}

test_nodes = []


sorted_nodes = []



