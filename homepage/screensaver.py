import pygame

from core.buttons import Button
from core.load_file import load_image
from core.screen_operation import terminate
from homepage.change_car import choosing_car
from homepage.change_options import settings
from settings import HEIGHT, WIDTH

IMAGES = {
    'screensaver': load_image('screensaver/screensaver.jpg'),
}


class Manager:
    btn_func = {
        'button_settings': settings,
        'button_garage': choosing_car,
    }

    def __init__(self, screen, user):
        self.user = user
        self.screen = screen
        self.button_settings = Button(1200, 20, 'screensaver/settings.png')
        self.button_garage = Button(20, 80, 'screensaver/garage.png')

    def start_screen(self):
        fon = pygame.transform.scale(IMAGES['screensaver'], (WIDTH, HEIGHT))
        self.screen.blit(fon, (0, 0))
        for button in self.__dict__:
            if button.startswith('button'):
                btn = self.__dict__[button]
                btn_img = pygame.transform.scale(
                    btn.image,
                    (btn.image_x, btn.image_y),
                )
                self.screen.blit(btn_img, (btn.x, btn.y))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.push_button(event)
            pygame.display.flip()

    def push_button(self, event):
        for button in self.__dict__:
            if button.startswith('button'):
                if self.__dict__[button].is_button_down(event.pos):
                    self.btn_func[button]()


def homepage():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screensaver = Manager(screen, 123)
    screensaver.start_screen()
