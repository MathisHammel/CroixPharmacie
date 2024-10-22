import math
import random
from abc import abstractmethod, ABC

import pygame
from pygame import Rect

from croix_pharmacie.pharmacontroller import PharmaScreen, SCREEN_SIZE

HALF_SCREEN_SIZE = SCREEN_SIZE // 2
TIME_SCALE = 0.002


class VisualEffect(ABC):
    def __init__(self) -> None:
        self.screen_image = [[0. for _ in range(SCREEN_SIZE)] for _ in range(SCREEN_SIZE)]

    @abstractmethod
    def update(self, t: float, dt: float) -> None:
        pass


class SpiralPoint(VisualEffect):
    @staticmethod
    def point_intensity(x: int, y: int, t: float) -> float:
        dx, dy = x - HALF_SCREEN_SIZE, y - HALF_SCREEN_SIZE
        angle = math.atan2(dy, dx)
        dist = math.hypot(dx, dy)
        return (math.sin(3 * angle + 0.3 * dist + t) + 1) / 2

    def update(self, t: float, dt: float) -> None:
        for y in range(SCREEN_SIZE):
            for x in range(SCREEN_SIZE):
                self.screen_image[y][x] = self.point_intensity(x, y, t)


class RipplePoint(VisualEffect):
    @staticmethod
    def point_intensity(x: int, y: int, t: float) -> float:
        dist = math.hypot(x - HALF_SCREEN_SIZE, y - HALF_SCREEN_SIZE)
        return (math.sin(dist * 0.1 - t * 2) + 1) / 2

    def update(self, t: float, dt: float) -> None:
        for y in range(SCREEN_SIZE):
            for x in range(SCREEN_SIZE):
                self.screen_image[y][x] = self.point_intensity(x, y, t)


class Radial1Point(VisualEffect):
    @staticmethod
    def point_intensity(x: int, y: int, t: float) -> float:
        distance = math.sqrt((x - HALF_SCREEN_SIZE) ** 2 + (y - HALF_SCREEN_SIZE) ** 2)
        value = math.sin(distance * 0.1 + t)
        intensity = (math.sin(value * math.pi) + 1) / 2
        return intensity

    def update(self, t: float, dt: float) -> None:
        for y in range(SCREEN_SIZE):
            for x in range(SCREEN_SIZE):
                self.screen_image[y][x] = self.point_intensity(x, y, t)


class Radial2Point(VisualEffect):
    @staticmethod
    def point_intensity(x: int, y: int, t: float) -> float:
        cx = (x - HALF_SCREEN_SIZE) / HALF_SCREEN_SIZE
        cy = (y - HALF_SCREEN_SIZE) / HALF_SCREEN_SIZE
        radius = math.sqrt(cx ** 2 + cy ** 2)
        value = math.sin(radius * 10 - t * 5)
        intensity = (value + 1) / 2
        return intensity

    def update(self, t: float, dt: float) -> None:
        for y in range(SCREEN_SIZE):
            for x in range(SCREEN_SIZE):
                self.screen_image[y][x] = self.point_intensity(x, y, t)


class RainEffect(VisualEffect):
    DROP_PROBABILITY = 1 / 70
    DROP_LENGTH = 4
    DROP_INTENSITY = 0.6
    FRAME_TIME = 1 / 10

    def __init__(self) -> None:
        super().__init__()
        self.screen_image[0][HALF_SCREEN_SIZE] = self.DROP_INTENSITY
        self.dt = 0.

    def update(self, t: float, dt: float) -> None:
        self.dt += dt
        if self.dt >= self.FRAME_TIME:
            self.dt = 0.

            for x in range(SCREEN_SIZE):
                if random.random() < self.DROP_PROBABILITY:
                    self.screen_image[0][x] = self.DROP_INTENSITY

                for y in range(SCREEN_SIZE - 1, -1, -1):
                    if self.screen_image[y][x] == 0:
                        if y > 0 and self.screen_image[y - 1][x] != 0:
                            self.screen_image[y][x] = self.DROP_INTENSITY
                    elif y == 0 or self.screen_image[y - 1][x] == 0:
                        length = sum(1 for k in range(y + 1, y + self.DROP_LENGTH + 1) if
                                     k >= SCREEN_SIZE or self.screen_image[k][x] != 0)
                        if length >= self.DROP_LENGTH:
                            self.screen_image[y][x] = 0


class FireEffect(VisualEffect):
    FRAME_TIME = 1 / 4
    TIER_SIZE = SCREEN_SIZE // 3
    ZONES = [
        pygame.Rect(0, TIER_SIZE, TIER_SIZE, TIER_SIZE),
        pygame.Rect(TIER_SIZE, 1 * TIER_SIZE, TIER_SIZE, 2 * TIER_SIZE),
        pygame.Rect(2 * TIER_SIZE, TIER_SIZE, TIER_SIZE, TIER_SIZE)
    ]

    def __init__(self) -> None:
        super().__init__()
        self.dt = 0.

    def generate_fire_source(self, zone: Rect) -> None:
        for c in range(zone.left, zone.right):
            self.screen_image[zone.bottom - 1][c] = random.uniform(0.4, 1.0)

    def propagate_fire(self, zone: Rect) -> None:
        for r in range(zone.top, zone.bottom - 1):
            for c in range(zone.left, zone.right):
                decay = random.uniform(0.02, 0.08)
                below = self.screen_image[r + 1][c]
                self.screen_image[r][c] = max(0.0, below - decay)

    def update(self, t: float, dt: float) -> None:
        self.dt += dt
        if self.dt >= self.FRAME_TIME:
            self.dt = 0.

            for zone in self.ZONES:
                self.generate_fire_source(zone)
                self.propagate_fire(zone)


def main():
    pygame.init()
    screen = PharmaScreen()
    effects = [SpiralPoint(), RipplePoint(), Radial1Point(), Radial2Point(), RainEffect(), FireEffect()]
    effect = 0
    last_time = pygame.time.get_ticks() * TIME_SCALE

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                effect = (effect + 1) % len(effects)

        time = pygame.time.get_ticks() * TIME_SCALE
        dt = time - last_time
        last_time = time

        effects[effect].update(time, dt)
        screen.set_image(effects[effect].screen_image)

    pygame.quit()

if __name__ == "__main__":
    main()