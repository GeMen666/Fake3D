import pygame
import config
import core.game_state as st


def paused_control():
    st.paused = not st.paused
    if st.paused:
        st.mouse_visible = True
        st.mouse_grabbed = False
        pygame.mouse.set_pos(config.WINDOW_WIDTH // 2,  config.WINDOW_HEIGHT // 2)
    else:
        st.mouse_visible = False
        st.mouse_grabbed = True
    pygame.mouse.set_visible(st.mouse_visible)
    pygame.event.set_grab(st.mouse_grabbed)

def mouse_move(event):
    st.rel_x,st.rel_y = event.rel
    st.view_angle = (st.view_angle + config.MOUSE_SENSITIVITY * st.rel_x) % config.YAW_RANGE


def keyboard_pressed(event):
    if event.key == pygame.K_UP:
        st.key_states['up'] = True
    elif event.key == pygame.K_LEFT:
        st.key_states['left'] = True
    elif event.key == pygame.K_DOWN:
        st.key_states['down'] = True
    elif event.key == pygame.K_RIGHT:
        st.key_states['right'] = True

def keyboard_released(event):
    if event.key == pygame.K_UP:
        st.key_states['up'] = False
    elif event.key == pygame.K_LEFT:
        st.key_states['left'] = False
    elif event.key == pygame.K_DOWN:
        st.key_states['down'] = False
    elif event.key == pygame.K_RIGHT:
        st.key_states['right'] = False


def event_manage(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            paused_control()
        elif not st.paused:
            keyboard_pressed(event)
    elif event.type == pygame.KEYUP:
        if not st.paused:
            keyboard_released(event)
    elif event.type == pygame.MOUSEMOTION and not st.paused:
        mouse_move(event)

