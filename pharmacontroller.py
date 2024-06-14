import pygame
import itertools

PANEL_SIZE = 16 # Size of a single panel on the cross, in pixels
SCREEN_SIZE = 3 * PANEL_SIZE # Width and height of the cross, in pixels
PIXEL_SIZE = 20 # Width of each square representing an LED
PIXEL_RADIUS_RATIO = 0.5 # Relative diameter of each LED
FPS_2COLOR = 60
FPS_8COLOR = 20
GREEN_BRIGHTNESS = 180 # Brightness (0-255) of the brightest green

class PharmaScreen():
    def __init__(self, color_scale=True, server_ip=None):
        '''
            An object representing the pharmacy cross screen for local simulation and remote control of the actual cross.
            Args:
                - `color_scale` enables up to 8 shades of green to be displayed, but reduces the expected framerate from 60 to 20FPS.
                - `server_ip` is the address of the controller where update packets should be transmitted. If None, the screen is only simulated locally.
        '''
        self.server_ip = server_ip
        self.color_scale = color_scale
        self.local_screen = pygame.display.set_mode([PIXEL_SIZE * SCREEN_SIZE, PIXEL_SIZE * SCREEN_SIZE])
        self.pixel_buffer = [[0. for c in range(SCREEN_SIZE)] for r in range(SCREEN_SIZE)]
        self.clock = pygame.time.Clock()
        self.fps = FPS_8COLOR if color_scale else FPS_2COLOR
        self.font = pygame.font.SysFont(None, 24)

    def is_drawable(self, row, col):
        '''
            Returns whether the given coordinates match an actual LED on the screen.
        '''
        if not (0 <= row < SCREEN_SIZE and 0 <= col < SCREEN_SIZE):
            return False

        panel_coords = (row//PANEL_SIZE, col//PANEL_SIZE) # Locate the target on the 3x3 grid of panels
        return panel_coords in ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1))
        
    def set_image(self, image):
        '''
            Sets the image to be displayed.
            
            The `image` argument should be an array of floats representing the pixels in (row, column) order.
            Values range from 0.0 (off) to 1.0 (brightest).
            Note that 4 sections of the image will be ignored as the screen is a cross.
        '''
        if len(image) != SCREEN_SIZE or any(len(row)!=SCREEN_SIZE for row in image):
            raise ValueError(f'Invalid image size (expected {SCREEN_SIZE}x{SCREEN_SIZE})')

        self.local_screen.fill((0, 0, 0))
        for r,c in itertools.product(range(SCREEN_SIZE), repeat=2):
            if not 0.0 <= image[r][c] <= 1.0:
                raise ValueError('Pixel values should be between 0.0 and 1.0')
            
            if self.is_drawable(r, c):
                quantizer = 7 if self.color_scale else 1
                quantized_color = round(image[r][c] * quantizer) / quantizer
                    
                led_color = (30, 30 + GREEN_BRIGHTNESS * quantized_color, 30)
                center = (PIXEL_SIZE * (c + 0.5), PIXEL_SIZE * (r + 0.5))
                pygame.draw.circle(self.local_screen, led_color, center, PIXEL_SIZE * PIXEL_RADIUS_RATIO / 2)
        
        if self.server_ip is not None:
            # Send the image to the controller
            raise NotImplementedError('Remote control is not yet implemented')
        
        current_fps = self.clock.get_fps()
        fps_img = self.font.render(f'FPS: {current_fps:.1f}', True, (0, 100, 0))
        self.local_screen.blit(fps_img, (0, 0))
        pygame.display.flip()
        self.frame_timing = self.clock.tick(self.fps)