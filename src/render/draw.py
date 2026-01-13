# render_draw.py 处理渲染逻辑
import pygame
import config as conf
from core import game_state as st
from .controller import nodes
import math


def draw_small_map(screen):


    # 绘制瓦片
    for row in range(len(st.map_data)):
        for col in range(len(st.map_data[0])):
            screen_x = col * conf.TILE_SIZE * conf.SCALE + conf.BASED_POS[0]
            screen_y = row * conf.TILE_SIZE * conf.SCALE + conf.BASED_POS[1]
            rect = pygame.Rect(int(screen_x), int(screen_y), int(conf.TILE_SIZE * conf.SCALE), int(conf.TILE_SIZE * conf.SCALE))
            
            # 根据地图数据绘制不同颜色的瓦片
            if st.map_data[row][col] == 1:  # 墙体
                # 绘制墙体填充
                pygame.draw.rect(screen, (100, 100, 100), rect)
                # 绘制墙体边界
                pygame.draw.rect(screen, (150, 150, 150), rect, 1)  # 1像素宽的边界
            else:  # 空地
                # 绘制空地填充
                pygame.draw.rect(screen, (50, 50, 50), rect)
                # 绘制空地边界
                pygame.draw.rect(screen, (70, 70, 70), rect, 1)  # 1像素宽的边界

    for i in range(conf.WINDOW_WIDTH):
        if i in nodes:
            x = conf.BASED_POS[0] + nodes[i][1] * conf.SCALE
            y = conf.BASED_POS[1] + nodes[i][2] * conf.SCALE
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 1)


    draw_fov_boundaries(screen, st.view_angle - conf.FOV / 2, 1000)
    draw_fov_boundaries(screen, st.view_angle + conf.FOV / 2, 1000)



def draw_fov_boundaries(screen, angle, dir_length):
    player_screen_x = conf.BASED_POS[0] + st.player_x * conf.SCALE
    player_screen_y = conf.BASED_POS[1] + st.player_y * conf.SCALE
    angle_rad = math.radians(angle)
    x = player_screen_x + math.cos(angle_rad) * dir_length * 2
    y = player_screen_y + math.sin(angle_rad) * dir_length * 2
    pygame.draw.line(screen, (255, 0, 0), (player_screen_x, player_screen_y), (x, y), 1)