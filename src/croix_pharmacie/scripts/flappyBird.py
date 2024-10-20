# Chatgpt prompt: https://chatgpt.com/share/4b10b6ec-ed70-49e9-a69c-aa0db1167b1e

import sys
import pygame
import random

from croix_pharmacie.pharmacontroller import SCREEN_SIZE, PharmaScreen


######################################################################
#                                                                    #
#                                                                    #
#             ######                                                 #
#             #     # #    #   ##   #####  #    #   ##               #
#             #     # #    #  #  #  #    # ##  ##  #  #              #
#             ######  ###### #    # #    # # ## # #    #             #
#             #       #    # ###### #####  #    # ######             #
#             #       #    # #    # #   #  #    # #    #             #
#             #       #    # #    # #    # #    # #    #             #
#                                                                    #
#                      ######                                        #
#                      #     # # #####  #####                        #
#                      #     # # #    # #    #                       #
#                      ######  # #    # #    #                       #
#                      #     # # #####  #    #                       #
#                      #     # # #   #  #    #                       #
#                      ######  # #    # #####                        #
#                                                                    #
#                          PHARMA BIRD                               #
#                                                                    #
#                      ░░░░░░░░░░░░░░░░░░░░░░░                       #
#                      ░░░░░░░░░░░░░░░░░░░░░░░                       #
#                      ░░░░░░██░░░░░░░░░░██░░░                       #
#                      ░░░░░░░░██░░░░░░██░░░░░                       #
#                      ░░░░░░░░██████████░░░░░                       #
#                      ░░░░░░░░░░██████░░░░░░░                       #
#                      ░░░░░░░░░░██████░░░░░░░                       #
#                      ░░░░░░░░░░██████░░░░░░░                       #
#                      ░░░░░░░░░░░░░░░░░░░░░░░                       #
#                                                                    #
######################################################################

# Constants for the game
BIRD_SIZE = 2
GRAVITY = 0.5
FLAP_STRENGTH = -2.5
OBSTACLE_WIDTH = 3
GAP_HEIGHT = 16
OBSTACLE_SPEED = 1
FPS = 20
BIRD_X_OFFSET = 15  # Offset to center the bird on the left edge of the vertical cross

class Bird:
    def __init__(self):
        self.y = SCREEN_SIZE // 2
        self.x = BIRD_X_OFFSET  # Use the bird offset constant
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        # Prevent the bird from going out of bounds
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y >= SCREEN_SIZE - BIRD_SIZE:
            self.y = SCREEN_SIZE - BIRD_SIZE
            self.velocity = 0

class Obstacle:
    def __init__(self):
        self.x = SCREEN_SIZE
        self.gap_start = random.randint(1, SCREEN_SIZE - GAP_HEIGHT - 1)

    def update(self):
        self.x -= OBSTACLE_SPEED

    def is_off_screen(self):
        return self.x < -OBSTACLE_WIDTH

    def collides_with(self, bird):
        # Check if the bird is within the obstacle's vertical range and horizontal range
        if (self.x <= bird.x + BIRD_SIZE and self.x + OBSTACLE_WIDTH >= bird.x):
            if not (self.gap_start <= bird.y <= self.gap_start + GAP_HEIGHT - BIRD_SIZE):
                return True
        return False

def draw_bird(screen, bird):
    bird_y = int(bird.y)
    bird_x = bird.x
    for i in range(BIRD_SIZE):
        for j in range(BIRD_SIZE):
            if screen.is_drawable(bird_y + i, bird_x + j):
                screen.pixel_buffer[bird_y + i][bird_x + j] = 1.0

def draw_obstacles(screen, obstacles):
    for obstacle in obstacles:
        for y in range(SCREEN_SIZE):
            if y < obstacle.gap_start or y >= obstacle.gap_start + GAP_HEIGHT:
                for i in range(OBSTACLE_WIDTH):
                    if screen.is_drawable(y, obstacle.x + i):
                        screen.pixel_buffer[y][obstacle.x + i] = 1.0

def main():
    pygame.init()
    screen = PharmaScreen(True)
    clock = pygame.time.Clock()
    bird = Bird()
    obstacles = [Obstacle()]
    running = True

    while running:
        screen.pixel_buffer = [[0.0 for _ in range(SCREEN_SIZE)] for _ in range(SCREEN_SIZE)]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        if obstacles[-1].x < SCREEN_SIZE // 2:
            obstacles.append(Obstacle())

        for obstacle in obstacles:
            obstacle.update()
            if obstacle.collides_with(bird):
                print("Game Over")
                pygame.quit()
                sys.exit()

        obstacles = [obs for obs in obstacles if not obs.is_off_screen()]

        draw_bird(screen, bird)
        draw_obstacles(screen, obstacles)

        screen.set_image(screen.pixel_buffer)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
