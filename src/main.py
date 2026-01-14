# main.py - 主程序入口
# src\main.py

import pygame
import time
import config
from core.engine import *
from core.input_event import *
from core.game_state import *
from render.controller import all_calculate
from render.draw import all_draw
from core.engine import engine_controller


pygame.init()
screen = pygame.display.set_mode((config.WINDOW_WIDTH,config.WINDOW_HEIGHT))
pygame.display.set_caption("test")
clock = pygame.time.Clock()
last_time = time.time()
pygame.mouse.set_visible(mouse_visible)
pygame.event.set_grab(mouse_grabbed)
# 关键步骤：停止文本输入，锁定为英文输入模式
pygame.key.stop_text_input()

running = True
while running:
    clock.tick(config.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        event_manage(event)
    
    engine_controller()

    all_calculate()

    all_draw(screen)

    pygame.display.flip()

pygame.quit()