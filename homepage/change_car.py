import sqlite3

import pygame

from core.buttons import Button
from core.load_file import load_image
from core.screen_operation import terminate
from settings import HEIGHT, WIDTH

IMAGES = {
    'backgroung': load_image('garage/background.jpg'),
    'btn_unlocked': pygame.transform.scale(
                        load_image('garage/lock.png'),
                        (100, 100),
                    )
}
user_id = 4
user_coins = 300


class Car:
    def __init__(self, car_id, model, path, price, velocity, x, y, user):
        self.btn = Button(x, y, path)
        self.id = car_id
        self.model = model
        self.price = price
        self.velocity = velocity
        self.user = user
        self.locked = (car_id,) in list(sqlite3.connect('db.sqlite3').execute(
            f'SELECT garage_id FROM user_garage WHERE user_id = {self.user.id}'
        ))

    def buy(self):
        self.user['coins'] = self.user.coins - self.price
        self.locked = True
        db_connect = sqlite3.connect('db.sqlite3')
        db_connect.execute(
            f'INSERT INTO user_garage (user_id, garage_id) VALUES '
            f'({self.user.id}, {self.id});'
        )
        db_connect.commit()


class Garage:
    def __init__(self, screen, user):
        self.user = user
        self.screen = screen
        for car in sqlite3.connect(
            'db.sqlite3'
        ).execute('SELECT * FROM garage'):
            self.__dict__[f'car{car[0]}'] = Car(*car, self.user)
        self.button_home = Button(20, 20, 'garage/home.png')

    def start_screen(self):
        font_s = pygame.font.Font(None, 40)
        text_s = font_s.render('Selected', True, '#54bd42')
        text_w_s = text_s.get_width()
        text_h_s = text_s.get_height()
        pointing_b = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                ):
                    new_car = self.push_button(event, self.user.selected_car)
                    if new_car != self.user.selected_car:
                        self.user['selected_car'] = new_car
                        pygame.mixer.music.load(
                            f'audio/music/{self.user.selected_car}.ogg'
                        )
                        pygame.mixer.music.play(-1)
                elif event.type == pygame.MOUSEMOTION:
                    pointing_b = self.pointing_button(event)
            car = self.__dict__[f'car{self.user.selected_car}']
            x_selected = car.btn.x + car.btn.image_x / 2 - 50
            y_selected = car.btn.y - 40
            fon = pygame.transform.scale(IMAGES['backgroung'], (WIDTH, HEIGHT))
            self.screen.blit(fon, (0, 0))
            self.screen.blit(text_s, (x_selected, y_selected))

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

            text_c = font_s.render(f'{self.user.coins}$', True, '#54bd42')
            text_w_c = text_s.get_width()
            text_h_c = text_s.get_height()
            x_c = 1160
            y_c = 40
            pygame.draw.rect(
                self.screen,
                '#54bd42',
                (
                    x_c - 10,
                    y_c - 10,
                    text_w_c - 35,
                    text_h_c + 20,
                ),
                1,
            )
            self.screen.blit(text_c, (x_c, y_c))

            pygame.draw.rect(
                self.screen,
                '#54bd42',
                (
                    x_selected - 10,
                    y_selected - 10,
                    text_w_s + 20,
                    text_h_s + 20,
                ),
                1,
            )
            for car in self.__dict__:
                if car.startswith('car'):
                    btn = self.__dict__[car].btn
                    car = self.__dict__[car]
                    self.screen.blit(
                        pygame.transform.scale(
                            btn.image,
                            (btn.image_x, btn.image_y),
                        ),
                        (btn.x, btn.y),
                    )
                    naming_car = font_s.render(
                        f'{car.model} - {car.velocity}км/ч',
                        True,
                        'black',
                    )
                    self.screen.blit(
                        naming_car,
                        (
                            btn.x + (btn.image_x - naming_car.get_width()) / 2,
                            346 if btn.y <= 200 else 695,
                        ),
                    )
                    if not car.locked:
                        self.screen.blit(
                            IMAGES['btn_unlocked'],
                            (
                                btn.x + btn.image_x / 2,
                                btn.y + btn.image_y / 2 - 50,
                            ),
                        )
                        text_price = font_s.render(
                            f'{car.price}$',
                            True,
                            '#54bd42',
                        )
                        self.screen.blit(
                            text_price,
                            (
                                btn.x + btn.image_x / 2 + 17,
                                btn.y + btn.image_y / 2 + 20,
                            ),
                        )

            pygame.display.flip()

    def push_button(self, event, active_car):
        from homepage.screensaver import homepage
        for btn in self.__dict__:
            if btn.startswith('car'):
                if self.__dict__[btn].btn.is_button_down(event.pos):
                    return self.choice_car(self.__dict__[btn], active_car)
            elif btn.startswith('button'):
                if self.__dict__[btn].is_button_down(event.pos):
                    homepage(self.user, music=False)
        return active_car

    def pointing_button(self, event):
        for button in self.__dict__:
            if button.startswith('button'):
                if self.__dict__[button].is_button_down(event.pos):
                    return button

    def choice_car(self, car, active_car):
        if (car.id,) in list(
            sqlite3.connect('db.sqlite3').execute(
                'SELECT garage_id FROM user_garage WHERE'
                f' user_id = {self.user.id}'
            )
        ):
            return car.id
        else:
            if self.user.coins >= car.price:
                car.buy()
                return car.id
            return active_car


def choosing_car(user):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    garage = Garage(screen, user)
    garage.start_screen()
