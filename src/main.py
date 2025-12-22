# main 实现游戏窗口和主循环

import pygame
import time
from engine import *
from input_event import *
from status import *

pygame.init()
screen = pygame.display.set_mode((config.WINDOW_WIDTH,config.WINDOW_HEIGHT))
pygame.display.set_caption("test")
clock = pygame.time.Clock()
last_time = time.time() 
pygame.mouse.set_visible(mouse_visible)
pygame.event.set_grab(mouse_grabbed)

running = True
while running:
    clock.tick(config.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        event_manage(event)

    if not st.paused:
        if st.key_states['up']:
            player_move('w')
        if st.key_states['left']:
            player_move('a')
        if st.key_states['down']:
            player_move('s')
        if st.key_states['right']:
            player_move('d')

    print(f"({st.paused},{st.mouse_grabbed},{st.mouse_visible},{st.rel_x},{st.view_angle},{st.player_x},{st.player_y})")

    screen.fill((0, 0, 0))

    pygame.display.flip()

pygame.quit()

