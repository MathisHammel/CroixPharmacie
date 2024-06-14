import cv2
import pygame
import sys
import tempfile

from pharmacontroller import PharmaScreen, SCREEN_SIZE

VIDEO_FILE = 'videoExample.mp4'
FORCED_FRAMERATE = None
INVERT_COLORS = False
PLAY_AUDIO = True

def frame_to_image(frame, invert_colors=False):
    '''
        Converts a frame from a video file to a 2D array of floats representing the pixel values.
        This assumes that the video is in landscape mode.
    '''
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Scale the image to fit SCREEN_SIZE in height
    height, width = grayscale_frame.shape
    scaled_width = int(width * SCREEN_SIZE / height)
    scaled_frame = cv2.resize(grayscale_frame, (scaled_width, SCREEN_SIZE))

    # Crop the image to SCREEN_SIZE in width
    start_col = (scaled_width - SCREEN_SIZE) // 2
    cropped_frame = scaled_frame[:, start_col:start_col + SCREEN_SIZE]

    # Normalize the pixel values to the [0.0, 1.0] range and (row, column) order
    normalized_frame = cropped_frame / 255.0

    if invert_colors:
        normalized_frame = 1.0 - normalized_frame

    return normalized_frame

if __name__ == '__main__':
    cap = cv2.VideoCapture(VIDEO_FILE)
    if not cap.isOpened():
        print(f'Error: cannot open video file {VIDEO_FILE}')
        sys.exit()

    if PLAY_AUDIO:
        from moviepy.editor import VideoFileClip
        vclip = VideoFileClip(VIDEO_FILE)
        vclip.audio.write_audiofile('temp_audio.mp3')

    pygame.init()
    screen = PharmaScreen()

    if PLAY_AUDIO:
        pygame.mixer.music.load('temp_audio.mp3')
        pygame.mixer.music.play()

    if FORCED_FRAMERATE is not None:
        fps = FORCED_FRAMERATE
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)

    ms_per_frame = 1000 / fps

    print(f'Playing video at {fps} FPS (frame duration: {ms_per_frame} ms)')

    running = True
    frame_counter = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        curr_time = pygame.time.get_ticks()

        if frame_counter == 0 and PLAY_AUDIO:
            # Reset music to sync with the video
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(curr_time / 1000)

        frame_ctr_before = frame_counter
        while frame_counter * ms_per_frame < curr_time:
            # Read frames until synchronized with the current time
            ret, frame = cap.read()
            frame_counter += 1
            if not ret:
                print('End of video file')
                pygame.quit()
                sys.exit()

        if frame_counter != frame_ctr_before + 1:
            print(f'Frame desync: {frame_ctr_before} -> {frame_counter}')

        image = frame_to_image(frame, invert_colors=INVERT_COLORS)
        screen.set_image(image)

pygame.quit()
