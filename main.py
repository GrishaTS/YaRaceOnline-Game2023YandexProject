import pygame

from homepage.change_options import draw_settings
from settings import SIZE

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    draw_settings(screen)
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
