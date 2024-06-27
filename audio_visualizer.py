import sys
import numpy as np
import pygame
from pydub import AudioSegment
from pydub.utils import which
from pharmacontroller import SCREEN_SIZE, PharmaScreen

# Configure pydub to use ffmpeg
AudioSegment.converter = which("ffmpeg")

# Function to load audio data
def get_audio_data(file_path):
    audio = AudioSegment.from_file(file_path)
    samples = np.array(audio.get_array_of_samples())
    return samples, audio.frame_rate

# Function to compute amplitude spectrum using FFT
def get_amplitude_spectrum(data):
    fft_result = np.fft.fft(data)
    amplitude_spectrum = np.abs(fft_result)
    return amplitude_spectrum[:len(amplitude_spectrum)//2]

# Function to draw techno sign as a wave based on amplitude spectrum
def draw_techno_sign(screen, spectrum):
    image = [[0.0 for _ in range(SCREEN_SIZE)] for _ in range(SCREEN_SIZE)]
    
    max_amplitude = np.max(spectrum)
    num_bins = len(spectrum)
    num_points = SCREEN_SIZE * 2  # Increase the number of points for wider shape
    
    point_width = max(1, num_bins // num_points)

    spectrum /= max_amplitude
    
    for point in range(num_points):
        start_idx = point * point_width
        end_idx = min(start_idx + point_width, num_bins)
        mean_amplitude = np.mean(spectrum[start_idx:end_idx])
        
        wave_height = int(mean_amplitude * SCREEN_SIZE / 3)  # Adjust amplitude to fit screen

        for y_offset in range(-wave_height, wave_height):
            y = SCREEN_SIZE // 2 + y_offset
            x = point
            if 0 <= y < SCREEN_SIZE and 0 <= x < SCREEN_SIZE:
                image[y][x] = 1.0

    screen.set_image(image)

# Main function
if __name__ == "__main__":
    pygame.init()
    screen = PharmaScreen()

    pygame.mixer.init()

    file_path = "music.mp3"  # Replace with your audio file path
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    audio_data, sample_rate = get_audio_data(file_path)

    chunk_size = 1024
    start = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if start + chunk_size < len(audio_data):
            chunk = audio_data[start:start + chunk_size]
            amplitude_spectrum = get_amplitude_spectrum(chunk)
            draw_techno_sign(screen, amplitude_spectrum)
            start += chunk_size
        else:
            running = False

        pygame.time.wait(30)
        pygame.display.flip()

    pygame.quit()
