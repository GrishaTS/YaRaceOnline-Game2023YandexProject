import pygame

from core.buttons import Button
from core.screen_operation import terminate
from settings import HEIGHT, WIDTH


def draw_buttons_for_settings(self, name, text_y, parent_text):
    text_y = text_y - parent_text.get_height() // 2
    for i in range(1, 11):
        text_x = WIDTH // 10 * i // 1.4 + 5 + parent_text.get_width()
        setattr(self, f'button_{name}{i}', Button(text_x - 10, text_y - 10, f'numbers/{i}.png'))


class Settings:
    def __init__(self, screen, user):
        self.user = user
        self.screen = screen

    def start_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)

        title_text = font.render('Настройки', True, (220, 20, 60))
        title_x = WIDTH // 2 - title_text.get_width() // 2
        title_y = HEIGHT // 10 - title_text.get_height() // 10
        self.screen.blit(title_text, (title_x, title_y))

        music_text = font.render('Музыка', True, (220, 20, 60))
        music_x = 10
        music_y = HEIGHT // 2.5 - music_text.get_height() // 2
        self.screen.blit(music_text, (music_x, music_y))
        draw_buttons_for_settings(self, 'music', HEIGHT // 2.5, music_text)

        sound_text = font.render('Звуки', True, (220, 20, 60))
        sound_x = 15
        sound_y = HEIGHT // 1.5 - sound_text.get_height() // 2
        self.screen.blit(sound_text, (sound_x, sound_y))

        draw_buttons_for_settings(self, 'sound', HEIGHT // 1.5, music_text)
        self.button_home = Button(20, 20, 'garage/home.png')
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
        from homepage.screensaver import homepage

        for button in self.__dict__:
            if button.startswith('button'):
                if self.__dict__[button].is_button_down(event.pos):
                    if button == 'button_home':
                        homepage(self.user)

    def pointing_button(self, event):
        for button in self.__dict__:
            if button.startswith('button'):
                if self.__dict__[button].is_button_down(event.pos):
                    return button


def settings(user):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screensaver = Settings(screen, user)
    screensaver.start_screen()
