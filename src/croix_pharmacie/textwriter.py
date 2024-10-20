import pygame

import sys
import time
import json

from .asset_helper import get_asset_path
from .pharmacontroller import PharmaScreen, SCREEN_SIZE

# loads the letters
with open(get_asset_path("letters.json"), "r") as f:
    LETTERS = json.load(f)
    f.close()

class Letter:
    def __init__(self, symbol:str, coords:tuple):
        """A class to represent a letter on the cross

        Args:
            - symbol (str): the char represented
            - coords (tuple): coordinates of the letter in the cross
        """
        assert len(symbol) == 1, f"A letter needs to be 1 character long, {symbol} is empty or more than 1 char"
        self.symbol = symbol.strip().upper()
        self.coords = coords
        # Representation of the letter in matrix form
        self.matrix = LETTERS[symbol]
        # Dimensions in dots
        self.width = len(self.matrix[0])
        self.height = len(self.matrix)

    def draw(self, image, inverted:bool = False, xbounds:tuple = (0,False)):
        """Draw the letter at its coordinates

        Args:
            - image (list): the matrix representing the screen to draw on
            - inverted (bool, optional): Determine if the letter is green or disabled. Defaults to False.
            - xbounds (tuple, optional): Limits of the letter, the first element of the tuple is the minimal coord where the letter can be drawn. The second is the limit on the right side. Defaults to (0,False).
        """
        # determine if the letter is cutted on the left
        left_cut = xbounds[0] - self.coords[0]
        if left_cut < 0: left_cut = 0

        for y, line in enumerate(image[self.coords[1]:self.coords[1] + self.height]):
            for x in range(left_cut, self.width):
                overflow = xbounds[1] and self.coords[0] + x > xbounds[1]
                if overflow:
                    break
                color = 1 ^ self.matrix[y][x] if inverted else self.matrix[y][x]
                line[self.coords[0] + x] = color

    def __str__(self) -> str:
        return self.symbol

class String:
    def __init__(self, image, coords:tuple, width:int, text:str, cooldown:float = 0.05, timeout:float = 0.3):
        """A class to represent a string on the cross

        Args:
            - image (list): the matrix representing the screen to draw on
            - coords (tuple): the coordinates of the string on the cross
            - width (int): width of the string (the limit where the string will not be displayed)
            - text (str): the text to display
            - cooldown (float, optional): cooldown betwen letters scroll. Defaults to 0.05.
            - timeout (float, optional): time before the text return on the screen. Defaults to 0.3.
        """
        self.image = image
        self.coords = coords
        self.width = width
        # x coord of the string right limit
        self.xlimit = self.coords[0] + self.width

        self.cooldown = cooldown
        self.time = time.time()
        self.timeout = timeout
        self.timeout_state = False

        # Coords are specified when drawing
        self.letters = list(
            map(lambda x: Letter(x, (0, 0)), text.upper().strip())
        )
        # Actual width of the string
        self.dot_width = sum(map(lambda x: x.width, self.letters))
        self.dot_width += (len(self.letters) - 1) # <-- spaces between letters 
        
        # Starts off limit
        self.current_pos = (self.coords[0] + width, self.coords[1]) 

    def set_pos(self, coords:tuple):
        """Setter for the current position

        Args:
            - coords (tuple): New coordinates of the string 
        """
        self.current_pos = coords

    def draw(self, inverted=False):
        """Show the string on the cross, the string limits and current position matter. 

        Args:
            - inverted (bool, optional): Determine if the letter are green or disabled. Defaults to False.
        """
        temp_width = 0
        for letter in self.letters:
            letter.coords = (self.current_pos[0] + temp_width, self.coords[1])
            letter_right = letter.coords[0] + letter.width
            # Verify if the letter overflow on the right
            if letter_right <= self.xlimit :
                limit = False
            elif letter_right > self.xlimit and letter.coords[0] <= self.xlimit:
                limit = self.xlimit
            else:
                break

            letter.draw(self.image, inverted, xbounds=(self.coords[0], limit)) 
            temp_width += letter.width + 1

    def scroll(self, inverted=False):
        """Scroll the text, starts off the bounds then comme on the cross

        Args:
            - inverted (bool, optional): Determine if the letter are green or disabled. Defaults to False.
        """
        if self.timeout_state:
            if time.time() - self.time >= self.timeout:
                self.timeout_state = False
            else:
                return
        if time.time() - self.time >= self.cooldown:
            self.set_pos((self.current_pos[0] - 1, self.current_pos[1]))
            self.time = time.time()
        self.draw(inverted)
        if self.current_pos[0] + self.dot_width < self.coords[0]:
            self.current_pos = (self.coords[0] + self.width, self.coords[1])
            self.timeout_state = True

if __name__ == '__main__':
    INVERTED:bool = True # Set the color of the letters to green or disabled

    pygame.init()
    screen = PharmaScreen(color_scale=False)

    image = [[0 for c in range(SCREEN_SIZE)] for r in range(SCREEN_SIZE)]
    s = String(image, (1, 18), 45, "I use Arch btw", cooldown=0.05, timeout=2)
    
    running = True
    while running:
        
        # Color for the middle line of the cross 
        for line in image[16:32]:
            for i in range(len(line)):
                line[i] = (int(INVERTED))

        s.scroll(inverted=INVERTED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        screen.set_image(image)