# main.py - 主程序入口
import pygame
import time
import config
from core.engine import *
from core.input_event import *
from core.game_state import *
from render.controller import all_calculate
from render.draw import all_draw


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

    all_draw(screen)

    pygame.display.flip()

pygame.quit()