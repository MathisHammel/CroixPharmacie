import time
import random
from enum import Enum

import pygame

from pharmacontroller import SCREEN_SIZE, PharmaScreen
from writter import String

class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST  = 2
    WEST  = 3

class Snake:
    def __init__(self, speed, lenght, image):
        
        self.APPLE_BRIGHTNESS = 0.4
        self.SNAKE_BRIGHTNESS = 1.
        self.MAX_LENGHT = (16**2) * 5

        self.heading = Direction.SOUTH
        self.speed = speed
        assert 2 <= lenght <= 10, "start lenght must be between 2 and 10"
        self.lenght = lenght
        self.image = image

        self.time = time.time()

        self.starting_cell = (16, 0)
        self.tail = [None] * self.lenght
        for i in range(self.lenght):
            self.tail[i] = (16, self.lenght - 1 - i)

        self.apple = (23, 23)
        self.winned = False
        self.loosed = False

        # Avoid 2 inputs in the same frame
        self.heading_changed_in_frame = False

    def update(self, pressed_keys):
        self.handle_inputs(pressed_keys)

        if time.time() - self.time >= self.speed:
            if self.heading == Direction.NORTH:
                to_add = (0, -1)
            if self.heading == Direction.SOUTH:
                to_add = (0, 1)
            if self.heading == Direction.EAST:
                to_add = (1, 0)
            if self.heading == Direction.WEST:
                to_add = (-1, 0)
            new_head = (self.tail[0][0] + to_add[0], self.tail[0][1] + to_add[1])

            # Wall collision
            if not PharmaScreen.is_drawable(None, new_head[0], new_head[1]) or new_head in self.tail[1:]:
                self.loosed = True
                return False

            self.tail.insert(0, new_head)
            if len(self.tail) == self.MAX_LENGHT:
                self.winned = True
            apple_eaten = self.update_apple()
            if not apple_eaten:
                del self.tail[-1]

            self.heading_changed_in_frame = False
            self.time = time.time()

    def handle_inputs(self, pressed_keys):
        if self.heading_changed_in_frame: return

        if pressed_keys[pygame.K_UP]:
            if snake.heading != Direction.SOUTH:
                self.heading_changed_in_frame = True
                snake.heading = Direction.NORTH
        if pressed_keys[pygame.K_DOWN]:
            if snake.heading != Direction.NORTH:
                self.heading_changed_in_frame = True
                snake.heading = Direction.SOUTH
        if pressed_keys[pygame.K_LEFT]:
            if snake.heading != Direction.EAST:
                self.heading_changed_in_frame = True
                snake.heading = Direction.WEST
        if pressed_keys[pygame.K_RIGHT]:
            if snake.heading != Direction.WEST:
                self.heading_changed_in_frame = True
                snake.heading = Direction.EAST

    def update_apple(self):
        if self.tail[0] == self.apple:
            avaiable_cells = []
            for x in range(48):
                for y in range(48):
                    if PharmaScreen.is_drawable(None, x, y) and (x, y) not in self.tail : 
                        avaiable_cells.append((x, y))
            self.apple = random.choice(avaiable_cells)
            return True
        return False
    
    def draw(self):
        if self.loosed or self.winned: return
        for cell in self.tail:
            self.image[cell[1]][cell[0]] = self.SNAKE_BRIGHTNESS
        self.image[self.apple[1]][self.apple[0]] = self.APPLE_BRIGHTNESS

def clear(image):
    for line in image:
        for i in range(len(line)):
            line[i] = 0 

if __name__ == "__main__":
    pygame.init()
    screen = PharmaScreen()

    image = [[0.0 for c in range(SCREEN_SIZE)] for r in range(SCREEN_SIZE)]

    loosing_string = String(image, (1, 18), 45, "Perdu")
    winning_string = String(image, (1, 18), 45, "GG WP", cooldown=0.03, timeout=0)

    running = True
    snake = Snake(0.1, 10, image)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
        

        clear(image)
        if snake.loosed:
            loosing_string.scroll()
        elif snake.winned:
            # Color for the middle line of the cross 
            for line in image[16:32]:
                for i in range(len(line)):
                    line[i] = (1)
            winning_string.scroll(inverted=True)
        else:
            snake.update(pygame.key.get_pressed())
            snake.draw()

        screen.set_image(image)
