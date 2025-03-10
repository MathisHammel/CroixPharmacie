"""
 Copyright(C) 2024 Wojciech Graj
 Copyright(C) 2024 Miika Lönnqvist

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
"""


import sys

import cv2
import cydoomgeneric as cdg
import numpy as np
import pygame

from pharmacontroller import PharmaScreen

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400
DEBUGGER = True

keymap = {
    pygame.K_LEFT: cdg.Keys.LEFTARROW,
    pygame.K_RIGHT: cdg.Keys.RIGHTARROW,
    pygame.K_UP: cdg.Keys.UPARROW,
    pygame.K_DOWN: cdg.Keys.DOWNARROW,
    pygame.K_COMMA: cdg.Keys.STRAFE_L,
    pygame.K_PERIOD: cdg.Keys.STRAFE_R,
    pygame.K_LCTRL: cdg.Keys.FIRE,
    pygame.K_SPACE: cdg.Keys.USE,
    pygame.K_RSHIFT: cdg.Keys.RSHIFT,
    pygame.K_RETURN: cdg.Keys.ENTER,
    pygame.K_ESCAPE: cdg.Keys.ESCAPE,
}

def draw_frame(screen, pixels, debug_figax) -> None:
    if DEBUGGER:
        fig, ax = debug_figax
        ax.clear()
        ax.imshow(pixels[:,:,[2,1,0]])
        fig.canvas.draw()
        fig.canvas.flush_events()

    # Resize pixels to a 48x77 array with interpolation
    pixels = cv2.resize(pixels, (77, 48), interpolation=cv2.INTER_CUBIC)

    # Flatten rgba to grayscale and normalize to [0.0, 1.0]
    pixels = pixels.mean(axis=2) / 255.0

    # Crop to 48x48 centered
    pixels = pixels[:, 14:62]

    screen.set_image(pixels[:48][:48])

def get_key():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in keymap:
                return 1, keymap[event.key]
        
        if event.type == pygame.KEYUP:
            if event.key in keymap:
                return 0, keymap[event.key]
            
    return None

if __name__ == '__main__':
    pygame.init()
    screen = PharmaScreen()

    if DEBUGGER:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        debug_figax = (fig, ax)
        fig.show()
    else:
        debug_figax = None

    cdg.init(SCREEN_WIDTH,
        SCREEN_HEIGHT,
        lambda pixels: draw_frame(screen, pixels, debug_figax),
        get_key)
    cdg.main()
