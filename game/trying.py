import random
import sys

import pygame

from core.load_file import load_image
from settings import HEIGHT, WIDTH


class Barrier:
    def __init__(self, x, file):
        self.x = x
        self.y = -50
        self.image = load_image(file)


class Car:
    def __init__(self, x, file):
        self.x = x
        self.max_velocity = 30
        self.velocity = 3
        self.angle = 0
        self.base_image = load_image(file)
        self.image = load_image(file)

    def move_angle(self):
        self.image = pygame.transform.rotate(self.base_image, self.angle)

    def move(self, key):
        if key in 'aфAФ':
            self.x -= 20
            if self.angle < 30:
                self.angle += 2
        elif key in 'dвDВ':
            self.x += 20
            if self.angle > -30:
                self.angle -= 2
        elif key in 'wцЦW':
            if self.velocity + 1 < self.max_velocity:
                self.velocity += 3
        elif key in 'sыЫS':
            if self.velocity - 1 > 1:
                self.velocity -= 3
        self.move_angle()


class Game:
    def __init__(self, screen, user):
        self.screen = screen
        self.barriers = []
        self.car = Car(700, 'garage/top_view/5.png')
        self.bg_photo = load_image('game/road_example.jpg')
        self.bg_y = 0

    def start_screen(self):
        flag = False
        clock = pygame.time.Clock()
        while True:
            if random.randrange(1, 101) % 100 == 0:
                self.barriers.append(
                    Barrier(
                        random.randrange(300, 1000),
                        'game/barriers/1.png',
                    ),
                )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    flag = False
                    key = event.__dict__.get('unicode')
                    if type(key) is str and key in 'фцвыawdsAWDSФЦВЫ':
                        for _ in range(2):
                            self.car.move(key)
                            self.draw()
                            clock.tick(50)
                elif event.type == pygame.TEXTINPUT:
                    flag = False
                    key = event.__dict__.get('text')
                    if type(key) is str and key in 'фцвыawdsAWDSФЦВЫ':
                        self.car.move(key)
                elif event.type == pygame.KEYUP:
                    flag = True
            if flag:
                if self.car.angle > 0:
                    self.car.angle -= 4
                    if self.car.angle < 0:
                        self.car.angle = 0
                elif self.car.angle < 0:
                    self.car.angle += 4
                    if self.car.angle > 0:
                        self.car.angle = 0
                self.car.move_angle()
            self.draw()
            clock.tick(50)

    def draw(self):
        self.screen.fill('black')
        self.bg_y += self.car.velocity
        self.screen.blit(self.bg_photo, (0, self.bg_y))
        self.screen.blit(self.bg_photo, (0, self.bg_y - 720))
        to_del = []
        for i in range(len(self.barriers)):
            barrier = self.barriers[i]
            barrier.y += self.car.velocity
            if barrier.y > 720:
                to_del.append(i)
            self.screen.blit(
                pygame.transform.scale(
                    barrier.image,
                    tuple(i // 20 for i in barrier.image.get_size()),
                ),
                (barrier.x, barrier.y),
            )
        for i in to_del:
            del self.barriers[i]
        if self.bg_y >= 719:
            self.bg_y = 0
        btn_img = pygame.transform.scale(
            self.car.image,
            self.car.image.get_size(),
        )
        self.screen.blit(
            btn_img,
            (
                (
                    self.car.x -
                    (
                        self.car.image.get_width()
                        - self.car.base_image.get_width()
                    ) // 2
                ),
                420,
            )
        )
        pygame.display.flip()


def race(user):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(screen, user)
    game.start_screen()
