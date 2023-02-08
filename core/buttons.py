import os


from core.load_file import load_image
print(os.getcwd())

class Button:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = load_image(image)
        if not os.path.exists(
                f'images/{image.split("/")[0]}/'
                f'{image.split("/")[1].split(".")[0]}_pointing.png'
        ):
            from PIL import Image, ImageEnhance
            im = Image.open(f'images/{image}')
            enhancer = ImageEnhance.Contrast(im)
            factor = 0.2
            im_output = enhancer.enhance(factor)
            im_output.save(f'images/{image.split("/")[0]}/{image.split("/")[1].split(".")[0]}_pointing.png')
        self.pointing_image = load_image(
            f'{image.split("/")[0]}/'
            f'{image.split("/")[1].split(".")[0]}_pointing.png'
        )
        self.image_x, self.image_y = self.image.get_size()

    def is_button_down(self, pos):
        return (
            self.x < pos[0] < self.x + self.image_x and
            self.y < pos[1] < self.y + self.image_y
        )
