# input_event.py - 输入事件处理
# src\core\input_event.py


import pygame
import config as conf
import core.game_state as st


# 暂停控制
def paused_control():
    st.paused = not st.paused
    if st.paused:
        st.mouse_visible = True
        st.mouse_grabbed = False
        pygame.mouse.set_pos(conf.WINDOW_WIDTH // 2,  conf.WINDOW_HEIGHT // 2)
    else:
        st.mouse_visible = False
        st.mouse_grabbed = True
    pygame.mouse.set_visible(st.mouse_visible)
    pygame.event.set_grab(st.mouse_grabbed)

# 鼠标移动事件处理
def mouse_move(event):
    # 获取鼠标的相对移动量
    st.rel_x,st.rel_y = event.rel
    st.view_angle = (st.view_angle + conf.MOUSE_SENSITIVITY * st.rel_x) % conf.YAW_RANGE
    st.vertical_view -= st.rel_y 


# 键盘按下事件处理
def keyboard_pressed(event):
    if event.key == pygame.K_w:
        print('forward')
        st.key_states['forward'] = True
    elif event.key == pygame.K_a:
        print('left')
        st.key_states['left'] = True
    elif event.key == pygame.K_s:
        print('backward')
        st.key_states['backward'] = True
    elif event.key == pygame.K_d:
        print('right')
        st.key_states['right'] = True
    elif event.key == pygame.K_SPACE:
        print('jump')
        if not st.jumping:
            st.jumping = True
            st.jump_time = 0
            st.jump_height = 0


# 键盘松开事件处理
def keyboard_released(event):
    if event.key == pygame.K_w:
        st.key_states['forward'] = False
    elif event.key == pygame.K_a:
        st.key_states['left'] = False
    elif event.key == pygame.K_s:
        st.key_states['backward'] = False
    elif event.key == pygame.K_d:
        st.key_states['right'] = False



def event_manage(event):
    # 键盘按下事件
    if event.type == pygame.KEYDOWN:
        # 处理ESC键, 切换暂停
        if event.key == pygame.K_ESCAPE:
            paused_control()
        # 处理其他按键
        elif not st.paused:
            keyboard_pressed(event)
    # 键盘松开事件
    elif event.type == pygame.KEYUP:
        # 处理其他按键
        if not st.paused:
            keyboard_released(event)
    # 鼠标移动事件
    elif event.type == pygame.MOUSEMOTION and not st.paused:
        mouse_move(event)

