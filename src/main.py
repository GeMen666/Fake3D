# main 实现游戏窗口和主循环

import pygame
import time
from config import *
from input_event import *
from status import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("test")
clock = pygame.time.Clock()
last_time = time.time() 
pygame.mouse.set_visible(mouse_visible)
pygame.event.set_grab(mouse_grabbed)

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        event_manage(event)

    screen.fill((0, 0, 0))

    pygame.display.flip()

pygame.quit()

