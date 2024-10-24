import itertools
import json
from typing import List

import cv2
import pygame
import socket
import numpy as np
import numpy.typing as npt

PANEL_SIZE = 16  # Size of a single panel on the cross, in pixels
SCREEN_SIZE = 3 * PANEL_SIZE  # Width and height of the cross, in pixels
PIXEL_SIZE = 20  # Width of each square representing an LED
PIXEL_RADIUS_RATIO = 0.5  # Relative diameter of each LED
FPS_2COLOR = 60
FPS_8COLOR = 20
GREEN_BRIGHTNESS = 180  # Brightness (0-255) of the brightest green
COLOR_DEPTH = 3  # Number of bits in each shade of green

cross_mask = np.array([
    [0, 255, 0],
    [255, 255, 255],
    [0, 255, 0],
], dtype=np.uint8)
cross_mask = cv2.resize(cross_mask, (SCREEN_SIZE, SCREEN_SIZE), interpolation=cv2.INTER_NEAREST)


class PharmaScreen:
    def __init__(self, color_scale=True, server_ip='192.168.10.10'):
        """
        An object representing the pharmacy cross screen for local simulation and remote control of the actual cross.
        Args:
            - `color_scale` enables up to 8 shades of green to be displayed, but reduces the expected framerate from 60 to 20FPS.
            - `server_ip` is the address of the controller where update packets should be transmitted. If None, the screen is only simulated locally.
        """
        self.server_ip = server_ip
        if server_ip is not None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.socket.connect(('192.168.1.107', 1337))
            #print('Socket connected')
        self.color_scale = color_scale
        self.local_screen = pygame.display.set_mode(
            [PIXEL_SIZE * SCREEN_SIZE, PIXEL_SIZE * SCREEN_SIZE]
        )
        self.pixel_buffer = [
            [0.0 for c in range(SCREEN_SIZE)] for r in range(SCREEN_SIZE)
        ]
        self.clock = pygame.time.Clock()
        self.fps = FPS_8COLOR if color_scale else FPS_2COLOR
        self.font = pygame.font.SysFont(None, 24)

    def is_drawable(self, row: int, col: int) -> bool:
        """
        Returns whether the given coordinates match an actual LED on the screen.
        """
        if not (0 <= row < SCREEN_SIZE and 0 <= col < SCREEN_SIZE):
            return False
        return int(cross_mask[row, col]) > 0

    def set_image_u8(self, img_u8: npt.NDArray):
        """
        Sets the image to be displayed.

        The `image` argument should be a 2D numpy array of uint8 representing the pixels.
        Values range from 0 (off) to 255 (brightest).
        Note that 4 sections of the image will be ignored as the screen is a cross.

        For float images, see function: set_image
        """
        if img_u8.shape != (SCREEN_SIZE, SCREEN_SIZE):
            raise ValueError(
                f"Invalid image size (expected {SCREEN_SIZE}x{SCREEN_SIZE}, got {img_u8.shape})"
            )

        if img_u8.dtype != np.uint8:
            raise ValueError("Image type must be uint8")

        self.local_screen.fill((0, 0, 0))


        quantized_frame = img_u8 // 32
        if self.server_ip is not None:
            frameenc = json.dumps(quantized_frame.tolist()).encode()
            # print(len(frameenc))
            # self.socket.sendall(frameenc)
            self.socket.sendto(frameenc, (self.server_ip, 1337))
            print('Frame sent')

        if self.color_scale:
            quantized_frame = quantized_frame.astype(float) / 7
        else:
            quantized_frame = (quantized_frame // 4).astype(float)

        for r, c in np.argwhere(cross_mask > 0):
            led_color = (30, 30 + GREEN_BRIGHTNESS * quantized_frame[r, c], 30)
            center = (PIXEL_SIZE * (c + 0.5), PIXEL_SIZE * (r + 0.5))
            pygame.draw.circle(
                self.local_screen,
                led_color,
                center,
                PIXEL_SIZE * PIXEL_RADIUS_RATIO / 2,
            )

        current_fps = self.clock.get_fps()
        fps_img = self.font.render(f"FPS: {current_fps:.1f}", True, (0, 100, 0))
        self.local_screen.blit(fps_img, (0, 0))
        pygame.display.flip()
        self.frame_timing = self.clock.tick(self.fps)

    def set_image(self, image: List[List[float]]):
        """
        Sets the image to be displayed.

        The `image` argument should be an array of floats representing the pixels in (row, column) order.
        Values range from 0.0 (off) to 1.0 (brightest).
        Note that 4 sections of the image will be ignored as the screen is a cross.

        For uint8 images, see function: set_image_u8
        """
        arr = np.array(image, dtype=float)

        if arr.shape != (SCREEN_SIZE, SCREEN_SIZE):
            raise ValueError(
                f"Invalid image size (expected {SCREEN_SIZE}x{SCREEN_SIZE}, got {arr.shape})"
            )

        if arr.flatten().min() < 0.0 or 1.0 < arr.flatten().max():
            raise ValueError("Pixel values must be between 0.0 and 1.0")

        im8 = np.round(arr * 255).astype(np.uint8)
        self.set_image_u8(im8)
