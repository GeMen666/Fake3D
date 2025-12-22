import pygame
import math
import status as st
import config as conf
from render_calculate import nodes, valid_nodes, processing_grid

SCALE = 1

def draw_fov_boundaries(screen, player_screen_x, player_screen_y, angle, dir_length):
    """绘制视野边界线（角度转弧度计算）"""
    angle_rad = math.radians(angle)
    x = player_screen_x + math.cos(angle_rad) * dir_length * 2
    y = player_screen_y + math.sin(angle_rad) * dir_length * 2
    pygame.draw.line(screen, (255, 0, 0), (player_screen_x, player_screen_y), (x, y), 1)

def draw_map(screen):
    """绘制地图、玩家、视野、节点"""
    # 绘制瓦片
    for row in range(len(st.map_data)):
        for col in range(len(st.map_data[0])):
            screen_x = col * st.TILE_SIZE * SCALE
            screen_y = row * st.TILE_SIZE * SCALE
            rect = pygame.Rect(screen_x, screen_y, st.TILE_SIZE * SCALE, st.TILE_SIZE * SCALE)
            
            # 瓦片颜色逻辑
            if st.map_data[row][col] == 1:  # 墙体
                color = (255, 255, 100) if processing_grid[row][col] else (200, 200, 200)
            else:  # 空地
                color = (255, 255, 100) if processing_grid[row][col] else (0, 0, 0)
            pygame.draw.rect(screen, color, rect)

    # 绘制玩家
    player_screen_x = st.player_x * SCALE
    player_screen_y = st.player_y * SCALE
    pygame.draw.circle(screen, (255, 255, 255), (player_screen_x, player_screen_y), 3)

    # 绘制玩家朝向
    dir_length = 100 * SCALE
    view_angle_rad = math.radians(st.view_angle)
    end_x = player_screen_x + math.cos(view_angle_rad) * dir_length
    end_y = player_screen_y + math.sin(view_angle_rad) * dir_length
    pygame.draw.line(screen, (0, 255, 0), (player_screen_x, player_screen_y), (end_x, end_y), 2)

    # 绘制视野边界
    fov = conf.FOV
    left_angle = st.view_angle - fov / 2
    right_angle = st.view_angle + fov / 2
    draw_fov_boundaries(screen, player_screen_x, player_screen_y, left_angle, dir_length)
    draw_fov_boundaries(screen, player_screen_x, player_screen_y, right_angle, dir_length)

    # 绘制节点（修复：加KeyError防护，按布尔值判断颜色）
    for node in nodes:
        if node in valid_nodes:
            color = (0, 255, 0) if valid_nodes[node] else (255, 0, 0)
            pygame.draw.circle(screen, color, (node[0] * SCALE, node[1] * SCALE), 2)