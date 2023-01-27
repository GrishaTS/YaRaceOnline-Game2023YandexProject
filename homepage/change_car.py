import pygame

from core.buttons import Button
from core.screen_operation import terminate
from settings import HEIGHT, WIDTH


class Garage:

    def __init__(self, screen, user):
        self.user = user
        self.screen = screen
        self.button_car1 = Button(57, 150, 'garage/side_view/1.png')
        self.button_car2 = Button(465, 150, 'garage/side_view/2.png')
        self.button_car3 = Button(873, 150, 'garage/side_view/3.png')
        self.button_car4 = Button(57, 450, 'garage/side_view/4.png')
        self.button_car5 = Button(465, 450, 'garage/side_view/5.png')
        self.button_car6 = Button(873, 450, 'garage/side_view/6.png')

    def start_screen(self):
        self.screen.fill('grey')
        for button in self.__dict__:
            if button.startswith('button'):
                btn = self.__dict__[button]
                btn_img = pygame.transform.scale(
                    btn.image,
                    (btn.image_x, btn.image_y),
                )
                self.screen.blit(btn_img, (btn.x, btn.y))
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
                    self.choice_car(button[-1])

    def choice_car(self, id):
        print(id)


def choosing_car():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    garage = Garage(screen, 123)
    garage.start_screen()
