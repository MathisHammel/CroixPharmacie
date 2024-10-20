import random
import sys
import pygame

from croix_pharmacie.pharmacontroller import SCREEN_SIZE, PharmaScreen

class Grid:
  def __init__ (self, width, height,screen, pointer_radius=1, pointer_probability=0.5):
    self.width = width
    self.height = height
    self.grid = [[0 for _ in range(width)] for _ in range(height)]
    self.screen = screen
    self.pointer_radius = pointer_radius
    self.pointer_probability = pointer_probability
    self.set_default_pointer()

  def set_default_pointer(self):
    self.pointer = [self.width // 2, self.height // 2]
    self.pointer_prev_value = self.get(self.pointer[0], self.pointer[1])
    self.set(self.pointer[0], self.pointer[1], 1)

  def move_pointer(self, x, y):
    if self.screen.is_drawable(self.pointer[0] + x, self.pointer[1] + y) == False:
      return

    self.set(self.pointer[0], self.pointer[1], self.pointer_prev_value)
    self.pointer[0] += x
    self.pointer[1] += y
    self.pointer_prev_value = self.get(self.pointer[0], self.pointer[1])
    self.set(self.pointer[0], self.pointer[1], 1)

  def place(self, value):
    for x in range(self.pointer[0] - self.pointer_radius, self.pointer[0] + self.pointer_radius + 1):
      for y in range(self.pointer[1] - self.pointer_radius, self.pointer[1] + self.pointer_radius + 1):
        if random.random() < self.pointer_probability:
          self.set(x, y, value)

  def update_pixel(self, x, y):
    under = (x, y + 1)
    under_left = (x - 1, y + 1)
    under_right = (x + 1, y + 1)

    if self.screen.is_drawable(*under) == False and self.screen.is_drawable(*under_left) == False and self.screen.is_drawable(*under_right) == False:
      return

    if self.screen.is_drawable(*under) and self.is_empty(*under):
      self.swap(x, y, *under)
    elif self.screen.is_drawable(*under_left) and self.is_empty(*under_left):
      self.swap(x, y, *under_left)
    elif self.screen.is_drawable(*under_right) and self.is_empty(*under_right):
      self.swap(x, y, *under_right)

  def update(self):
    for y in range(self.height - 1, -1, -1):
      for x in range(self.width):
        if (x, y) != tuple(self.pointer):
            self.update_pixel(x, y)

  def get(self, x, y):
    return self.grid[y][x]

  def is_empty(self, x, y):
    return self.get(x, y) == 0
  
  def set(self, x, y, value):
    if self.screen.is_drawable(x, y) == False:
      return
    self.grid[y][x] = value

  def swap(self, x1, y1, x2, y2):
    self.grid[y1][x1], self.grid[y2][x2] = self.grid[y2][x2], self.grid[y1][x1]

  def clear(self):
    self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
    self.set_default_pointer()

  def get_grid(self):
    return self.grid

def get_random_color():
  return round(random.random(), 1)

def main():
    pygame.init()
    screen = PharmaScreen(True)

    grid = Grid(SCREEN_SIZE, SCREEN_SIZE,screen, 1, 0.5)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            grid.move_pointer(-1, 0)
        if pressed_keys[pygame.K_RIGHT]:
            grid.move_pointer(1, 0)
        if pressed_keys[pygame.K_UP]:
            grid.move_pointer(0, -1)
        if pressed_keys[pygame.K_DOWN]:
            grid.move_pointer(0, 1)

        if pressed_keys[pygame.K_SPACE]:
            grid.place(get_random_color())

        if pressed_keys[pygame.K_c]:
            grid.clear()

        grid.update()

        screen.set_image(grid.get_grid())

    pygame.quit()

if __name__ == "__main__":
    main()