import random
import sys
import numpy as np
import pygame
from pydub import AudioSegment
from pydub.utils import which
from pharmacontroller import SCREEN_SIZE, PharmaScreen

# Configurer pydub pour utiliser ffmpeg
AudioSegment.converter = which("ffmpeg")

def get_audio_data(file_path):
    # Charger le fichier audio en utilisant pydub
    audio = AudioSegment.from_file(file_path)
    # Convertir l'audio en échantillons de données brutes (tableau numpy)
    samples = np.array(audio.get_array_of_samples())
    return samples, audio.frame_rate

def get_amplitude_spectrum(data):
    # Transformer les données audio en un spectre d'amplitude
    fft_result = np.fft.fft(data)
    amplitude_spectrum = np.abs(fft_result)
    return amplitude_spectrum[:len(amplitude_spectrum)//2]  # Utiliser seulement la première moitié

def draw_waves(screen, spectrum):
    # Créer une image pour afficher le spectre
    image = [[0.0 for _ in range(SCREEN_SIZE)] for _ in range(SCREEN_SIZE)]
    
    max_amplitude = np.max(spectrum)
    for i in range(min(len(spectrum), SCREEN_SIZE)):
        amplitude = spectrum[i] / max_amplitude
        height = int(amplitude * SCREEN_SIZE)
        for j in range(height):
            image[SCREEN_SIZE - 1 - j][i] = 1.0  # Dessiner une barre verticale selon l'amplitude

    screen.set_image(image)

if __name__ == "__main__":
    pygame.init()
    screen = PharmaScreen()

    # Initialiser le mixer de pygame pour jouer la musique
    pygame.mixer.init()

    # Charger et analyser le fichier audio
    file_path = "Rave_Teacher.mp3"

    # Charger le fichier audio avec pygame.mixer pour le jouer
    pygame.mixer.music.load(file_path)

    # Démarrer la lecture de la musique
    pygame.mixer.music.play()

    # Obtenir les échantillons audio pour la visualisation
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
            draw_waves(screen, amplitude_spectrum)
            start += chunk_size
        else:
            running = False  # Arrêter une fois que toute la musique a été traitée

        pygame.time.wait(50)  # Attendre un peu pour synchroniser avec la lecture audio
