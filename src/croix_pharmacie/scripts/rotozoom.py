#
#               HZV ROTOZOOM
#   tixlegeek 2024 - tixlegeek@cyberpunk.company
#
import random
import sys
import numpy as np
import pygame
from croix_pharmacie.pharmacontroller import SCREEN_SIZE, PharmaScreen

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

def main():
    size = 48
    t=0
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
                x = ( (i-24) * np.cos(t/10) - (j-24) * np.sin(t/10)) / ((np.sin(t/20)*3)+4)+4
                y = ( (j-24) * np.cos(t/10) + (i-24) * np.sin(t/10)) / ((np.sin(t/20)*3)+4)+4
                matrix[i][j] = hzv[int(x)%8][int(y)%9]

        screen.set_image(matrix.tolist())

if __name__ == "__main__":
    main()