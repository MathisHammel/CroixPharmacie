#
#               HZV ROTOZOOM
#   tixlegeek 2024 - tixlegeek@cyberpunk.company
#
import random
import sys
import numpy as np
import pygame
from pharmacontroller import SCREEN_SIZE, PharmaScreen
size = 48
t=0

hzv = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,0,0],
    [0,1,0,0,1,1,1,1,0],
    [0,1,0,0,1,0,0,1,0],
    [0,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,1,0,0],
    [0,0,1,0,1,0,1,0,0],
    [0,0,0,0,0,0,0,0,0],
]

if __name__ == "__main__":
    pygame.init()
    screen = PharmaScreen()
    matrix = np.zeros((size, size), dtype=float)
    screen.set_image(matrix.tolist())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Randomize the values of 10 pixels
        t=t+1
        for i in range(size):
            for j in range(size):
                x= ( i * np.cos(t/10) - j * np.sin(t/10)) / ((np.sin(t/20)*3)+4)
                y= ( j * np.cos(t/10) + i * np.sin(t/10)) / ((np.sin(t/20)*3)+4)
                matrix[i][j] = hzv[int(x)%8][int(y)%9]

        screen.set_image(matrix.tolist())
