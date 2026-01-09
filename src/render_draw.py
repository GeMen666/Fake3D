# render_draw.py

import pygame
import math
import game_state as st
import config as conf
from render_globals import visible_grid, in_fov_nodes, valid_nodes, visible_line, visible_nodes, linked_nodes

def draw_fov_boundaries(screen, player_screen_x, player_screen_y, angle, dir_length):
    angle_rad = math.radians(angle)
    x = player_screen_x + math.cos(angle_rad) * dir_length * 2
    y = player_screen_y + math.sin(angle_rad) * dir_length * 2
    pygame.draw.line(screen, (255, 0, 0), (player_screen_x, player_screen_y), (x, y), 1)

def draw_small_map(screen):
    player_screen_x = conf.BASED_POS[0] + st.player_x * conf.SCALE
    player_screen_y = conf.BASED_POS[1] + st.player_y * conf.SCALE
    # 绘制瓦片
    for row in range(len(st.map_data)):
        for col in range(len(st.map_data[0])):
            screen_x = col * st.TILE_SIZE * conf.SCALE + conf.BASED_POS[0]
            screen_y = row * st.TILE_SIZE * conf.SCALE + conf.BASED_POS[1]
            rect = pygame.Rect(int(screen_x), int(screen_y), int(st.TILE_SIZE * conf.SCALE) + 1, int(st.TILE_SIZE * conf.SCALE) + 1)
            
            # 瓦片颜色逻辑
            if st.map_data[row][col] == 1:  # 墙体
                color = (220, 220, 220) if visible_grid[row][col] else (128, 128, 128)
            else:  # 空地
                color = (64, 64, 64) if visible_grid[row][col] else (15, 15, 15)
            pygame.draw.rect(screen, color, rect)

    # 绘制玩家
    pygame.draw.circle(screen, (255, 255, 255), (player_screen_x, player_screen_y), 3)


    # 绘制视野
    for i in range(len(linked_nodes)):
        if i == len(linked_nodes) - 1:
            break
        screen_x1, screen_y1 = conf.BASED_POS[0] + linked_nodes[i][0] * conf.SCALE, conf.BASED_POS[1] + linked_nodes[i][1] * conf.SCALE
        screen_x2, screen_y2 = conf.BASED_POS[0] + linked_nodes[i+1][0] * conf.SCALE, conf.BASED_POS[1] + linked_nodes[i+1][1] * conf.SCALE
        # pygame.draw.polygon(screen, (200, 200, 200), [(player_screen_x, player_screen_y), (screen_x1, screen_y1), (screen_x2, screen_y2)])
        pygame.draw.line(screen, (255, 0, 0), (screen_x1, screen_y1), (screen_x2, screen_y2), 2)




    # 绘制节点
    for node in in_fov_nodes:
        if in_fov_nodes[node]:
            if node in valid_nodes and valid_nodes[node]:
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





def draw_3D(screen):

    # #绘制视野边框
    # rect = pygame.Rect(conf.TEST_BASED[0], conf.TEST_BASED[1], conf.WINDOW_WIDTH * conf.TEST_SCALE, conf.WINDOW_HEIGHT * conf.TEST_SCALE)
    # pygame.draw.rect(screen, (255, 255, 255), rect, 3)
    
    for x1, y1, x2, y2 in visible_line:
        pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 1)
    
    for x, y in visible_nodes:
        pygame.draw.circle(screen, (0, 255, 0), (x, y), 1)


