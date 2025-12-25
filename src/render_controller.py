import queue
import math
import status as st
from utils import *
import config as conf
from render_calculate import *

# 可见的格子队列
visible_grid = [
    [False for _ in range(len(st.map_data[0]))]
    for _ in range(len(st.map_data))
]

nodes = set()           # 视线方向所有节点列表（像素坐标）

in_fov_nodes = {}       # 节点是否在视野范围内：{(x,y): True/False} （像素坐标）

valid_nodes = {}        # 视野范围节点是否有效（是否是墙体节点）：{(x,y): True/False} （像素坐标）

visible_nodes = {}      # 节点是否在视野内可见：{(x,y): True/False} （像素坐标）

wall_line = []      # 可以看见的墙体线段 [((),()),(()()),(()())]




def reset_grids():
    nodes.clear()
    in_fov_nodes.clear()
    visible_nodes.clear()
    valid_nodes.clear()
    for i in range(len(visible_grid)):
        for j in range(len(visible_grid[0])):
            visible_grid[i][j] = False



def bfs_init():
    global visible_grid
    tile_q = queue.Queue()
    player_pos = get_floor_position(st.player_x, st.player_y)  # (col, row)
    tile_q.put((player_pos[1],player_pos[0]))
    visible_grid[player_pos[1]][player_pos[0]] = True
    max_distance = math.sqrt(len(st.map_data) ** 2 + len(st.map_data[0]) ** 2) * st.TILE_SIZE
    tlies = get_tiles_along_ray(st.player_x, st.player_y, st.view_angle, max_distance)
    for tile_x, tile_y in tlies:
        tile_q.put((tile_y, tile_x))
    return tile_q


def bfs_select_tile():
    
    tile_q = bfs_init()
    visited_grid = [
        [False for _ in range(len(st.map_data[0]))]
        for _ in range(len(st.map_data))
    ]

    while not tile_q.empty():
        cur_pos = tile_q.get()
        if (cur_pos[0] < 0 or cur_pos[0] >= len(st.map_data) or cur_pos[1] < 0 or cur_pos[1] >= len(st.map_data[0])):
            continue
        if visited_grid[cur_pos[0]][cur_pos[1]]:
            continue
        visited_grid[cur_pos[0]][cur_pos[1]] = True
        is_in_fov = check_current_tile(cur_pos)
        if is_in_fov:
            visible_grid[cur_pos[0]][cur_pos[1]] = True
            tile_q.put((cur_pos[0]+1, cur_pos[1]))
            tile_q.put((cur_pos[0]-1, cur_pos[1]))
            tile_q.put((cur_pos[0], cur_pos[1]+1))
            tile_q.put((cur_pos[0], cur_pos[1]-1))


def check_current_tile(tile_pos):
    global nodes, in_fov_nodes, valid_nodes
    row, col = tile_pos
    half_fov = math.radians(conf.FOV / 2)

    if row < 0 or row >= len(st.map_data) or col < 0 or col >= len(st.map_data[0]):
        return False

    tile_nodes = get_tile_nodes(col, row)
    tile_in_fov = False
    for node_x, node_y in tile_nodes:

        if (node_x, node_y) not in nodes:
            nodes.add((node_x, node_y))

        # 检查节点是否在视野范围内
        if check_node_in_fov(node_x, node_y, half_fov):
            tile_in_fov = True
            in_fov_nodes[(node_x, node_y)] = True
        else:
            in_fov_nodes[(node_x, node_y)] = False
        
        # 检查节点是否有效
        if check_node_valid(node_x, node_y):
            valid_nodes[(node_x, node_y)] = True
        else:
            valid_nodes[(node_x, node_y)] = False
        
    if tile_in_fov:
        visible_grid[row][col] = True

    return tile_in_fov


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


def check_nodes_is_visible():
    global visible_nodes, valid_nodes

    for node_x, node_y in valid_nodes:
        if not valid_nodes[(node_x, node_y)]:
            continue
        
        visible_nodes[(node_x, node_y)] = True

        tiles = get_tiles_along_line(node_x, node_y, st.player_x, st.player_y)
        
        for tile_x, tile_y in tiles:
            if tile_x < 0 or tile_x >= len(st.map_data[0]) or tile_y < 0 or tile_y >= len(st.map_data):
                continue
            if st.map_data[tile_y][tile_x] == 1:
                visible_nodes[(node_x, node_y)] = False
                break


def get_intersections_along_all_ray():
    global nodes, in_fov_nodes, visible_nodes
    
    fov_ray = set()
    fov_ray.add((st.view_angle - conf.FOV / 2) % 360)
    fov_ray.add((st.view_angle + conf.FOV / 2) % 360)

    for range in fov_ray:
        target_node = get_single_ray_intersections(range)
        nodes.update(target_node)
        in_fov_nodes[target_node] = True
        visible_nodes[target_node] = True

def all_calculate():
    reset_grids()
    bfs_select_tile()
    check_nodes_is_visible()
    get_intersections_along_all_ray()
