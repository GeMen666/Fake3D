# render_draw.py

import pygame
import math
import status as st
import config as conf
from render_calculate import processing_grid, visible_nodes, in_fov_nodes

def draw_fov_boundaries(screen, player_screen_x, player_screen_y, angle, dir_length):
    angle_rad = math.radians(angle)
    x = player_screen_x + math.cos(angle_rad) * dir_length * 2
    y = player_screen_y + math.sin(angle_rad) * dir_length * 2
    pygame.draw.line(screen, (255, 0, 0), (player_screen_x, player_screen_y), (x, y), 1)

def draw_map(screen):


    # 绘制瓦片
    for row in range(len(st.map_data)):
        for col in range(len(st.map_data[0])):
            screen_x = col * st.TILE_SIZE * conf.SCALE + conf.BASED_POS[0]
            screen_y = row * st.TILE_SIZE * conf.SCALE + conf.BASED_POS[1]
            rect = pygame.Rect(int(screen_x), int(screen_y), int(st.TILE_SIZE * conf.SCALE) + 1, int(st.TILE_SIZE * conf.SCALE) + 1)
            
            # 瓦片颜色逻辑
            if st.map_data[row][col] == 1:  # 墙体
                color = (220, 220, 220) if processing_grid[row][col] else (128, 128, 128)
            else:  # 空地
                color = (64, 64, 64) if processing_grid[row][col] else (15, 15, 15)
            pygame.draw.rect(screen, color, rect)

    # 绘制玩家
    player_screen_x = conf.BASED_POS[0] + st.player_x * conf.SCALE
    player_screen_y = conf.BASED_POS[1] + st.player_y * conf.SCALE
    pygame.draw.circle(screen, (255, 255, 255), (player_screen_x, player_screen_y), 3)

    # 绘制玩家视线
    dir_length = 700 * conf.SCALE
    view_angle_rad = math.radians(st.view_angle)
    end_x = player_screen_x + math.cos(view_angle_rad) * dir_length
    end_y = player_screen_y + math.sin(view_angle_rad) * dir_length
    pygame.draw.line(screen, (0, 255, 0), (player_screen_x, player_screen_y), (end_x, end_y), 2)

    # 绘制视野边界线
    fov = conf.FOV
    left_angle = st.view_angle - fov / 2
    right_angle = st.view_angle + fov / 2
    draw_fov_boundaries(screen, player_screen_x, player_screen_y, left_angle, dir_length)
    draw_fov_boundaries(screen, player_screen_x, player_screen_y, right_angle, dir_length)


    # 绘制节点
    for node in in_fov_nodes:
        if in_fov_nodes[node]:
            if node in visible_nodes and visible_nodes[node]:
                node_screen_x = conf.BASED_POS[0] + node[0] * conf.SCALE
                node_screen_y = conf.BASED_POS[1] + node[1] * conf.SCALE
                pygame.draw.line(screen, (0, 0, 255), (player_screen_x, player_screen_y), (node_screen_x, node_screen_y), 1)    # 蓝色连接线
                color = (0, 255, 0)     # 绿色可见节点
            else:
                color = (255, 255, 150)   # 浅黄色无效节点
        else:
            color = (255, 0, 0)         # 红色不可见节点
        
        node_screen_x = conf.BASED_POS[0] + node[0] * conf.SCALE
        node_screen_y = conf.BASED_POS[1] + node[1] * conf.SCALE
        pygame.draw.circle(screen, color, (node_screen_x, node_screen_y), 2)

    # for node in v_node:
    #     node_screen_x = conf.BASED_POS[0] + node[0] * conf.SCALE
    #     node_screen_y = conf.BASED_POS[1] + node[1] * conf.SCALE
    #     pygame.draw.circle(screen, (255, 0, 255), (node_screen_x, node_screen_y), 3)
    
