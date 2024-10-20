import itertools
import json
from typing import List
import pygame
import socket
import time

# Constants
PANEL_SIZE = 16           # Size of a single panel on the cross, in pixels
SCREEN_SIZE = 3 * PANEL_SIZE  # Width and height of the cross, in pixels
PIXEL_SIZE = 20           # Width of each square representing an LED
PIXEL_RADIUS_RATIO = 0.5  # Relative diameter of each LED
FPS_2COLOR = 60           # Frame rate for 2-color mode
FPS_8COLOR = 20           # Frame rate for 8-color mode
GREEN_BRIGHTNESS = 220    # Brightness (0-255) of the brightest green
COLOR_DEPTH = 3           # Number of bits in each shade of green
GAME_TIME_LIMIT = 30      # Time limit for the game (seconds)


class PharmaScreen:
    def __init__(self, color_scale=True, server_ip=None):
        """
        Object representing the pharmacy cross screen for local simulation and remote control.
        Args:
            - `color_scale`: Enables 8 shades of green with reduced FPS (20 FPS), defaults to True.
            - `server_ip`: IP address of the controller for remote updates. If None, simulates locally.
        """
        self.server_ip = server_ip
        self.color_scale = color_scale
        self.socket = None

        if server_ip is not None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Initialize local screen for simulation
        pygame.init()
        self.local_screen = pygame.display.set_mode(
            [PIXEL_SIZE * SCREEN_SIZE, PIXEL_SIZE * SCREEN_SIZE]
        )
        pygame.display.set_caption("Pharma Cross Challenge")  # Set the game title
        self.pixel_buffer = [
            [0.0 for _ in range(SCREEN_SIZE)] for _ in range(SCREEN_SIZE)
        ]
        self.clock = pygame.time.Clock()
        self.fps = FPS_8COLOR if color_scale else FPS_2COLOR
        self.font = pygame.font.SysFont(None, 24)

    def is_drawable(self, row: int, col: int) -> bool:
        """
        Check if the given coordinates correspond to an actual LED on the cross screen.
        """
        if not (0 <= row < SCREEN_SIZE and 0 <= col < SCREEN_SIZE):
            return False

        panel_coords = (row // PANEL_SIZE, col // PANEL_SIZE)
        return panel_coords in ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1))

    def set_image(self, image: List[List[float]]):
        """
        Set the image to be displayed. The image should be a 2D list with float values between 0.0 and 1.0.
        Pixels that are part of the cross will be rendered, others will be ignored.
        """
        self.local_screen.fill((0, 0, 0))  # Clear the screen

        for r, c in itertools.product(range(SCREEN_SIZE), repeat=2):
            if self.is_drawable(r, c):
                quantizer = 7 if self.color_scale else 1
                quantized_color = round(image[r][c] * quantizer) / quantizer
                led_color = (30, 30 + int(GREEN_BRIGHTNESS * quantized_color), 30)
                center = (PIXEL_SIZE * (c + 0.5), PIXEL_SIZE * (r + 0.5))
                pygame.draw.circle(
                    self.local_screen,
                    led_color,
                    center,
                    PIXEL_SIZE * PIXEL_RADIUS_RATIO / 2,
                )

        pygame.display.flip()
        self.clock.tick(self.fps)

    def set_pixel(self, row: int, col: int, brightness: float):
        """
        Sets the brightness of a single pixel, only if it's part of the cross.
        """
        if self.is_drawable(row, col):
            self.pixel_buffer[row][col] = brightness

    def update_image(self):
        """
        Updates the display with the current pixel buffer.
        """
        self.set_image(self.pixel_buffer)

    def is_complete(self):
        """
        Check if all the valid pixels (cross shape) are fully lit.
        """
        for r, c in itertools.product(range(SCREEN_SIZE), repeat=2):
            if self.is_drawable(r, c) and self.pixel_buffer[r][c] < 1.0:
                return False
        return True


def run_game():
    """
    Main function to run the Pharma Cross Challenge game.
    
    Game Rules:
    1. Objective:
       - Light up all the LEDs that form the cross shape on the screen within 30 seconds.

    2. Gameplay:
       - Click on the pixels to toggle their brightness.
       - Clicking on a valid LED (part of the cross) will turn it on or off.
       - Invalid clicks (on non-cross pixels) have no effect.

    3. Winning Condition:
       - You win if you light up all the valid LEDs (the cross) before the time runs out.

    4. Losing Condition:
       - You lose if the time runs out and not all LEDs are lit.

    5. Timer:
       - The remaining time is displayed on the screen during gameplay, counting down from 30 seconds.
    """
    # Initialize the pharmacy screen
    screen = PharmaScreen(color_scale=True)
    
    running = True
    start_time = time.time()

    # Game loop
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = mouse_y // PIXEL_SIZE
                col = mouse_x // PIXEL_SIZE

                # Toggle LED brightness on click if it's part of the cross
                if screen.is_drawable(row, col):
                    current_brightness = screen.pixel_buffer[row][col]
                    new_brightness = 1.0 if current_brightness < 1.0 else 0.0
                    screen.set_pixel(row, col, new_brightness)

        # Update the screen
        screen.update_image()

        # Check game timer
        elapsed_time = time.time() - start_time
        if elapsed_time > GAME_TIME_LIMIT:
            print("Time's up! You lost.")  # Notify player they lost
            running = False

        # Check if all LEDs are lit (win condition)
        if screen.is_complete():
            print("Congratulations! You won!")  # Notify player they won
            running = False

        # Show timer
        remaining_time = GAME_TIME_LIMIT - elapsed_time
        timer_text = screen.font.render(f"Time: {remaining_time:.1f}", True, (255, 0, 0))
        screen.local_screen.blit(timer_text, (10, 10))
        pygame.display.flip()

    # Quit pygame
    pygame.quit()


if __name__ == "__main__":
    run_game()
