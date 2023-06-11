import pygame
import os


def winner_animation(winner=None):
    if winner:
        frame_speed = 0
        images = []

        winner_animation_folder = "winner_screen_4"
        for file_name in os.listdir(winner_animation_folder):
            if file_name.endswith('.png') or file_name.endswith('.jpg'):
                image = pygame.image.load(os.path.join(winner_animation_folder, file_name))
                images.append(image)
        current_image = images[frame_speed]


        if frame_speed <= len(images):
            frame_speed += .3
        if frame_speed >= len(images):
            frame_speed = 0
        current_image = images[int(frame_speed)]


