# engine 游戏计算
import math
import status as st  # 使用别名 st


def player_move(direction):
    angle = 0
    if direction == 'w':
        angle = math.radians(st.view_angle)
    elif direction == 's':
        angle = math.radians(st.view_angle + 180)
    elif direction == 'a':
        angle = math.radians(st.view_angle - 90)
    elif direction == 'd':
        angle = math.radians(st.view_angle + 90)

    st.player_x = st.player_x + math.cos(angle) * st.player_speed
    st.player_y = st.player_y + math.sin(angle) * st.player_speed

