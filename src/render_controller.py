import queue
import math
import game_state as st
from utils import *
import config as conf
from render_calculate import *
from render_globals import visible_grid, nodes, in_fov_nodes, valid_nodes


def reset_grids():
    global visible_grid, nodes, in_fov_nodes, valid_nodes
    nodes.clear()
    in_fov_nodes.clear()
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


def check_nodes_is_visible():
    global  valid_nodes

    for node_x, node_y in valid_nodes:
        if not valid_nodes[(node_x, node_y)]:
            continue

        tiles = get_tiles_along_line(node_x, node_y, st.player_x, st.player_y)
        
        for tile_x, tile_y in tiles:
            if tile_x < 0 or tile_x >= len(st.map_data[0]) or tile_y < 0 or tile_y >= len(st.map_data):
                continue
            if st.map_data[tile_y][tile_x] == 1:
                valid_nodes[(node_x, node_y)] = False
                break



def process_fov_ray_node():
    global nodes, in_fov_nodes, valid_nodes
    fov_ray = set()
    fov_ray.add((st.view_angle - conf.FOV / 2) % 360)
    fov_ray.add((st.view_angle + conf.FOV / 2) % 360)

    for node_x, node_y in valid_nodes:
        if not valid_nodes[(node_x, node_y)]:
            continue

        # 1：左上 2：右上 3：右下 4：左下
        if   node_x < st.player_x and node_y < st.player_y:
            direction = 1
        elif node_x > st.player_x and node_y < st.player_y:
            direction = 2
        elif node_x > st.player_x and node_y > st.player_y:
            direction = 3
        elif node_x < st.player_x and node_y > st.player_y:
            direction = 4
        else:
            continue

        index_x, index_y = get_direction_tile(node_x, node_y, direction)

        if check_index_valid(index_x, index_y) and st.map_data[index_y][index_x] == 0:
            dx, dy = node_x - st.player_x, node_y - st.player_y
            radian = math.atan2(dy, dx)
            fov_ray.add(math.degrees(radian))

    for range in fov_ray:
        node = get_single_ray_intersections(range)
        if not node:
            continue
        nodes.update(node)
        in_fov_nodes[node] = True
        valid_nodes[node] = True
        
def all_calculate():
    reset_grids()
    bfs_select_tile()
    check_nodes_is_visible()
    process_fov_ray_node()
