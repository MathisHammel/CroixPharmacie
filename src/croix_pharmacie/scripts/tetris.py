import pygame, sys, time, random
from collections import defaultdict
from croix_pharmacie.pharmacontroller import SCREEN_SIZE, PANEL_SIZE, PharmaScreen

"""
TETRIS, pharmacy cross edition
- Use left/right arrows or q/s to move to the side
- Use up arrow or z to rotate 90° clockwise
- Use down arrow or s to move down faster

- Press enter to restart
"""

# Parameters
KEY_COOLDOWN = .1           # Time before checking again sideways displacements (in s)
START_SPEED = .5            # Time between two down movements of the falling piece at the start (in s)
SPEEDUP_FACTOR = .94        # Factor by which the previously mentionned time is multiplied when completing a line
SCALE = 2                   # Width in cross pixels of a single piece pixel (should be 1 or 2)
SHOW_FINAL_POS = True       # Whether or not to show the final position
FINAL_POS_BLINK_DELAY = .2  # Blinking period of the final position (in s)
FULL_BRIGHT = 1             # Brightness of the main elements (between 0 and 1)
LIGHT_BRIGHT = 2/8          # Brightness of the edge and final position (between 0 and 1)
POINTS = [1, 4, 9, 16]      # Points earned by completing 1, 2, 3 and 4 lines at once respectively

DEBUG = False

# Constants
HEIGHT = SCREEN_SIZE // SCALE
WIDTH = PANEL_SIZE // SCALE

PIECES = [
    [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]], # I
    [[1, 1], [1, 1]], # O
    [[0, 1, 1], [1, 1, 0], [0, 0, 0]], # S
    [[1, 1, 0], [0, 1, 1], [0, 0, 0]], # Z
    [[0, 1, 0], [0, 1, 0], [0, 1, 1]], # L
    [[0, 1, 0], [0, 1, 0], [1, 1, 0]], # J
    [[0, 0, 0], [1, 1, 1], [0, 1, 0]], # T
]
LETTERS = {
    'A': [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 0, 1]],
    'C': [[1, 1, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 1, 1]],
    'E': [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 1, 1]],
    'G': [[1, 1, 1], [1, 0, 0], [1, 0, 0], [1, 0, 1], [1, 1, 1]],
    'N': [[1, 1, 0], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1]],
    'M': [[1, 0, 0, 0, 1], [1, 1, 0, 1, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1]],
    'O': [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
    'P': [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 0], [1, 0, 0]],
    'R': [[1, 1, 1], [1, 0, 1], [1, 1, 0], [1, 0, 1], [1, 0, 1]],
    'S': [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    'T': [[1, 1, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
    'V': [[1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [0, 1, 0]],
    'X': [[1, 0, 1], [1, 0, 1], [0, 1, 0], [1, 0, 1], [1, 0, 1]],
    '0': [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
    '1': [[0, 1, 0], [1, 1, 0], [0, 1, 0], [0, 1, 0], [1, 1, 1]],
    '2': [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
    '3': [[1, 1, 1], [0, 0, 1], [0, 1, 1], [0, 0, 1], [1, 1, 1]],
    '4': [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
    '5': [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    '6': [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    '7': [[1, 1, 1], [0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 0, 0]],
    '8': [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    '9': [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    ':': [[0], [1], [0], [1], [0]],
    ' ': [[0], [0], [0], [0], [0]],
}

# Code to handle pieces
def random_piece():
    piece = random.choice(PIECES)
    for _ in range(random.randrange(4)):
        piece = rotate_piece(piece)

    return piece

def rotate_piece(piece):
    piece = [line for line in piece[::-1]]
    piece = [[piece[x][y] for x in range(len(piece))] for y in range(len(piece))]

    return piece

# Drawing code
def draw_pixel(image, y, x, bright=FULL_BRIGHT):
    if not (0 <= y < SCREEN_SIZE and 0 <= x < SCREEN_SIZE):
        if DEBUG:
            print(f'Warning: Trying to draw pixel out of bounds at ({y}, {x}).')
        return
    bright = max(0, min(1, bright))

    image[y][x] = bright

def draw_letter(image, c, y, x, bright=FULL_BRIGHT, letter_scale=1):
    letter = LETTERS[c]
    for dy in range(len(letter)):
        for dx in range(len(letter[0])):
            for ddy in range(letter_scale):
                for ddx in range(letter_scale):
                    draw_pixel(image, y + letter_scale * dy + ddy, x + letter_scale * dx + ddx, letter[dy][dx] * bright)

    return letter_scale * (len(letter[0]) + 1)

def draw_text(image, text, y, x, bright=FULL_BRIGHT, letter_scale=1):
    for c in text:
        x += draw_letter(image, c, y, x, bright, letter_scale)

    return x

def draw_piece(image, piece, y, x, bright=FULL_BRIGHT, scale=SCALE):
    """Draw piece by its absolute coordinates"""
    for dy in range(len(piece)):
        for dx in range(len(piece[0])):
            if piece[dy][dx]:
                for ddy in range(scale):
                    for ddx in range(scale):
                        draw_pixel(image, y + scale * dy + ddy, x + scale * dx + ddx, bright)

def draw_piece_grid(image, piece, y, x, bright=FULL_BRIGHT):
    """Draw piece by its grid coordinates"""
    draw_piece(image, piece, SCALE * y, PANEL_SIZE + SCALE * x, bright)

# Main game code
class Tetris:
    def __init__(self):
        # Init grid
        self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

        # Generate first piece
        self.next_piece = random_piece()
        self.new_piece()

        # Parameters
        self.speed = START_SPEED
        self.score = 0
        self.running = True
        self.last_event_time = defaultdict(int)
        self.show_final_pos = True
        self.game_over_scrolling = 0

    def new_piece(self):
        # If we can't place the new piece, game over
        if not self.check_piece(0, (WIDTH - 1) // 2, self.next_piece):
            return self.game_over()

        # Initialize the new piece
        self.current_piece = self.next_piece
        self.next_piece = random_piece()
        self.piece_y = 0
        self.piece_x = (WIDTH - 1) // 2

    def update(self, force=False):
        # Check if enough time has elapsed since last time
        if not force and time.time() - self.last_event_time['move'] < self.speed:
            return
        self.last_event_time['move'] = time.time()

        # Check if the piece can go down
        new_y = self.piece_y + 1
        if self.check_piece(new_y, self.piece_x, self.current_piece):
            self.piece_y = new_y
        else:
            self.deposit_piece()
            self.new_piece()

    def step(self):
        if self.running:
            self.handle_input(pygame.key.get_pressed())
            self.update()

            return self.generate_image()
        else:
            image = [[0 for _ in range(SCREEN_SIZE)] for _ in range(SCREEN_SIZE)]

            final_pix_x = draw_text(
                image,
                f'GAME OVER      SCORE: {self.score}      ',
                PANEL_SIZE + 3,
                SCREEN_SIZE - self.game_over_scrolling,
                letter_scale=2
            )

            # Handle text scrolling
            self.game_over_scrolling += 1
            if final_pix_x < 0:
                self.game_over_scrolling = 0

            return image

    def game_over(self):
        self.running = False

    def handle_keydown(self, key_pressed):
        """Handle keydown events"""
        if key_pressed == pygame.K_UP or key_pressed == pygame.K_z:
            # Arrow up / z: rotate piece
            new_piece = rotate_piece(self.current_piece)
            if self.check_piece(self.piece_y, self.piece_x, new_piece):
                self.current_piece = new_piece

            elif self.check_piece(self.piece_y, self.piece_x + 1, new_piece):
                self.current_piece = new_piece
                self.piece_x += 1

            elif self.check_piece(self.piece_y, self.piece_x - 1, new_piece):
                self.current_piece = new_piece
                self.piece_x -= 1

        elif key_pressed == pygame.K_RETURN and (DEBUG or not self.running):
            # Enter: restart game
            self.__init__()

    def handle_input(self, key_pressed):
        """Handle currently pressed keys"""
        if (key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_q]) and time.time() - self.last_event_time['left'] > KEY_COOLDOWN:
            # Arrow left / q: move current piece left
            self.last_event_time['left'] = time.time()

            new_piece_x = self.piece_x - 1
            if self.check_piece(self.piece_y, new_piece_x, self.current_piece):
                self.piece_x = new_piece_x

        elif (key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]) and time.time() - self.last_event_time['right'] > KEY_COOLDOWN:
            # Arrow right / d: move current piece right
            self.last_event_time['right'] = time.time()

            new_piece_x = self.piece_x + 1
            if self.check_piece(self.piece_y, new_piece_x, self.current_piece):
                self.piece_x = new_piece_x

        elif key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            # Arrow down / s: move the piece down one pixel
            self.update(True)

        elif DEBUG and key_pressed[pygame.K_r]:
            # (Debug) r: Force a game over
            self.game_over()

    def deposit_piece(self):
        assert self.check_piece(self.piece_y, self.piece_x, self.current_piece)

        # Place the piece on the grid
        for dy in range(len(self.current_piece)):
            for dx in range(len(self.current_piece)):
                if self.current_piece[dy][dx]:
                    self.grid[self.piece_y + dy][self.piece_x + dx] = 1

        # Check if rows were completed
        completed_rows = 0
        for y in range(HEIGHT):
            if all(self.grid[y]):
                self.grid.pop(y)
                self.grid = [[0 for _ in range(WIDTH)]] + self.grid

                completed_rows += 1
                self.speed *= SPEEDUP_FACTOR

        if completed_rows > 0:
            self.score += POINTS[completed_rows - 1]

    def check_piece(self, piece_y, piece_x, piece):
        for dy in range(len(piece)):
            for dx in range(len(piece)):
                if not piece[dy][dx]:
                    continue

                grid_y, grid_x = piece_y + dy, piece_x + dx
                if not (0 <= grid_y < HEIGHT and 0 <= grid_x < WIDTH):
                    return False

                if self.grid[grid_y][grid_x]:
                    return False

        return True

    def get_end_pos(self):
        y = self.piece_y
        while self.check_piece(y + 1, self.piece_x, self.current_piece):
            y += 1

        return (y, self.piece_x)

    def generate_image(self):
        image = [[0.0 for _ in range(SCREEN_SIZE)] for _ in range(SCREEN_SIZE)]

        # Draw center region sides
        for y in range(PANEL_SIZE, 2 * PANEL_SIZE):
            draw_pixel(image, y, PANEL_SIZE - 1, LIGHT_BRIGHT)
            draw_pixel(image, y, PANEL_SIZE * 2, LIGHT_BRIGHT)

        # Draw the fallen pieces
        for y in range(HEIGHT):
            for x in range(WIDTH):
                for dy in range(SCALE):
                    for dx in range(SCALE):
                        draw_pixel(image, SCALE * y + dy, PANEL_SIZE + SCALE * x + dx, self.grid[y][x])

        # Draw the final position of the falling piece
        if SHOW_FINAL_POS:
            final_y, final_x = self.get_end_pos()

            if self.show_final_pos:
                draw_piece_grid(image, self.current_piece, final_y, final_x, LIGHT_BRIGHT)

            if time.time() - self.last_event_time['final_pos'] > FINAL_POS_BLINK_DELAY:
                self.show_final_pos = not self.show_final_pos
                self.last_event_time['final_pos'] = time.time()

        # Draw the falling piece
        draw_piece_grid(image, self.current_piece, self.piece_y, self.piece_x)

        # Draw the next piece
        draw_text(image, 'NXT', PANEL_SIZE + 1, PANEL_SIZE * 2 + 3)

        y_next_piece_offset, x_next_piece_offset = {4: (7, 5), 3: (8, 6), 2: (9, 7)}[len(self.next_piece)]
        draw_piece(image, self.next_piece, PANEL_SIZE + y_next_piece_offset, PANEL_SIZE * 2 + x_next_piece_offset)

        # Draw the score
        draw_text(image, 'PTS', PANEL_SIZE + 1, 2)
        draw_text(image, str(self.score), PANEL_SIZE + 9, 2)

        return image

def main():
    pygame.init()
    screen = PharmaScreen(True)

    game = Tetris()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                game.handle_keydown(event.key)

        screen.set_image(game.step())

if __name__ == "__main__":
    main()