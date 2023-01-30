import pygame as pg


class Input_Field:
    def __init__(self, width, height, input_text):
        self.width = width
        self.height = height
        self.input_text = input_text
        self.need_input = False

    def draw(self, display, x, y):
        input_rect = pg.Rect(x, y, self.width, self.height)
        pg.draw.rect(display, (255, 255, 255), input_rect)
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]
        if input_rect.collidepoint(mouse[0], mouse[1]) and click:
            self.need_input = True
            self.input_text = ''
        if self.need_input:
            for event in pg.event.get():
                if self.need_input and event.type == pg.KEYDOWN and input_rect.collidepoint(mouse[0], mouse[1]):
                    if event.key == pg.K_RETURN:
                        self.need_input = False
                        self.input_text = 'Player1'
                    elif event.key == pg.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode
        font_color = (0, 0, 0)
        font_type = pg.font.SysFont('arial', 30)
        text = font_type.render(self.input_text, True, font_color)
        display.blit(text, (x + self.width // 40, y + self.height // 6))

    def get_text(self):
        return self.input_text
