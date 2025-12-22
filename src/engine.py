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

    limit_player_position()


def limit_player_position():
    if st.player_x < 0:
        st.player_x = 0
    elif st.player_x >= len(st.map_data) * st.TILE_SIZE:
        st.player_x = len(st.map_data) * st.TILE_SIZE - 1

    if st.player_y < 0:
        st.player_y = 0
    elif st.player_y >= len(st.map_data[0]) * st.TILE_SIZE:
        st.player_y = len(st.map_data[0]) * st.TILE_SIZE - 1



