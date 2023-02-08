import sys
import time

import pygame

from core.audio import sounds
from core.load_file import load_image
from game.core import Barrier, Coin, Finish
from settings import HEIGHT, WIDTH


class Car(pygame.sprite.Sprite):
    def __init__(self, x, file, car_id):
        super(Car, self).__init__()
        self.max_velocity = 30 - (7 - car_id) * 2
        self.velocity = 0
        self.angle = 0
        self.base_image = load_image(file)
        self.image = load_image(file)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, 420)
        self.mask = pygame.mask.from_surface(self.image)

    def move_angle(self):
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, key):
        if key in 'aфAФ':
            self.rect = self.rect.move(-20, 0)
            if self.angle < 30:
                self.angle += 2
        elif key in 'dвDВ':
            self.rect = self.rect.move(20, 0)
            if self.angle > -30:
                self.angle -= 2
        elif key in 'wцЦW':
            if self.velocity + 1 < self.max_velocity:
                self.velocity += 1
        elif key in 'sыЫS':
            if self.velocity - 1 > 1:
                self.velocity -= 1
        self.move_angle()


class Game:
    def __init__(self, screen, user):
        self.screen = screen
        self.finish = []
        self.barriers = []
        self.coins = []
        self.start_coin = user.coins
        self.user = user
        self.car = Car(
            700,
            f'garage/top_view/{user.selected_car}.png',
            user.selected_car,
        )
        self.bg_photo = load_image('game/road_example.jpg')
        self.bg_y = 0
        # self.level = random.randrange(1, 10)
        self.level = 1

    def start_race(self):
        k = 3
        sounds['321'].play()
        while k:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.draw_start(k)
            time.sleep(1)
            k -= 1
        self.car.velocity = 1

    def draw_start(self, k):
        self.screen.fill('black')
        self.screen.blit(self.bg_photo, (0, self.bg_y))
        btn_img = pygame.transform.scale(
            self.car.image,
            self.car.image.get_size(),
        )
        self.screen.blit(
            btn_img,
            (
                (
                    self.car.rect.x -
                    (
                        self.car.image.get_width()
                        - self.car.base_image.get_width()
                    ) // 2
                ),
                420,
            )
        )
        font_s = pygame.font.Font(None, 400)
        text_price = font_s.render(
            f'{k}',
            True,
            'white',
        )
        self.screen.blit(
            text_price,
            (
                WIDTH // 2 - 80,
                HEIGHT // 2 - 70,
            ),
        )
        pygame.display.flip()

    def start_screen(self):
        flag = False
        clock = pygame.time.Clock()
        self.start_race()
        self.start_race_time = time.time()
        self.map_race = open(f'game/levels/{self.level}.txt').read().split()
        self.map_i = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    flag = False
                    key = event.__dict__.get('unicode')
                    if (
                        type(key) is str and
                        key != '' and key in 'фцвыawdsAWDSФЦВЫ'
                    ):
                        for _ in range(2):
                            self.car.move(key)
                            self.draw()
                            clock.tick(50)
                elif event.type == pygame.TEXTINPUT:
                    flag = False
                    key = event.__dict__.get('text')
                    if (
                        type(key) is str and
                        key != '' and key in 'фцвыawdsAWDSФЦВЫ'
                    ):
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
            self.check_crash()
            self.bg_y += self.car.velocity
            if self.bg_y >= 720:
                self.map_i += 1
                self.bg_y = 0
                next_m = list(
                    filter(
                        lambda x: x[0] in ['B', 'C', '-'],
                        zip(list(self.map_race[self.map_i]), range(4))
                    )
                )
                for i in next_m:
                    if i[0] == '-':
                        self.finish.append(Finish())
                        break
                    if i[0] == 'B':
                        self.barriers.append(Barrier(i[1]))
                    if i[0] == 'C':
                        self.coins.append(Coin(i[1]))
            self.draw()
            clock.tick(50)

    def draw(self):
        self.screen.fill('black')
        self.screen.blit(self.bg_photo, (0, self.bg_y))
        self.screen.blit(self.bg_photo, (0, self.bg_y - 720))
        for items in [self.barriers, self.coins, self.finish]:
            to_del = []
            for item in items:
                item.rect.y += self.car.velocity
                if item.rect.y > 730:
                    to_del.append(item)
                self.screen.blit(
                    pygame.transform.scale(
                        item.image,
                        item.image.get_size(),
                    ),
                    (item.rect.x, item.rect.y),
                )
            for i in to_del:
                items.remove(i)
        btn_img = pygame.transform.scale(
            self.car.image,
            self.car.image.get_size(),
        )
        self.screen.blit(
            btn_img,
            (
                (
                    self.car.rect.x -
                    (
                        self.car.image.get_width()
                        - self.car.base_image.get_width()
                    ) // 2
                ),
                420,
            )
        )
        font_s = pygame.font.Font(None, 40)
        text_c = font_s.render(f'{self.user.coins}$', True, '#54bd42')
        text_w_c = text_c.get_width()
        text_h_c = text_c.get_height()
        x_c = 1160
        y_c = 40
        pygame.draw.rect(
            self.screen,
            '#54bd42',
            (
                x_c - 10,
                y_c - 10,
                text_w_c + 20,
                text_h_c + 20,
            ),
            1,
        )
        self.screen.blit(text_c, (x_c, y_c))
        pygame.display.flip()

    def check_crash(self):
        clock = pygame.time.Clock()
        flag = False
        for barrier in self.barriers:
            if pygame.sprite.collide_mask(self.car, barrier):
                flag = True
                del self.barriers[self.barriers.index(barrier)]
        for coin in self.coins:
            if pygame.sprite.collide_mask(self.car, coin):
                del self.coins[self.coins.index(coin)]
                sounds['get coin'].play()
                self.user['coins'] = self.user.coins + 100
        if self.finish:
            if self.finish[0].rect.y > 650:
                from homepage.screensaver import homepage
                self.end_race((time.time() - self.start_race_time) // 1)
                homepage(self.user, music=False)
        if (
            (
                self.car.rect.x -
                (
                    self.car.image.get_width()
                    - self.car.base_image.get_width()
                ) // 2
            ) < 207 or
            (
                self.car.rect.x +
                (
                    self.car.image.get_width() +
                    self.car.base_image.get_width()
                ) // 2 > 1100
            ) or
            flag
        ):
            sounds['crash'].play()
            if not flag:
                self.car.rect.x = 600
            self.car.velocity = 1
            for i in range(20):
                if i % 2:
                    self.car.image.set_alpha(50)
                else:
                    self.car.image.set_alpha(100)
                self.draw()
                clock.tick(50)

    def end_race(self, race_time):
        if self.user.record > race_time:
            self.user.record = race_time
            font_s = pygame.font.Font(None, 100)
            text_c = font_s.render(
                f'Новый рекорд: {round(self.user.record, 2)}с', True, 'red'
            )
            x_c = (WIDTH - text_c.get_width()) / 2
            y_c = 40
            self.screen.blit(text_c, (x_c, y_c))
        font_s = pygame.font.Font(None, 100)
        text_c = font_s.render(
            f'Вы заработали {self.user.coins - self.start_coin}$',
            True,
            'red',
        )
        x_c = (WIDTH - text_c.get_width()) / 2
        y_c = 100
        self.screen.blit(text_c, (x_c, y_c))
        sounds['win'].play()
        pygame.display.flip()
        time.sleep(3)


def race(user):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game(screen, user)
    game.start_screen()
