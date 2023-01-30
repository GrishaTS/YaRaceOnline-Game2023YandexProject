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
            f'SELECT garage_id FROM user_garage WHERE user_id = {user_id}'  # user.id
        ))
        print(self.locked)

    def buy(self):
        global user_coins
        user_coins -= self.price
        self.locked = True
        print(f'INSERT INTO user_garage (user_id, garage_id) VALUES ({user_id}, {self.id});')
        db_connect = sqlite3.connect('db.sqlite3')
        db_connect.execute(
            f'INSERT INTO user_garage (user_id, garage_id) VALUES ({user_id}, {self.id});'  # user.id
        )
        db_connect.commit()


class Garage:
    def __init__(self, screen, user):
        self.user = user
        self.screen = screen
        for car in sqlite3.connect(
            'db.sqlite3'
        ).execute('SELECT * FROM garage'):
            print(*car)
            self.__dict__[f'car{car[0]}'] = Car(*car, user_id)

    def start_screen(self):
        font_s = pygame.font.Font(None, 50)
        text_s = font_s.render('Selected', True, '#54bd42')
        text_w_s = text_s.get_width()
        text_h_s = text_s.get_height()
        active_car = 1  # self.user.active_car = 2
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    active_car = self.push_button(event, active_car)
            car = self.__dict__[f'car{active_car}']
            x_selected = car.btn.x + car.btn.image_x / 2 - 50
            y_selected = car.btn.y - 40
            fon = pygame.transform.scale(IMAGES['backgroung'], (WIDTH, HEIGHT))
            self.screen.blit(fon, (0, 0))
            self.screen.blit(text_s, (x_selected, y_selected))

            text_c = font_s.render(f'{user_coins}$', True, '#54bd42')
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
                    text_w_c - 45,
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
                                btn.x + btn.image_x / 2 + 10,
                                btn.y + btn.image_y / 2 + 20,
                            ),
                        )

            pygame.display.flip()

    def push_button(self, event, active_car):
        for car in self.__dict__:
            if car.startswith('car'):
                if self.__dict__[car].btn.is_button_down(event.pos):
                    return self.choice_car(self.__dict__[car], active_car)
        return active_car

    def choice_car(self, car, active_car):
        if (car.id,) in list(
            sqlite3.connect('db.sqlite3').execute(
                f'SELECT garage_id FROM user_garage WHERE user_id = {user_id}'
            )
        ):
            # self.user.active_car = id
            return car.id
        else:
            if user_coins >= car.price:
                car.buy()
                return car.id
            return active_car


def choosing_car():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    garage = Garage(screen, 123)
    garage.start_screen()
