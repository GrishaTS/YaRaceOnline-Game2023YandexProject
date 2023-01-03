from core.load_file import load_image


class Button:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = load_image(image)
        self.image_x, self.image_y = self.image.get_size()

    def is_button_down(self, pos):
        return (
            self.x < pos[0] < self.x + self.image_x and
            self.y < pos[1] < self.y + self.image_y
        )
