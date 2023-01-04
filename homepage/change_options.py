import pygame

from core.screen_operation import terminate
from settings import HEIGHT, WIDTH


def draw_buttons_for_settings(screen, font, text_y, parent_text):
    text_y = text_y - parent_text.get_height() // 2
    for i in range(1, 11):
        text = font.render(f'{i}', True, (100, 255, 100))
        text_x = WIDTH // 10 * i // 1.4 + 5 + parent_text.get_width()
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (text_x - 10, text_y - 10, text_w + 20, text_h + 20),
            1
        )


class Settings:
    def __init__(self, screen, user):
        self.user = user
        self.screen = screen

    def start_screen(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)

        title_text = font.render('Настройки', True, (220, 20, 60))
        title_x = WIDTH // 2 - title_text.get_width() // 2
        title_y = HEIGHT // 10 - title_text.get_height() // 10
        screen.blit(title_text, (title_x, title_y))

        music_text = font.render('Музыка', True, (220, 20, 60))
        music_x = 10
        music_y = HEIGHT // 2.5 - music_text.get_height() // 2
        screen.blit(music_text, (music_x, music_y))

        draw_buttons_for_settings(screen, font, HEIGHT // 2.5, music_text)

        sound_text = font.render('Звуки', True, (220, 20, 60))
        sound_x = 15
        sound_y = HEIGHT // 1.5 - sound_text.get_height() // 2
        screen.blit(sound_text, (sound_x, sound_y))

        draw_buttons_for_settings(screen, font, HEIGHT // 1.5, music_text)

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
                    print('grisha loh')


def settings():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screensaver = Settings(screen, 123)
    screensaver.start_screen(screen)
