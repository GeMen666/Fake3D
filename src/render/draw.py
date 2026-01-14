# render_draw.py 渲染绘制
# src\render\draw.py

import pygame
import config as conf
from core import game_state as st
from .controller import nodes
import math


def all_draw(screen):
    draw_background(screen)
    draw_3D(screen)
    draw_small_map(screen)
    draw_fov_boundaries(screen)
    draw_player(screen)


def draw_background(screen):
    # 计算地图的实际尺寸
    map_width = len(st.map_data[0]) * conf.TILE_SIZE
    map_height = len(st.map_data) * conf.TILE_SIZE
    
    # 绘制上半部分（天蓝色）- 天空
    upper_rect = pygame.Rect(0, 0, conf.WINDOW_WIDTH, conf.HORIZON + st.jump_height)
    pygame.draw.rect(screen, (135, 206, 235), upper_rect)  # 天蓝色
    
    # 绘制下半部分（浅绿色）- 地面
    lower_rect = pygame.Rect(0, conf.HORIZON + st.jump_height, conf.WINDOW_WIDTH, conf.WINDOW_HEIGHT - conf.HORIZON - st.jump_height)
    pygame.draw.rect(screen, (107, 142, 35), lower_rect) 


def draw_3D(screen):
    # 绘制射线交点和3D墙
    for i in range(conf.WINDOW_WIDTH):
        if i in nodes:
            # 绘制3D墙（在主视图上）
            y1 = (conf.HORIZON - nodes[i][2]) / 2 + conf.BASED_HEIGHT + st.jump_height
            y2 = y1 + nodes[i][2] + conf.BASED_HEIGHT
            
            # 根据距离计算墙的颜色（距离越远颜色越深）
            distance = nodes[i][3]
            color_factor = min(1.0, distance / 1000)  # 0-1之间的因子
            
            # 线性插值计算颜色 - 改为柔和的灰白色系
            # 近处：柔和的米白色 (220, 220, 210)
            # 远处：深灰色 (100, 100, 95)
            r = int(220 * (1 - color_factor) + 100 * color_factor)
            g = int(220 * (1 - color_factor) + 100 * color_factor)
            b = int(210 * (1 - color_factor) + 95 * color_factor)
            
            # 绘制3D墙切片
            pygame.draw.line(screen, (r, g, b), (i, int(y1)), (i, int(y2)), 1)

def draw_small_map(screen):
    # 绘制瓦片
    for row in range(len(st.map_data)):
        for col in range(len(st.map_data[0])):
            screen_x = col * conf.TILE_SIZE * conf.SCALE + conf.BASED_POS[0]
            screen_y = row * conf.TILE_SIZE * conf.SCALE + conf.BASED_POS[1]
            rect = pygame.Rect(int(screen_x), int(screen_y), int(conf.TILE_SIZE * conf.SCALE) + 1, int(conf.TILE_SIZE * conf.SCALE) + 1)
            
            # 根据地图数据绘制不同颜色的瓦片
            if st.map_data[row][col] == 1:  # 墙体
                # 绘制墙体填充
                pygame.draw.rect(screen, (100, 100, 100), rect)
            else:  # 空地
                # 绘制空地填充
                pygame.draw.rect(screen, (50, 50, 50), rect)

    for i in range(conf.WINDOW_WIDTH):
        if i in nodes:
            # 绘制射线交点（在小地图上）
            x = conf.BASED_POS[0] + nodes[i][0] * conf.SCALE
            y = conf.BASED_POS[1] + nodes[i][1] * conf.SCALE
            pygame.draw.circle(screen, (180, 180, 150), (int(x), int(y)), 1)  # 柔和的米黄色交点




def draw_fov_boundaries(screen):
    def darw(screen, angle, dir_length):
        player_screen_x = conf.BASED_POS[0] + st.player_x * conf.SCALE
        player_screen_y = conf.BASED_POS[1] + st.player_y * conf.SCALE
        angle_rad = math.radians(angle)
        x = player_screen_x + math.cos(angle_rad) * dir_length * 2
        y = player_screen_y + math.sin(angle_rad) * dir_length * 2
        pygame.draw.line(screen, (255, 0, 0), (player_screen_x, player_screen_y), (x, y), 1)

    darw(screen, st.view_angle - conf.FOV / 2, 5)
    darw(screen, st.view_angle + conf.FOV / 2, 5)


def draw_player(screen):
    player_screen_x = conf.BASED_POS[0] + st.player_x * conf.SCALE
    player_screen_y = conf.BASED_POS[1] + st.player_y * conf.SCALE
    pygame.draw.circle(screen, (255, 0, 0), (int(player_screen_x), int(player_screen_y)), 1)