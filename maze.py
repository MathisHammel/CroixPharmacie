import sys
import pygame
import threading
from pharmacontroller import SCREEN_SIZE, PharmaScreen
from textwriter import String

# Constants for the game
TRAIL_TIME = 5  # Time in seconds before trail disappears

game_started = False
game_over = False

# Directions (example level input)
level_directions = [
   "right", "right", "right", "right", "right", "right", "up", "right", "up", "up", "up", "up", "up", "up", "up", "up", "up", "up", "up", "up", "up", "left", "up", "up", "right", "right",
   "up", "up", "up", "up", "up", "up", "up", "up", "up", "up", "up", "up", "right", "right", "right", "up", "up", "left", "up", "left", "left", "left", "left", "left", "left", "left",
   "up", "up", "up", "up", "up", "up", "up", "up", "left", "left", "left", "up", "up", "up", "up", "up", "up", "up", "up"
]
# To create level, copy the array above with the same name and replace the directions with the correct ones

# Colors
TRAIL_COLOR = 1.0  # Using 1.0 value for 'on' pixels
EMPTY_COLOR = 0.0  # Using 0.0 value for 'off' pixels

pygame.init()

# Define movement directions as x, y deltas
DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

class Player:
    def __init__(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.trail = [(self.x, self.y)]  # Start trail with initial position
        self.trail_directions = []

    def move(self, direction, maze=None):
        if direction in DIRECTIONS:
            dx, dy = DIRECTIONS[direction]
            self.trail_directions.append(direction)
            new_x = self.x + dx
            new_y = self.y + dy
            # Make sure the player stays within the bounds
            if 0 <= new_x < SCREEN_SIZE and 0 <= new_y < SCREEN_SIZE:
                self.x = new_x
                self.y = new_y
                self.trail.append((self.x, self.y))

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.trail = [(self.x, self.y)]  # Reset trail to the initial position
        self.trail_directions = []

def draw_trail(screen, player, show_trail=True):
    # Fill screen with blank (off pixels)
    screen.pixel_buffer = [[EMPTY_COLOR for _ in range(SCREEN_SIZE)] for _ in range(SCREEN_SIZE)]

    # Draw player trail
    if show_trail:
        for pos in player.trail:
            draw_cell(screen, pos[1], pos[0], TRAIL_COLOR)

    # Draw player
    draw_cell(screen, player.y, player.x, TRAIL_COLOR)
    screen.set_image(screen.pixel_buffer)


def draw_cell(screen, row, col, color):
    if screen.is_drawable(row, col):
        screen.pixel_buffer[row][col] = color

def check_trail(player):
    image = [[0.0 for c in range(SCREEN_SIZE)] for r in range(SCREEN_SIZE)]

    loosing_string = String(image, (1, 18), 45, "Y o u  L o s t")
    winning_string = String(image, (1, 18), 45, "L e v e l C l e a r e d", cooldown=0.03, timeout=0)

    current_length = len(player.trail_directions)
    if player.trail_directions != level_directions[:current_length]:
        return loosing_string, True  # Return "You Lost" and set game_over as True
    elif player.trail_directions == level_directions:
        return winning_string, True   # Return "Level Cleared" and set game_over as True
    return None, False  # No game over yet

# Function to hide trail after TRAIL_TIME and reset the player's position
def hide_trail(player):
    player.reset()  # Reset the player's position and trail
    global game_started
    game_started = True

def display_message_until_escape(string_object, screen):
    """Display the string message until the player presses ESC to exit."""
    image = [[0.0 for c in range(SCREEN_SIZE)] for r in range(SCREEN_SIZE)]
    string_object.image = image

    running = True
    while running:
        # Keep showing the message until ESC is pressed
        string_object.scroll(inverted=False)
        screen.set_image(image)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.time.Clock().tick(30)

def game_loop():
    # Define starting point at the very bottom middle of the cross
    start_x = SCREEN_SIZE // 2  # Middle of the screen horizontally
    start_y = SCREEN_SIZE - 1   # Very bottom of the screen
    player = Player(start_x, start_y)

    screen = PharmaScreen(True)

    # Start a timer to hide the trail after TRAIL_TIME and reset the player
    threading.Timer(TRAIL_TIME, lambda: hide_trail(player)).start()

    for direction in level_directions:
        player.move(direction)

    global game_over

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move("left")
                elif event.key == pygame.K_RIGHT:
                    player.move("right")
                elif event.key == pygame.K_UP:
                    player.move("up")
                elif event.key == pygame.K_DOWN:
                    player.move("down")

        draw_trail(screen, player, show_trail=True)
        
        if game_started and not game_over:
            string_object, game_over = check_trail(player)
            if game_over:
                display_message_until_escape(string_object, screen)

        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    game_loop()
