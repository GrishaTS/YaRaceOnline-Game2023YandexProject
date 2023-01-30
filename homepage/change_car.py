import pygame

from core.buttons import Button
from core.load_file import load_image
from core.screen_operation import terminate
from settings import HEIGHT, WIDTH

IMAGES = {
    'backgroung': load_image('garage/background.jpg'),
}


class Garage:

    def __init__(self, screen, user):
        self.user = user
        self.screen = screen
        self.button_car1 = Button(57, 200, 'garage/side_view/1.png')
        self.button_car2 = Button(465, 200, 'garage/side_view/2.png')
        self.button_car3 = Button(873, 150, 'garage/side_view/3.png')
        self.button_car4 = Button(57, 500, 'garage/side_view/4.png')
        self.button_car5 = Button(465, 570, 'garage/side_view/5.png')
        self.button_car6 = Button(873, 520, 'garage/side_view/6.png')

    def start_screen(self):
        font = pygame.font.Font(None, 50)
        text = font.render("Selected", True, '#54bd42')
        text_w = text.get_width()
        text_h = text.get_height()
        active_car = 2
        while True:
            for event in pygame.event.get():
                new_car = 0
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    new_car = self.push_button(event)
                if new_car:
                    active_car = new_car
            car = self.__dict__[f'button_car{active_car}']
            x = car.x + car.image_x / 2 - 50
            y = car.y - 40
            fon = pygame.transform.scale(IMAGES['backgroung'], (WIDTH, HEIGHT))
            self.screen.blit(fon, (0, 0))
            self.screen.blit(text, (x, y))
            pygame.draw.rect(
                self.screen,
                '#54bd42',
                (x - 10, y - 10, text_w + 20, text_h + 20),
                1,
            )
            for button in self.__dict__:
                if button.startswith('button'):
                    btn = self.__dict__[button]
                    btn_img = pygame.transform.scale(
                        btn.image,
                        (btn.image_x, btn.image_y),
                    )
                    self.screen.blit(btn_img, (btn.x, btn.y))
                    
                    btn_unlocked = pygame.transform.scale(
                        load_image('garage/lock.png'),
                        (100, 100),
                    )
                    self.screen.blit(
                        btn_unlocked,
                        (
                            btn.x + btn.image_x / 2,
                            btn.y + btn.image_y / 2 - 50,
                        ),
                    )

                    money = __import__('random').randrange(1000, 5000)
                    text_m = font.render(f'{money}$', True, '#54bd42')
                    x = btn.x + car.image_x / 2
                    y = btn.y + 100
                    self.screen.blit(
                        text_m,
                        (
                            btn.x + btn.image_x / 2,
                            btn.y + btn.image_y / 2 + 20,
                        ),
                    )

            pygame.display.flip()

    def push_button(self, event):
        for button in self.__dict__:
            if button.startswith('button'):
                if self.__dict__[button].is_button_down(event.pos):
                    return self.choice_car(button[-1])

    def choice_car(self, id):
        print(id)
        return id


def choosing_car():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    garage = Garage(screen, 123)
    garage.start_screen()
