from deckpy import Deck, Svoystvo, Carnivore, Camouflage, SharpVision, Food
from frontend import choose_obj
import random
import pygame
from random import shuffle, Random
from time import sleep
import csv
from screeninfo import get_monitors
BASENCARDS = 6
for disp in get_monitors():
    if disp.is_primary:
        print(disp)
        W, H = disp.width, disp.height
SW, SH = 90, 120

# In[353]:

# основной класс игры


class Game:
    def __init__(self):
        pygame.init()

        self.display = pygame.display.set_mode((W, H))

        self.screen = self.display.copy()
        self.evo_card = pygame.image.load("evolution.jpg").convert_alpha()
        # загрузка колоды
        self.deck = Deck("deck2.csv")
        # инициализация игрока
        # раздача карт
        self.players = [Player(1),
                        Player(2)]
        self.fat = pygame.sprite.LayeredUpdates()
        self.food_base = pygame.sprite.LayeredUpdates()
        while self.deck:
            try:
                self.players_init()
                print("___________________фаза развития_______________________")
                self.evo_phase_pygame()
                print("___________________фаза кормления_______________________")
                self.eat_phase_pygame()
                print("___________________фаза вымирания_______________________")
                self.dead_phase()
            except TypeError:
                print("___________________подсчет очков_______________________")
                self.score_phase()
                break

    def update_disp(self, act_pl, en_pl, food):
        self.screen.fill((255, 255, 255))
        self.display.blit(self.screen, (0, 0))
        self.display.blit(act_pl.an_add.image, act_pl.an_add.rect)
        for card in act_pl.hand:
            print(card.rect.x)
            card.image = pygame.transform.rotate(card.image, card.angle)
            self.display.blit(card.image, card.rect)
        x = 200
        for card in en_pl.hand:
            self.display.blit(self.evo_card, self.evo_card.get_rect(center=(x + 100, 150)))
            x += W // 16
        food.update([], [])
        food.draw(self.display)

        act_pl.paint_animals(H - 300, False, self.display)
        en_pl.paint_animals(250, True, self.display)

        # squares.draw(display)
        pygame.display.update()
        pygame.display.flip()

    def players_init(self):  # инициализация певого и второго игрока
        for i in self.players:
            i.add_cards_from_deck(self.deck)  # раздача карт первому игроку
            i.an_add = AddAnimalArea() # объявление области добавления животных первого игрока
            for an in i.animals:
                an.food = pygame.sprite.LayeredUpdates()

    def taketurn(self, n):
        sleep(1)
        self.display.fill((255, 255, 255))
        self.display.blit(pygame.image.load("take_turn_img.png").convert_alpha(),
                          pygame.image.load("take_turn_img.png").convert_alpha().get_rect(center=(1000, 500)))
        pygame.display.update()
        pygame.display.flip()
        while True:
            e = pygame.event.wait()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                # изменение текущего игрока
                n *= -1
                print("пробел")
                return n

    def act_choose(self, player):
        player.selected = choose_obj(player.printcard(),
                                     player.hand,
                                     f"0 - пас\nplayer{player.number} введите номер карты:",
                                     True)
        if player.selected != "":  # игрок нажал пас
            action = choose_obj(["1 - выложить как животное",
                                 "2 - выложить как свойство"],
                                [player.add_animal, player.prop_chooses],
                                "введите номер действия:", True)
            if action != "":
                action()
            else:  # игрок нажал пас
                player.notpass = False
        else:
            player.notpass = False

    def is_end_of_phase(self):
        self.playerpasses = []
        for player in self.players:
            if player.notpass and player.hand != []:
                self.playerpasses.append(True)

            else:
                self.playerpasses.append(False)
                player.notpass = False
        return any(self.playerpasses)

    def evo_phase(self):
        for i in self.players:
            i.notpass = True
        raundcard = 1
        while self.is_end_of_phase():
            print(f"***** {raundcard} раунд выкладывания карт")
            for player in self.players:
                if player.notpass:
                    self.act_choose(player)
                raundcard = raundcard + 1

    def card_init(self, pl):
        for x in range(len(pl.hand)):
            pl.hand[x].obj_rect = [pl.hand[x].image.get_rect(center=(x * W // 16 + 200, H - 100)), False, "green", False]
            pl.hand[x].x = x * 100 + 700
            pl.hand[x].y = 800

    def evo_phase_pygame(self):
        self.card_init(self.players[0])
        self.card_init(self.players[1])
        n = 1
        while True:

            act_pl, en_pl = (self.players[1], self.players[0]) if n == -1 else (self.players[0], self.players[1])
            # определение действующего игрока и противника
            squares = []

            # загрузка изображений к картам
            for card in act_pl.hand:
                card.image = pygame.image.load(card.picture).convert_alpha()
                card.rect = card.obj_rect[0]
                squares.append(card)
            self.update_disp(act_pl, en_pl, self.fat)
            e = pygame.event.wait()
            if e.type == pygame.QUIT or e.type == pygame.KEYUP and e.key == 27:
                break
            elif not act_pl.hand and not en_pl.hand:
                break
            if e.type == pygame.MOUSEBUTTONUP and e.button == 3:
                if act_pl.selected:
                    # act_pl.selected.image = pygame.transform.rotate(act_pl.selected.image, 180)
                    self.update_disp(act_pl, en_pl, self.fat)
                    act_pl.selected.angle += 180
                    print(f"карта {act_pl.selected} перевернута {act_pl.selected.angle}")
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                # for x in squares:
                #     x[3] = False
                for square in squares:
                    if square.rect.collidepoint(e.pos):
                        # захват карты-объекта экрана
                        square.dragged = True
                        act_pl.selected = square
                        break
                        # square[3] = True
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                for square in squares:
                    if square.dragged:
                        # при перетягивании задаем ее позицию
                        square.dragged = False
                        square.rect.center = e.pos

                    if square.rect.colliderect(act_pl.an_add):
                        # создается животное
                        act_pl.add_animal()
                        n *= -1
                        self.update_disp(act_pl, en_pl, self.fat)
                        self.taketurn(n)
                        act_pl.selected = ""
                        print("добавлено животное")
                        break
                    for i in act_pl.animals:
                        if square.rect.colliderect(i.rect):
                            # добавляется свойство
                            act_pl.add_property(i, act_pl.selected.svoystva[act_pl.selected.angle % 360 // 180])
                            n *= -1  # изменение текущего игрока
                            self.update_disp(act_pl, en_pl, self.fat)
                            self.taketurn(n)
                            act_pl.selected = ""
                            print("добавлено свойство")
                            break

            elif e.type == pygame.MOUSEMOTION and e.buttons[0]:
                for square in squares:
                    if square.dragged:
                        square.rect.center = e.pos
                # print(e)

    def eat_phase(self):
        self.eat_base = random.randint(1, 6) + 2
        playerpasses = [True, True]
        raundkorm = 1
        while playerpasses[0] or playerpasses[1]:
            print(f"***** {raundkorm} раунд  кормления")
            for playerid in range(2):
                player = self.players[playerid]
                if playerpasses[playerid] and self.eat_base != 0 and player.is_hungry_animals() != []:
                    player.selected = choose_obj(player.printanimals(),
                                                 player.hand,
                                                 f"player{playerid + 1} введите номер животного:")
                    player.feed_animal_red(player.selected, self.eat_base)

                else:
                    playerpasses[playerid] = False
            raundkorm = raundkorm + 1

    def init_food(self):
        self.food_base = pygame.sprite.LayeredUpdates()
        y = H // 3
        x = W - 200
        for i in range(random.randint(2, 8)):
            self.food_base.add(Food(x + random.randint(0, 200), y + random.randint(0, 200), self.food_base, 5))

    def eat_phase_pygame(self):
        self.card_init(self.players[0])
        self.card_init(self.players[1])
        self.init_food()
        n = 1
        while True:

            act_pl, en_pl = (self.players[1], self.players[0]) if n == -1 else (self.players[0], self.players[1])
            # определение действующего игрока и противника
            squares = self.food_base
            # загрузка изображений к картам

            self.update_disp(act_pl, en_pl, self.food_base)
            e = pygame.event.wait()
            if e.type == pygame.QUIT or e.type == pygame.KEYUP and e.key == 27:
                print("конец фазы кормления")
                break
            elif not self.food_base or not (act_pl.is_hungry_animals() or en_pl.is_hungry_animals()):
                print("конец фазы кормления")
                break
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                # for x in squares:
                #     x[3] = False
                for square in squares:
                    if square.rect.collidepoint(e.pos):
                        # захват карты-объекта экрана
                        square.dragged = True
                        act_pl.selected = square
                        break
                        # square[3] = True
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                b = True
                for square in squares:
                    if square.dragged:
                        # при перетягивании задаем ее позицию
                        square.dragged = False
                        square.rect.center = e.pos
                    for i in act_pl.animals:
                        if square.rect.colliderect(i.rect):
                            # добавляется свойство
                            print(type(i))
                            act_pl.feed_animal_red(i, self.food_base, act_pl.selected)
                            n *= -1  # изменение текущего игрока
                            self.update_disp(act_pl, en_pl, self.food_base)
                            act_pl.selected = ""
                            en_pl.selected = ""
                            en_pl.targ = ""
                            act_pl.targ = ""
                            self.taketurn(n)
                            b = False
                            print(f"покормленно животное игрока {act_pl}")
                            break
                if b:
                    for an in act_pl.animals:
                        if an.rect.collidepoint(e.pos):
                            # захват карты-объекта экрана
                            act_pl.targ = an
                            break
                    for an in en_pl.animals:
                        if an.rect.collidepoint(e.pos):
                            # захват карты-объекта экрана
                            en_pl.targ = an
                            break

                    if act_pl.targ and en_pl.targ:
                        if Carnivore in [type(i) for i in act_pl.targ.svoystva_all]:
                            types_list = [type(i) for i in act_pl.targ.svoystva_all]
                            ind = types_list.index(Carnivore)
                            act_pl.targ.svoystva_all[ind].attack(act_pl.targ, act_pl, en_pl.targ, en_pl)
                            self.update_disp(act_pl, en_pl, self.food_base)
                            en_pl.targ = ""
                            act_pl.targ = ""
                            n *= -1
                            self.taketurn(n)
            elif e.type == pygame.MOUSEMOTION and e.buttons[0]:
                for square in squares:
                    if square.dragged:
                        square.rect.center = e.pos

    def dead_phase(self):
        for pl in self.players:
            for animal in pl.animals:
                if len(animal.food) < animal.need_food_count():
                    pl.animals.remove(animal)
        
    def score_phase(self):
        for pl in self.players:
            score = 0
            score += len(pl.animals)
            for i in pl.animals:
                score += len(i.svoystva_all)
            print(score)
        print("Конец игры")


class Animal(pygame.sprite.Sprite):
    def __init__(self, group, layer):
        self.image = pygame.image.load("evolution.jpg").convert_alpha()
        self.rect = self.image.get_rect(center=(600, 500))
        self.svoystva_all = []
        self.isalive = True
        self.food = pygame.sprite.LayeredUpdates()
        self.needfood = 1
        self.angle = 0
        self.svoystva_used_of_turn = []
        self.dragged = False
        self._layer = layer
        self.layer_s = layer
        pygame.sprite.Sprite.__init__(self, group)

    def need_food_count(self):
        self.needfood = 1
        for svoystvo in self.svoystva_all:
            self.needfood = self.needfood+svoystvo.need_food
        return self.needfood


class Player:
    def __init__(self, number):
        self.number = number
        self.hand = []
        self.animals = pygame.sprite.LayeredUpdates()
        self.selected = None
        self.notpass = False
        self.an_add = ""
        self.targ = ""

    def __str__(self):
        return f"{self.number}"
    
    def printanimals(self):
        lst = []
        n = 1
        for i in self.animals:
            lst.append(str(f"животное {n} со свойствами: {', '.join([j.name for j in i.svoystva_all])}"))
            n += 1
        return lst

    def printcard(self):
        # print(f"   карты {self.number} игрока:")
        lst = []
        n = 1
        for i in self.hand:
            lst.append(str(" ".join(i.info()) + " " + str(n)))
            n += 1
        return lst

    def is_hungry_animals(self):
        ans = []
        for an in self.animals:
            if len(an.food) < an.needfood:
                ans.append(an)
        return ans
    
    def add_animal(self):
        card_id = self.hand.index(self.selected)
        lan = self.animals.copy()
        lan.add(Animal(self.animals, 5))
        self.animals = lan
        del self.hand[card_id]
    
    def add_cards_from_deck(self, deck):
        if not self.animals:
            count_animals = BASENCARDS
        else:
            count_animals = len(self.animals) + 2
        for new_card in deck.get_cards(count_animals):
            self.hand.append(new_card)
        print("игроку выданы карты")
        return
    
    def add_property(self, animal, prop_in_card):
        card_id = self.hand.index(self.selected)
        svoysyvo = animal.svoystva_all.copy()
        svoysyvo.append(prop_in_card)
        animal.svoystva_all = svoysyvo
        del self.hand[card_id]
        return
    
    def feed_animal_red(self, animal, feed_base, food):
        if feed_base and animal.need_food_count() > len(animal.food):
            animal.food.add(food)
            print(type(food))
            food.pos_for_an_x = animal.rect.x - food.rect.x
            food.pos_for_an_y = animal.rect.y - food.rect.y
            feed_base.remove(food)
        return feed_base

    def feed_animal_blue(self, animal):
        if animal.need_food_count() > len(animal.food):
            x = animal.rect.x
            y = animal.rect.y
            food = Food(x + random.randint(0, 70), y + random.randint(0, 150), animal.food, 5)
            food.pos_for_an_x = x + random.randint(0, 70)
            food.pos_for_an_y = y + random.randint(0, 150)

    def prop_chooses(self):
        an = choose_obj([self.printanimals()],
                        self.animals,
                        "0 - пас\nвыберите номер животного:", True)
        pr1 = self.selected.svoystva[0].name
        pr2 = self.selected.svoystva[1].name if self.selected.svoystva[1] != "" else ""
        prop_in_card = choose_obj([f"1 - {pr1}",
                                   f"2 - {pr2}"],
                                  self.selected.svoystva,
                                  "0 - пас\nвыберите свойство:", True)
        self.add_property(an, prop_in_card)

    def paint_animals(self, y, is_en, display):
        t = 0
        for an in self.animals:
            x = W // 6 + 40 + 140 * t

            an.rect = an.image.get_rect(center=(x, y))
            if is_en:
                if an.angle != 180:
                    an.image = pygame.transform.rotate(an.image, 180)
                    an.angle += 180
            else:
                if an.angle == 180:
                    an.image = pygame.transform.rotate(an.image, 180)
                    an.angle = 0
            display.blit(an.image, an.rect)

            if an.svoystva_all:
                ys = y + 60 if is_en else y - 60
                for i in an.svoystva_all:
                    if is_en:
                        if i.angle != 180:
                            i.image = pygame.transform.rotate(i.image, 180)
                            i.angle = 180
                        ys += 20
                    else:
                        ys -= 20
                        if i.angle == 180:
                            i.image = pygame.transform.rotate(i.image, 180)
                            i.angle = 0
                    i.rect = i.image.get_rect(center=(x, ys))
                    display.blit(i.image, i.rect)

            an.food.update(an.rect.x, an.rect.y, an.layer_s)
            an.food.draw(display)
            t += 1


class AddAnimalArea(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("add_animal.png").convert_alpha()
        self.rect = self.image.get_rect(center=(50, 750))


def test_f():
    # тест фазы развтия

    rng = random.Random(5)
    deck = Deck("deck.csv")
    rng.shuffle(deck.cards)
    # for card in deck.cards:
    #    print(card.info())

    pl1 = Player(1)
    pl1.add_cards_from_deck(deck)

    pl2 = Player(2)
    pl2.add_cards_from_deck(deck)
    print(pl1)
    print(pl2)
    # создаем животных игрокам
    pl1.selected = pl1.hand[4]
    pl1.add_animal()
    pl1.selected = pl1.hand[4]
    pl1.add_animal()
    pl1.selected = pl1.hand[3]
    pl1.add_animal()
    pl2.selected = pl2.hand[0]
    pl2.add_animal()

    pl1.add_property(pl1.animals[2], pl1.hand[1].svoystva[0])
    pl1.add_property(pl1.animals[0], pl1.hand[0].svoystva[0])


    pl2.add_property(pl2.animals[0], pl2.hand[0].svoystva[0])
    pl2.add_property(pl2.animals[0], pl2.hand[1].svoystva[0])
    pl2.add_property(pl2.animals[0], pl2.hand[0].svoystva[0])
    pl1.printanimals()

    for i in [pl1, pl2]:
        for an in i.animals:
            print(f"у животного {i.animals.index(an) + 1} игрока {i.number}: свойства {an.svoystva_all} ")
    # In[456]:

    # тест фазы кормления
    for animal in pl1.animals:
        animal.food = 0
    for animal in pl2.animals:
        animal.food = 0
    feed_base = 5
    # random.randint(1, 6) + 2
    print(feed_base)


    # животное 1 игрока 1
    feed_base = pl1.feed_animal_red(pl1.animals[1], feed_base)
    # животное 1 игрока 2
    pl1.animals[2].svoystva_all[0].attack(pl1.animals[2], pl1, pl1.animals[1], pl1)
    # feed_base = pl2.feed_animal_red(pl2.animals[0], feed_base)
    # животное 1 игрока 1
    # feed_base = pl1.feed_animal_red(pl1.animals[0], feed_base)
    # животное 1 игрока 2
    # feed_base = pl2.feed_animal_red(pl2.animals[0], feed_base)
    pl2.animals[0].svoystva_all[0].attack(pl2.animals[0], pl2, pl1.animals[1], pl1)
    # животное 3 игрока 1
    # feed_base = pl1.feed_animal_red(pl1.animals[2], feed_base)
    feed_base = pl2.feed_animal_red(pl2.animals[0], feed_base)
    print(feed_base)

    for i in [pl1, pl2]:
        for an in i.animals:
            print(f"у животного {i.animals.index(an) + 1} игрока {i.number}: еды {an.food} ")
    # print(f"у животного 2 игрока 1: еды {pl1.animals[1].food} ")
    # print(f"у животного 3 игрока 1: еды {pl1.animals[2].food} ")
    # print(f"у животного 1 игрока 2: еды {pl2.animals[0].food} ")

    # In[458]:

    # фаза вымирания

    for animal in pl1.animals:
        if animal.food < animal.need_food_count():
            pl1.animals.remove(animal)


squares = []  # массив карт

# for card in deck.cards:
#    print(card.info(


new = Game()
pygame.quit()

