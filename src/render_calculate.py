import math
import status as st
from utils import *
import config as conf


def get_tiles_along_line(x1, y1, x2, y2):
    tiles = set()
    if x1 == x2 and y1 == y2: return tiles
    rate = (y2 - y1) / (x2 - x1)
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


def get_single_ray_intersections(angle):
    target_node = ()
    pending_nodes = get_all_intersections_along_ray(st.player_x, st.player_y, angle)
    min_distance = float('inf')
    for node_x, node_y in pending_nodes:
        distance = (node_x - st.player_x) ** 2 + (node_y - st.player_y) ** 2
        if distance < min_distance:
            target_node = (node_x, node_y)
            min_distance = distance
    return target_node


