# 在 renderer_draw.py 文件中添加以下代码
import pygame
import math
import status as st
from render_calculate import visited_grid


def draw_map_debug(screen, camera_x, camera_y):
    """
    绘制调试用的地图视图，包括地图、玩家位置和视野范围

    Args:
        screen: pygame surface 对象
        camera_x: 摄像机 x 坐标
        camera_y: 摄像机 y 坐标
    """
    # 绘制地图网格
    for row in range(len(st.map_data)):
        for col in range(len(st.map_data[0])):
            # 计算屏幕坐标
            screen_x = col * st.TILE_SIZE - camera_x
            screen_y = row * st.TILE_SIZE - camera_y

            # 创建矩形区域
            rect = pygame.Rect(screen_x, screen_y, st.TILE_SIZE, st.TILE_SIZE)

            # 根据地图数据绘制不同颜色
            if st.map_data[row][col] == 1:  # 墙壁
                color = (100, 100, 100)  # 灰色
            else:  # 空地
                # 检查是否在视野范围内
                if row < len(visited_grid) and col < len(visited_grid[0]) and visited_grid[row][col]:
                    color = (50, 50, 150)  # 蓝色表示可见区域
                else:
                    color = (30, 30, 30)  # 深灰色表示未探索区域

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (80, 80, 80), rect, 1)  # 边框

    # 绘制玩家位置
    player_screen_x = st.player_x - camera_x
    player_screen_y = st.player_y - camera_y
    pygame.draw.circle(screen, (0, 255, 0), (int(player_screen_x), int(player_screen_y)), 8)

    # 绘制朝向指示器
    dir_length = 30
    end_x = st.player_x + math.cos(math.radians(st.view_angle)) * dir_length
    end_y = st.player_y + math.sin(math.radians(st.view_angle)) * dir_length
    pygame.draw.line(
        screen,
        (255, 255, 0),
        (player_screen_x, player_screen_y),
        (end_x - camera_x, end_y - camera_y),
        3
    )

    # 绘制视野范围线
    fov = 60  # 视野角度
    left_angle = st.view_angle - fov / 2
    right_angle = st.view_angle + fov / 2

    # 左视野边界线
    left_end_x = st.player_x + math.cos(math.radians(left_angle)) * dir_length
    left_end_y = st.player_y + math.sin(math.radians(left_angle)) * dir_length
    pygame.draw.line(
        screen,
        (100, 200, 100),
        (player_screen_x, player_screen_y),
        (left_end_x - camera_x, left_end_y - camera_y),
        1
    )

    # 右视野边界线
    right_end_x = st.player_x + math.cos(math.radians(right_angle)) * dir_length
    right_end_y = st.player_y + math.sin(math.radians(right_angle)) * dir_length
    pygame.draw.line(
        screen,
        (100, 200, 100),
        (player_screen_x, player_screen_y),
        (right_end_x - camera_x, right_end_y - camera_y),
        1
    )
