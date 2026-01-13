import pygame
import math
import sys

# 初始化Pygame
pygame.init()

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raycasting Demo - Wolfenstein 3D Style")

# 地图设置（0=空地, 1=墙体）
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

# 地图参数
TILE_SIZE = 64
MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)

# 玩家设置
player_x = 3.5 * TILE_SIZE  # 玩家起始位置（X坐标）
player_y = 3.5 * TILE_SIZE  # 玩家起始位置（Y坐标）
player_angle = 0  # 玩家朝向（弧度，0=向右）
FOV = math.pi / 2  # 视野角度（90度）
WALL_SCALE = 100  # 墙体高度缩放系数
HORIZON = SCREEN_HEIGHT // 2  # 地平线位置

def cast_ray(x, y, angle):
    """DDA算法：计算射线与最近墙体的交点"""
    # 射线方向
    dx = math.cos(angle)
    dy = math.sin(angle)
    
    # 防止除零错误
    if abs(dx) < 1e-6:
        dx = 1e-6 if dx >= 0 else -1e-6
    if abs(dy) < 1e-6:
        dy = 1e-6 if dy >= 0 else -1e-6
    
    # 玩家所在网格
    gx = int(x // TILE_SIZE)
    gy = int(y // TILE_SIZE)
    
    # 到下一个垂直/水平网格线的距离
    if dx > 0:
        x_dist = (gx + 1) * TILE_SIZE - x
    else:
        x_dist = x - gx * TILE_SIZE
        
    if dy > 0:
        y_dist = (gy + 1) * TILE_SIZE - y
    else:
        y_dist = y - gy * TILE_SIZE
    
    # DDA步进
    while True:
        # 比较哪个方向更近
        if x_dist < y_dist:
            x_dist += TILE_SIZE / abs(dx)
            gx += 1 if dx > 0 else -1
        else:
            y_dist += TILE_SIZE / abs(dy)
            gy += 1 if dy > 0 else -1
        
        # 检查是否超出地图边界
        if gx < 0 or gx >= MAP_WIDTH or gy < 0 or gy >= MAP_HEIGHT:
            return None, None, None
        
        # 检查是否撞到墙体
        if MAP[gy][gx] == 1:
            # 计算交点坐标
            if dx > 0:
                hit_x = gx * TILE_SIZE
            else:
                hit_x = (gx + 1) * TILE_SIZE
                
            if dy > 0:
                hit_y = gy * TILE_SIZE
            else:
                hit_y = (gy + 1) * TILE_SIZE
                
            # 计算欧氏距离
            distance = math.sqrt((hit_x - x) ** 2 + (hit_y - y) ** 2)
            return distance, hit_x, hit_y
    
    return None, None, None

# 游戏主循环
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # 清屏
    screen.fill((0, 0, 0))  # 黑色背景
    
    # 绘制墙体（逐列光线投射）
    for screen_x in range(SCREEN_WIDTH):
        # 计算当前列的射线角度
        ray_angle = player_angle + (screen_x / SCREEN_WIDTH - 0.5) * FOV
        
        # 发射射线
        distance, hit_x, hit_y = cast_ray(player_x, player_y, ray_angle)
        
        if distance is not None:
            # 鱼眼校正
            angle_diff = ray_angle - player_angle
            corrected_distance = distance * math.cos(angle_diff)
            
            # 计算墙体高度（反比于距离）
            wall_height = min(WALL_SCALE / corrected_distance, SCREEN_HEIGHT)
            
            # 计算屏幕位置
            wall_top = HORIZON - wall_height // 2
            wall_bottom = HORIZON + wall_height // 2
            
            # 绘制墙体（垂直线）
            pygame.draw.line(screen, (100, 100, 200), (screen_x, wall_top), (screen_x, wall_bottom))
    
    # 绘制地面（简单填充）
    pygame.draw.rect(screen, (50, 50, 50), (0, HORIZON, SCREEN_WIDTH, SCREEN_HEIGHT - HORIZON))
    
    # 绘制天空（简单填充）
    pygame.draw.rect(screen, (100, 150, 255), (0, 0, SCREEN_WIDTH, HORIZON))
    
    # 更新屏幕
    pygame.display.flip()
    
    # 限制帧率
    clock.tick(60)

pygame.quit()
sys.exit()