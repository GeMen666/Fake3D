import pygame
from config import *
from status import *


def Paused():
    global mouse_visible, mouse_grabbed, paused
    paused = not paused
    if paused:
        mouse_visible = True
        mouse_grabbed = False
        pygame.mouse.set_pos(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    else:
        mouse_visible = False
        mouse_grabbed = True
    pygame.mouse.set_visible(mouse_visible)
    pygame.event.set_grab(mouse_grabbed)

def get_mouse_rel_x(event):
    global rel_x, rel_y, view_angle
    rel_x,rel_y = event.rel
    view_angle = (view_angle + MOUSE_SENSITIVITY * rel_x) % YAW_RANGE


def event_manage(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        Paused()
    elif event.type == pygame.MOUSEMOTION and not paused:
        get_mouse_rel_x(event)

    print(f"({paused},{mouse_grabbed},{mouse_visible},{rel_x},{view_angle})")
