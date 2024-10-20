import random
import sys

import pygame

from croix_pharmacie.pharmacontroller import SCREEN_SIZE, PharmaScreen

def main():
    pygame.init()
    screen = PharmaScreen()

    image = [[0.0 for c in range(SCREEN_SIZE)] for r in range(SCREEN_SIZE)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Randomize the values of 10 pixels
        for i in range(10):
            image[random.randrange(SCREEN_SIZE)][
                random.randrange(SCREEN_SIZE)
            ] = random.random()

        screen.set_image(image)

if __name__ == "__main__":
    main()