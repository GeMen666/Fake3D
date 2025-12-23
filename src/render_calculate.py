import queue
import math
import status as st
from utils import *
import config as conf


visited_grid = [
    [False for _ in range(len(st.map_data[0]))]
    for _ in range(len(st.map_data))
]

processing_grid = [
    [False for _ in range(len(st.map_data[0]))]
    for _ in range(len(st.map_data))
]

tile_q = queue.Queue()      # 待处理的格子队列（行，列）

nodes = []          # 视线方向所有节点列表（像素坐标）

in_fov_nodes = {}       # 节点是否在视野范围内：{(x,y): True/False} （像素坐标）

valid_nodes = {}        # 视野范围节点是否有效（是否是墙体节点）：{(x,y): True/False} （像素坐标）

visible_nodes = {}      # 节点是否在视野内可见：{(x,y): True/False} （像素坐标）

fov_ray_q = []      # 视野射线 [((),()),(()()),(()())]

wall_line = []      # 可以看见的墙体线段 [((),()),(()()),(()())]


def select_wall_line():
    global wall_line
    for row in range(len(processing_grid)):
        for col in range(len(processing_grid[0])):
            if processing_grid[row][col] and st.map_data[row][col] == 1:
                tile_nodes =  get_tile_nodes(row,col)   # 节点顺序：上左0、上右1、下右2、下左3
                tile_borders = get_tile_border(row,col)  # 边界顺序：上边界0、右边界1、下边界2、左边界3
                count = 0
                for node in tile_nodes:
                    if node in visible_nodes:
                        count += 1
                
            
 


def select_forward_tile():
    global tile_q
    player_pos = get_floor_position(st.player_x, st.player_y)  # (col, row)

    tile_q.put((player_pos[1],player_pos[0]))
    processing_grid[player_pos[1]][player_pos[0]] = True

    view_angle = st.view_angle
    col_max = len(st.map_data[0]) - 1
    row_max = len(st.map_data) - 1

    if 315 <= view_angle <= 360 or 0 <= view_angle < 45:  # 右（col+1）
        if player_pos[0] + 1 <= col_max:
            target_tile = (player_pos[1], player_pos[0]+1)
            tile_q.put(target_tile)
    elif 45 <= view_angle < 135:  # 下（row+1）
        if player_pos[1] + 1 <= row_max:
            target_tile = (player_pos[1]+1, player_pos[0])
            tile_q.put(target_tile)
    elif 135 <= view_angle < 225:  # 左（col-1）
        if player_pos[0] - 1 >= 0:
            target_tile = (player_pos[1], player_pos[0]-1)
            tile_q.put(target_tile)
    elif 225 <= view_angle < 315:  # 上（row-1）
        if player_pos[1] - 1 >= 0:
            target_tile = (player_pos[1]-1, player_pos[0])
            tile_q.put(target_tile)

def reset_grids():
    global visited_grid
    nodes.clear()
    in_fov_nodes.clear()
    for i in range(len(processing_grid)):
        for j in range(len(processing_grid[0])):
            processing_grid[i][j] = False
            visited_grid[i][j] = False

def bfs_select_tile():
    global tile_q, visited_grid
    while not tile_q.empty():
        cur_pos = tile_q.get()
        if (cur_pos[0] < 0 or cur_pos[0] >= len(st.map_data) or
            cur_pos[1] < 0 or cur_pos[1] >= len(st.map_data[0])):
            continue
        if visited_grid[cur_pos[0]][cur_pos[1]]:
            continue
        
        is_in_fov = check_current_tile(cur_pos)
        visited_grid[cur_pos[0]][cur_pos[1]] = True
        
        if is_in_fov:
            processing_grid[cur_pos[0]][cur_pos[1]] = True
            if cur_pos[0]+1 < len(st.map_data) and not visited_grid[cur_pos[0]+1][cur_pos[1]]:
                tile_q.put((cur_pos[0]+1, cur_pos[1]))
            if cur_pos[0]-1 >= 0 and not visited_grid[cur_pos[0]-1][cur_pos[1]]:
                tile_q.put((cur_pos[0]-1, cur_pos[1]))
            if cur_pos[1]+1 < len(st.map_data[0]) and not visited_grid[cur_pos[0]][cur_pos[1]+1]:
                tile_q.put((cur_pos[0], cur_pos[1]+1))
            if cur_pos[1]-1 >= 0 and not visited_grid[cur_pos[0]][cur_pos[1]-1]:
                tile_q.put((cur_pos[0], cur_pos[1]-1))

def check_current_tile(tile_pos):
    global nodes, in_fov_nodes, valid_nodes
    row, col = tile_pos
    half_fov = math.radians(conf.FOV / 2)

    if (row < 0 or row >= len(st.map_data) or col < 0 or col >= len(st.map_data[0])):
        return False

    tile_nodes = get_tile_nodes(col, row)
    has_valid_node = False
    for node_x, node_y in tile_nodes:

        if (node_x, node_y) not in nodes:
            nodes.append((node_x, node_y))

        # 检查节点是否在视野范围内
        if check_node_in_fov(node_x, node_y, half_fov):
            has_valid_node = True
            in_fov_nodes[(node_x, node_y)] = True
        else:
            in_fov_nodes[(node_x, node_y)] = False
        
        # 检查节点是否有效
        if check_node_valid(node_x, node_y):
            valid_nodes[(node_x, node_y)] = True
        else:
            valid_nodes[(node_x, node_y)] = False
        

    if has_valid_node:
        processing_grid[row][col] = True

        
    return has_valid_node

def check_node_in_fov(node_x, node_y, half_fov):

    if (node_x, node_y) in in_fov_nodes:
        return in_fov_nodes[(node_x, node_y)]

    delta_x = node_x - st.player_x
    delta_y = node_y - st.player_y
    
    # 计算节点相对于玩家的角度（基于屏幕坐标系）0°向右，90°向下，180°向左，270°向上
    node_angle = math.atan2(delta_y, delta_x)    # 使用atan2计算，返回-pi到pi的范围
    view_angle_rad = math.radians(st.view_angle)
    angle_diff = node_angle - view_angle_rad
    
    # 将角度差标准化到-pi到pi范围内
    if angle_diff > math.pi:
        angle_diff -= 2 * math.pi
    elif angle_diff < -math.pi:
        angle_diff += 2 * math.pi
    
    angle_diff = abs(angle_diff)
    
    # 判断是否在视野内
    in_fov = angle_diff <= half_fov

    return in_fov

def check_nodes_is_visible():
    global visible_nodes, valid_nodes

    # 判断玩家方向是否是墙，如果是则说明该节点在墙的背面，是不可见的
    # 判断玩家相对节点的方向
    # 1：左上 2：右上 3：右下 4：左下
    for node_x, node_y in valid_nodes:
        if not valid_nodes[(node_x, node_y)]:
            continue
        tile = -1
        if st.player_x > node_x and st.player_y < node_y:       # 右上
            tile = get_direction_tile(node_x, node_y, 2)
        elif st.player_x > node_x and st.player_y > node_y:     # 右下
            tile = get_direction_tile(node_x, node_y, 3)
        elif st.player_x < node_x and st.player_y > node_y:     # 左下
            tile = get_direction_tile(node_x, node_y, 4)
        elif st.player_x < node_x and st.player_y < node_y:     # 左上
            tile = get_direction_tile(node_x, node_y, 1)
        if tile == -1:
            continue
        if st.map_data[tile[1]][tile[0]] == 1:
            visible_nodes[(node_x, node_y)] = False
        else:
            visible_nodes[(node_x, node_y)] = True


def check_node_valid(node_x, node_y):
    if (node_x, node_y) in valid_nodes:
        return valid_nodes[(node_x, node_y)]


    # 我也不知道是节点哪个方向tile的索引了，不管了，能用就行
    index_x = int(node_x / st.TILE_SIZE) - 1
    index_y = int(node_y / st.TILE_SIZE) - 1

    # 添加边界检查
    map_height = len(st.map_data)
    map_width = len(st.map_data[0]) if map_height > 0 else 0
    
    # 检查所有可能访问的索引是否在有效范围内
    is_valid = False
    count = 0
    corners = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for dx, dy in corners:
        x = index_x + dx
        y = index_y + dy
        if 0 <= x < map_width and 0 <= y < map_height:
            if st.map_data[y][x] == 1:
                is_valid = True
                count += 1
        else:
            return False

    if count == 2 and index_x + 1 < map_width and index_y + 1 < map_height:
        if st.map_data[index_y][index_x] != st.map_data[index_y+1][index_x+1]:
            is_valid = False
    if count == 3:
        is_valid = True
    elif count == 4:
        is_valid = False


    return is_valid



def all_calculate():
    reset_grids()
    select_forward_tile()
    bfs_select_tile()
    check_nodes_is_visible()