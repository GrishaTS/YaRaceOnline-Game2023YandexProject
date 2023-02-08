import pygame

from core.audio import sounds
from core.buttons import Button
from core.load_file import load_image
from core.screen_operation import terminate
from game.race import race
from game.single_race import race as single_race
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
        'button_road': race,
        'button_single_road': single_race,
    }

    def __init__(self, screen, user, music):
        self.music = music
        self.user = user
        self.screen = screen
        self.button_settings = Button(1200, 20, 'screensaver/settings.png')
        self.button_garage = Button(20, 80, 'screensaver/garage.png')
        self.button_road = Button(20, 20, 'screensaver/road.png')
        self.button_single_road = Button(20, 140, 'screensaver/road.png')
        for i in sounds:
            sounds[i].set_volume(user.selected_sounds / 10)
        pygame.mixer.music.set_volume(user.selected_music / 10)

    def start_screen(self):
        if self.music:
            pygame.mixer.music.load(
                f'audio/music/{self.user.selected_car}.ogg'
            )
            pygame.mixer.music.play(-1)
        pointing_b = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                ):
                    self.push_button(event)
                elif event.type == pygame.MOUSEMOTION:
                    pointing_b = self.pointing_button(event)
            fon = pygame.transform.scale(
                IMAGES['screensaver'],
                (WIDTH, HEIGHT),
            )
            self.screen.blit(fon, (0, 0))
            for button in self.__dict__:
                if button.startswith('button'):
                    btn = self.__dict__[button]
                    if button == pointing_b:
                        btn_img = pygame.transform.scale(
                            btn.pointing_image,
                            (btn.image_x, btn.image_y),
                        )
                    else:
                        btn_img = pygame.transform.scale(
                            btn.image,
                            (btn.image_x, btn.image_y),
                        )
                    self.screen.blit(btn_img, (btn.x, btn.y))
            pygame.display.flip()

    def push_button(self, event):
        for button in self.__dict__:
            if button.startswith('button'):
                if self.__dict__[button].is_button_down(event.pos):
                    self.btn_func[button](self.user)

    def pointing_button(self, event):
        for button in self.__dict__:
            if button.startswith('button'):
                if self.__dict__[button].is_button_down(event.pos):
                    return button


def homepage(user, music=True):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screensaver = Manager(screen, user, music)
    screensaver.start_screen()
