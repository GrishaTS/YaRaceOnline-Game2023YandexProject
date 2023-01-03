import os
import sys

import pygame

from core.constants import HEIGHT, WIDTH
from core.screen_operation import terminate


class Screensaver:
    def __init__(self, screen, user):
        self.user = user
        self.screen = screen

    def settings(self):
        ...

    def start_screen(self):
        fon = pygame.transform.scale(images['screensaver'], (WIDTH, HEIGHT))
        self.screen.blit(fon, (0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    ...
            pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screensaver = Screensaver(screen, 123)
    screensaver.start_screen()


def load_image(name):
    fullname = os.path.join('data/screensaver/', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


images = {
    'screensaver': load_image('screensaver.jpg'),
}


main()
