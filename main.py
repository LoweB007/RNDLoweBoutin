import pygame as pg
from screeninfo import get_monitors
from button import Button
from input_field import Input_Field
import sqlite3
from evolution_main import Game


class Top:
    def __init__(self):
        pg.init()
        self.monik = get_monitors()[0]
        self.size = (self.monik.width, self.monik.height)
        self.screen = pg.display.set_mode(self.size)
        self.run = True
        self.ret_but = Button(self.size[0] // 4.8, self.size[1] // 18, (255, 255, 255), (23, 204, 58))
        connect = sqlite3.connect('top.db')
        cursor = connect.cursor()
        self.result = cursor.execute("""SELECT name, points FROM states
        ORDER BY points""").fetchall()[::-1][:10]

    def draw_top(self, x, y):
        font_color = (255, 255, 255)
        font_type = pg.font.SysFont('arial', 50)
        text = font_type.render('TOP 10 PLAYER:', True, font_color)
        self.screen.blit(text, (x, y))

    def draw(self, x, y, mes):
        font_color = (255, 255, 255)
        font_type = pg.font.SysFont('arial', 50)
        text = font_type.render(mes, True, font_color)
        self.screen.blit(text, (x, y))

    def start(self):
        self.run = True
        while self.run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.run = False
            self.draw_top(self.size[0] // 2.7, self.size[1] // 15.4)
            self.ret_but.draw(self.screen, self.size[0] // 2.7, self.size[1] // 1.2, 'В главное меню', self.stop)
            for i in range(len(self.result)):
                name, points = self.result[i]
                mes = '   '.join([name, str(points)])
                self.draw(self.size[0] // 2.7, self.size[1] // 7.2 + i * self.size[1] // 15.4, mes)

            pg.display.flip()

    def stop(self):
        self.run = False
        st = Start()
        st.start()


class Start:
    def __init__(self):
        pg.init()
        self.monik = get_monitors()[0]
        self.size = (self.monik.width, self.monik.height)
        self.screen = pg.display.set_mode(size=self.size)
        self.logo = pg.image.load('logo.jpg')
        self.logo = pg.transform.scale(self.logo, self.size)
        self.logo_rect = self.logo.get_rect(
            bottomright=self.size)
        self.screen.blit(self.logo, self.logo_rect)

        self.start_button = Button(self.size[0] // 4.8, self.size[1] // 18, (222, 82, 92), (23, 204, 58))
        self.tabl_button = Button(self.size[0] // 4.8, self.size[1] // 18, (24, 86, 140), (23, 204, 58))
        self.exit_button = Button(self.size[0] // 4.8, self.size[1] // 18, (174, 13, 73), (23, 204, 58))
        self.input_player_1 = Input_Field(self.size[0] // 4.8, self.size[1] // 18, 'Player1')
        self.input_player_2 = Input_Field(self.size[0] // 4.8, self.size[1] // 18, 'Player2')
        self.ret_button = Button(self.size[0] // 4.8, self.size[1] // 18, (222, 82, 92), (23, 204, 58))
        self.run = True

    def ex(self):
        self.run = False

    def top(self):
        self.run = False
        top = Top()
        top.start()

    def new_game(self):
        self.run = False
        new = Game()
        name_player_1 = self.input_player_1.input_text
        name_player_2 = self.input_player_2.input_text
        score_1, score_2 = new.get_score()
        connect = sqlite3.connect('top.db')
        cursor = connect.cursor()
        result = cursor.execute("""SELECT name FROM states""").fetchall()
        if name_player_1 not in result:
            cursor.execute(f"""INSERT INTO states(points, name) VALUES({score_1}, '{name_player_1}')""")
            connect.commit()
        else:
            cursor.execute(f"""UPDATE states
SET points = {score_1}
WHERE name = '{name_player_1}'""")
            connect.commit()
        if name_player_2 not in result:
            cursor.execute(f"""INSERT INTO states(points, name) VALUES({score_2}, '{name_player_2}')""")
            connect.commit()
        else:
            cursor.execute(f"""UPDATE states
        SET points = {score_2}
        WHERE name = '{name_player_2}'""")
            connect.commit()
        cursor.execute(
            f"""INSERT INTO games(name_1, name_2, score_1, score_2) VALUES('{name_player_1}', '{name_player_2}', {score_1}, {score_2})""")
        connect.commit()
        top = Top()
        top.start()

    def start(self):
        self.run = True
        while self.run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.run = False
            self.start_button.draw(self.screen, self.size[0] // 2.5, self.size[1] // 2.9 + self.size[1] // 5.4,
                                   'Начать игру', self.new_game)
            self.tabl_button.draw(self.screen, self.size[0] // 2.5, self.size[1] // 2.9 + self.size[1] // 3.6,
                                  'Таблица лидеров', self.top)
            self.exit_button.draw(self.screen, self.size[0] // 2.5, self.size[1] // 2.9 + self.size[1] // 2.7, 'Выйти',
                                  self.ex)
            self.input_player_1.draw(self.screen, self.size[0] // 2.5, self.size[1] // 2.9)
            self.input_player_2.draw(self.screen, self.size[0] // 2.5, self.size[1] // 2.9 + self.size[1] // 10.8)
            pg.display.flip()
        pg.quit()


if __name__ == '__main__':
    st = Start()
    st.start()
