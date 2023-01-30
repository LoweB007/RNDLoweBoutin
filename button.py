import pygame as pg
from screeninfo import get_monitors

monik = get_monitors()[0]
size = (monik.width, monik.height)


class Button:
    def __init__(self, width, height, inactive_color, active_color):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.activ_color = active_color

    def draw(self, display, x, y, text, active=None):
        x_mouse, y_mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]
        font_color = (0, 0, 0)
        font_type = pg.font.SysFont('arial', 30)
        text = font_type.render(text, True, font_color)
        if x < x_mouse < x + self.width:
            if y < y_mouse < y + self.height:
                pg.draw.rect(display, self.activ_color, (x, y, self.width, self.height))
                if click:
                    if active is not None:
                        active()

        else:
            pg.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))
        display.blit(text, (x + self.width // 40, y + self.height // 6))






