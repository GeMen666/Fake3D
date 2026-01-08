import pygame
import math
import game_state as st
import config as conf
from render_controller import visible_line, visible_nodes


def draw_3D(screen):
    
    for x1, y1, x2, y2 in visible_line:
        pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 1)
    
    for x, y in visible_nodes:
        pygame.draw.circle(screen, (0, 255, 0), (x, y), 1)
