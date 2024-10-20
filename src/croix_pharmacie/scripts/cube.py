from math import sin

import numpy as np
import pygame

from croix_pharmacie.pharmacontroller import PharmaScreen

size = 48
vertices = (
    np.array(
        [
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1],
        ]
    )
    * 0.5
)

edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
]


def project(points, angle):
    Rx = np.array(
        [
            [1, 0, 0],
            [0, np.cos(angle[0]), -np.sin(angle[0])],
            [0, np.sin(angle[0]), np.cos(angle[0])],
        ]
    )
    Ry = np.array(
        [
            [np.cos(angle[1]), 0, np.sin(angle[1])],
            [0, 1, 0],
            [-np.sin(angle[1]), 0, np.cos(angle[1])],
        ]
    )
    Rz = np.array(
        [
            [np.cos(angle[2]), -np.sin(angle[2]), 0],
            [np.sin(angle[2]), np.cos(angle[2]), 0],
            [0, 0, 1],
        ]
    )

    rotated = points @ Rx @ Ry @ Rz
    projected = rotated[:, :2]
    return projected


def update_matrix(matrix, projected_vertices, edges):
    matrix.fill(0)
    for edge in edges:
        start, end = projected_vertices[edge]
        x0, y0 = int((start[0] + 1) * (size / 2)), int((start[1] + 1) * (size / 2))
        x1, y1 = int((end[0] + 1) * (size / 2)), int((end[1] + 1) * (size / 2))
        bresenham(matrix, x0, y0, x1, y1)


def bresenham(matrix, x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if 0 <= x0 < size and 0 <= y0 < size:
            matrix[y0, x0] = 1
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def main():
    pygame.init()
    screen = PharmaScreen()
    matrix = np.zeros((size, size), dtype=int)

    k = 0
    while True:
        k += 0.01
        angle_rad = np.radians(360 * abs(sin(k)))
        angles = np.array([angle_rad, angle_rad, angle_rad])
        projected_vertices = project(vertices, angles)
        update_matrix(matrix, projected_vertices, edges)
        screen.set_image(matrix.tolist())

if __name__ == "__main__":
    main()