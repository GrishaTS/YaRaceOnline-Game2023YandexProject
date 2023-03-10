import os
import sys

import pygame


def load_image(name):
    fullname = os.path.join('images/', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением "{fullname}" не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image
