# main 实现窗口和主循环

import pygame
import time
import config
import ctypes
from engine import *
from input_event import *
from game_state import *
from render_draw import draw_small_map
from render_3D import draw_3D
from render_controller import all_calculate


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

    screen.fill((0, 0, 0))
    
    all_calculate()

    draw_small_map(screen)
    draw_3D(screen)
    pygame.display.flip()

pygame.quit()

