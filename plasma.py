#
#           YOU'RE UNDER CONTROL
#   tixlegeek 2024 - tixlegeek@cyberpunk.company
#
import random
import sys
import numpy as np
import pygame
from pharmacontroller import SCREEN_SIZE, PharmaScreen
size = 48
t=0
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
                pt = np.sin((t+i+j)/10)+np.cos((t+i+j)/10)
                p0 = np.sin(pt + j /3);
                p1 = np.cos(pt + i /3);
                matrix[i][j] = ((p0 + p1)+2)/4

        screen.set_image(matrix.tolist())
