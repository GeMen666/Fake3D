import pygame
import sys
import time
from config import *

# 初始化与窗口设置
pygame.init()
screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
pygame.display.set_caption("test")

# 核心状态变量
paused = False       # 游戏暂停状态：False=未暂停，True=暂停
grabbed = False      # 鼠标抓取状态：False=未锁定，True=锁定在窗口内（无法移出）
visible = False      # 鼠标指针可见状态：False=隐藏，True=显示
clock = pygame.time.Clock()  # 创建时钟对象（用于控制游戏帧率）
last_time = time.time()      # 记录上一次鼠标移动的时间戳（用于计算速度）
mouse_speed = [0.0, 0.0]     # 鼠标移动速度：[x轴速度, y轴速度]，单位：像素/秒

# 初始隐藏鼠标
pygame.mouse.set_visible(visible)

# 主循环
running = True
while running:
    dt = clock.tick(60) / 1000.0
    
    # 鼠标抓取状态控制
    if pygame.mouse.get_focused():
        if not paused and not grabbed:
            grabbed = True
            visible = False
            pygame.event.set_grab(True)
            pygame.mouse.set_visible(False)
    else:
        if grabbed:
            grabbed = False
            visible = True
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)

    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # ESC暂停/恢复
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused = not paused
            if paused:
                grabbed, visible = False, True
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
                pygame.mouse.set_pos((WINDOW_HEIGHT//2, WINDOW_WIDTH//2))  # 指针居中
            else:
                grabbed, visible = True, False
                pygame.event.set_grab(True)
                pygame.mouse.set_visible(False)
        
        # 读取鼠标移动与速度
        if event.type == pygame.MOUSEMOTION and not paused:
            dx, dy = event.rel
            time_diff = time.time() - last_time
            if time_diff > 0:
                mouse_speed = [dx/time_diff, dy/time_diff]
            last_time = time.time()
            # 绝对位置兜底（限制在窗口内）
            x, y = pygame.mouse.get_pos()
            pygame.mouse.set_pos((max(0, min(x, WINDOW_HEIGHT)), max(0, min(y, WINDOW_WIDTH))))

    # 绘制暂停提示
    screen.fill((30, 30, 30))
    if paused:
        text = pygame.font.SysFont(None, 48).render("暂停 (ESC恢复)", True, (255,255,255))
        screen.blit(text, (WINDOW_HEIGHT//2 - text.get_width()//2, WINDOW_WIDTH//2 - text.get_height()//2))
    pygame.display.flip()

# 退出
pygame.event.set_grab(False)  # 退出前释放鼠标抓取（避免鼠标被永久锁定）
pygame.mouse.set_visible(True)  # 退出前显示鼠标指针（恢复系统默认状态）
pygame.quit()  # 退出pygame所有模块
sys.exit()     # 退出程序