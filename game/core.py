import pygame

from core.load_file import load_image


class Finish(pygame.sprite.Sprite):
    image = load_image('game/other/finish.jpg')

    def __init__(self):
        super(Finish, self).__init__()
        self.image = Finish.image
        self.rect = self.image.get_rect()
        self.rect.x = 208
        self.rect.y = -100
        self.mask = pygame.mask.from_surface(self.image)


class Coin(pygame.sprite.Sprite):
    image = load_image('game/other/coin.png')

    def __init__(self, x):
        super(Coin, self).__init__()
        self.image = Coin.image
        self.rect = self.image.get_rect()
        self.rect.x = [262, 437, 632, 835][x] + 70
        self.rect.y = -70
        self.mask = pygame.mask.from_surface(self.image)


class Barrier(pygame.sprite.Sprite):
    image = load_image('game/barriers/1.png')

    def __init__(self, x):
        super(Barrier, self).__init__()
        self.image = Barrier.image
        self.rect = self.image.get_rect()
        self.rect.x = [262, 437, 632, 835][x] + 70
        self.rect.y = -70
        self.mask = pygame.mask.from_surface(self.image)
