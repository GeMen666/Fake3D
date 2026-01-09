import math
import game_state as st
from utils import *
import config as conf
from collections import deque, defaultdict
from render_globals import visible_grid,nodes, in_fov_nodes, valid_nodes


def get_tiles_along_line(x1, y1, x2, y2):
    tiles = set()
    rate = (y2 - y1) / (x2 - x1 + 0.01)
    correction = 1 if x1 < x2 else -1
    for cur_x in range(int(x1 / st.TILE_SIZE) * st.TILE_SIZE, int(x2), st.TILE_SIZE * correction):
        if not (min(x1, x2) < cur_x < max(x1, x2)): continue
        cur_y = (cur_x - x1) * rate + y1
        tiles.add((int(cur_x / st.TILE_SIZE), int(cur_y / st.TILE_SIZE)))
        tiles.add((int(cur_x / st.TILE_SIZE) - 1, int(cur_y / st.TILE_SIZE)))
    correction = 1 if y1 < y2 else -1
    for cur_y in range(int(y1 / st.TILE_SIZE) * st.TILE_SIZE, int(y2), st.TILE_SIZE * correction):
        if not (min(y1, y2) < cur_y < max(y1, y2)): continue
        cur_x = (cur_y - y1) / rate + x1
        tiles.add((int(cur_x / st.TILE_SIZE), int(cur_y / st.TILE_SIZE)))
        tiles.add((int(cur_x / st.TILE_SIZE), int(cur_y / st.TILE_SIZE) - 1))
    return tiles


def get_tiles_along_ray(start_x, start_y, angle, max_distance):
    angle_radians = math.radians(angle)
    end_x = start_x + math.cos(angle_radians) * max_distance
    end_y = start_y + math.sin(angle_radians) * max_distance
    return get_tiles_along_line(start_x, start_y, end_x, end_y)


def get_intersections_in_single_tile(start_x, start_y, tile_x, tile_y, angle):
    corss_nodes = set()
    top, right, botton, left = get_tile_border(tile_x, tile_y)
    angle_radians = math.radians(angle)
    tan = math.tan(angle_radians)
    def get_top_botton(target):
        dy = target - start_y
        if tan == 0: return
        dx = dy / tan
        if left < start_x + dx < right:
            corss_nodes.add((start_x + dx, start_y + dy))
    def get_left_right(target):
        dx = target - start_x
        dy = dx * tan
        if top < start_y + dy < botton:
            corss_nodes.add((start_x + dx, start_y + dy))

    get_top_botton(top)
    get_top_botton(botton)
    get_left_right(left)
    get_left_right(right)
    return corss_nodes


def get_all_intersections_along_ray(start_x, start_y, angle):
    pending_tiles = set()
    pending_nodes = set()
    max_distance = math.sqrt(len(st.map_data) ** 2 + len(st.map_data[0]) ** 2) * st.TILE_SIZE
    pending_tiles = get_tiles_along_ray(start_x, start_y, angle, max_distance)
    for tile_x, tile_y in pending_tiles:
        if check_index_valid(tile_x, tile_y) and st.map_data[tile_y][tile_x] == 1:
            pending_nodes.update(get_intersections_in_single_tile(start_x, start_y, tile_x, tile_y, angle))
    return pending_nodes


def get_target_intersections(x, y, angle):
    pending_nodes = get_all_intersections_along_ray(x, y, angle)
    if not pending_nodes:
        return ()
    if len(pending_nodes) == 1:
        return list(pending_nodes)[0]
    # 返回距离最小的交点
    min_distance = float('inf')
    min_node = None
    for node_x, node_y in pending_nodes:
        distance = math.sqrt((node_x - x) ** 2 + (node_y - y) ** 2)
        if distance < min_distance:
            min_distance = distance
            min_node = (node_x, node_y)
    return min_node
    
    

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
    if not in_fov_nodes[(node_x, node_y)]:
        return False
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





def node_connect():
    global nodes, valid_nodes

    nodes.clear()
    sorted_nodes = []
    for node_x, node_y in valid_nodes:
        if valid_nodes[(node_x, node_y)]:
            node_x, node_y = round(node_x, 2), round(node_y, 2)
            nodes.add((node_x, node_y))

    connect_node = {}

    left_fov_line = (st.view_angle - conf.FOV / 2) % 360
    
    angles = []
    for node_x, node_y in nodes:
        connect_node[(node_x, node_y)] = []
        dx, dy = node_x - st.player_x, node_y - st.player_y
        radian = math.atan2(dy, dx)
        angle = round(math.degrees(radian) - left_fov_line) % 360
        angles.append(angle)
        sorted_nodes.append((node_x, node_y, angle))
    sorted_nodes.sort(key=lambda x: x[2])
    angles.sort()
    angles = print(angles)

    for a, b, c in zip(sorted_nodes, sorted_nodes[1:], sorted_nodes[2:]):
        node_x1, node_y1, angle1 = a
        node_x2, node_y2, angle2 = b
        node_x3, node_y3, angle3 = c
        angle1, angle2, angle3 = round(angle1), round(angle2), round(angle3)
        if angle2 == angle3:
            if check_able_connect(node_x1, node_y1, node_x2, node_y2):
                connect_node[(node_x1, node_y1)].append((node_x2, node_y2))
                connect_node[(node_x2, node_y2)].append((node_x1, node_y1))
            elif check_able_connect(node_x1, node_y1, node_x3, node_y3):
                connect_node[(node_x1, node_y1)].append((node_x3, node_y3))
                connect_node[(node_x3, node_y3)].append((node_x1, node_y1))
        else:
            connect_node[(node_x1, node_y1)].append((node_x2, node_y2))
            connect_node[(node_x2, node_y2)].append((node_x1, node_y1))

    
        
    return connect_node

def check_able_connect(x1, y1, x2, y2):
    x1, y1 = round(x1), round(y1)
    x2, y2 = round(x2), round(y2)
    print((x1/64, x2/64), (y1/64, y2/64))
    if -5 <= x1 - x2 <= 5 or -5 <= y1 - y2 <= 5:
        print("True")
        return True
    else:
        print("False")
        return False
