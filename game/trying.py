import os
import sys

import pygame

SIZE = WIDTH, HEIGHT = 1280, 720

user_id = 4
user_coins = 300


def load_image(name):
    fullname = os.path.join('images/', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением "{fullname}" не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Car:
    def __init__(self, x, y, file):
        self.x = x
        self.y = y
        self.max_velocity = 10
        self.velocity = 3
        self.angle = 0
        self.base_image = load_image(file)
        self.image = load_image(file)

    def move_angle(self):
        self.image = pygame.transform.rotate(self.base_image, self.angle)

    def move(self, key):
        if key in 'aф':
            self.x -= 20
            if self.angle < 20:
                self.angle += 2
        elif key in 'dв':
            self.x += 20
            if self.angle > -20:
                self.angle -= 2
        else:
            if key in 'wц':
                if self.velocity + 1 < self.max_velocity:
                    self.velocity += 1
            elif key in 'sы':
                if self.velocity - 1 > 0:
                    self.velocity -= 1
        self.move_angle()


class Game:
    def __init__(self, screen, user):
        self.screen = screen
        self.car = Car(300, 50, 'garage/top_view/4.png')

    def start_screen(self):
        flag = False
        bg_photo = load_image('game/road_example.jpg')
        bg_y = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type in [pygame.KEYDOWN, pygame.TEXTINPUT]:
                    flag = False
                    key = (
                        event.__dict__.get('unicode') if
                        event.__dict__.get('unicode') else
                        event.__dict__.get('text')
                    )
                    if key in 'фцвыawds':
                        self.car.move(key)
                elif event.type == pygame.KEYUP:
                    flag = True
            if flag:
                if self.car.angle > 0:
                    self.car.angle -= 1
                elif self.car.angle < 0:
                    self.car.angle += 1
                self.car.move_angle()
            self.screen.fill('black')
            bg_y += self.car.velocity
            self.screen.blit(bg_photo, (0, bg_y))
            self.screen.blit(bg_photo, (0, bg_y - 720))
            if bg_y >= 719:
                bg_y = 0
            btn_img = pygame.transform.scale(
                self.car.image,
                tuple(i // 5 for i in self.car.image.get_size()),
            )
            self.screen.blit(btn_img, (self.car.x, 450))
            pygame.display.flip()


def choosing_car(user):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(screen, user)
    game.start_screen()


choosing_car(1)
