#
#           YOU'RE UNDER CONTROL
#   tixlegeek 2024 - tixlegeek@cyberpunk.company
#
import sys
import numpy as np
import pygame
from croix_pharmacie.pharmacontroller import PharmaScreen

def main():
    size = 48
    t=0
    pygame.init()
    screen = PharmaScreen()
    matrix = np.zeros((size, size), dtype=int)
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
                if ((np.sin( np.hypot(i-(size/2),j-(size/2))-np.atan2(i-(size/2),j-(size/2))-((i+j+t)/10)))) > 0:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = 0
        screen.set_image(matrix.tolist())

if __name__ == "__main__":
    main()