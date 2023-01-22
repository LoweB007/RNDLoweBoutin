#!/usr/bin/env python
# coding: utf-8

# In[348]:


from deckpy import Deck, Svoystvo, Carnivore, Camouflage, SharpVision
from frontend import choose_obj
import random
import pygame
from random import shuffle, Random
import csv
BASENCARDS = 6


# In[353]:


class Game:
    def __init__(self):
        self.deck = Deck("deck.csv")
        self.players = [Player(1),
                        Player(2)]
        self.players[0].add_cards_from_deck(self.deck)
        self.players[1].add_cards_from_deck(self.deck)
        self.players[0].printcard()
        self.players[1].printcard()
        self.eat_base = 0
        print("___________________фаза развития_______________________")
        self.evo_phase()
        print("___________________фаза кормления_______________________")
        self.eat_phase()
        print("___________________фаза вымирания_______________________")
        self.dead_phase()
        print("___________________подсчет очков_______________________")
        self.score_phase()

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

    def dead_phase(self):
        for pl in self.players:
            for animal in pl.animals:
                if animal.food < animal.need_food_count():
                    pl.animals.remove(animal)
        
    def score_phase(self):
        for pl in self.players:
            print(pl)
        print("Конец игры")

    def testprimer(self):
        for pl in self.players:
            pass


# In[354]:


# class Card:
#     def __init__(self, index, svoystva, out=False):
#         self.index = index
#         self.svoystva = svoystva
#         self.out = out
#
#     def info(self):
#         a = self.svoystva[0]
#         b = self.svoystva[1]
#         if b != "":
#             return a.name, b.name
#         return a.name, b


# In[428]:


class Animal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("evolution.jpg").convert_alpha()
        self.rect = self.image.get_rect(center=(600, 500))
        self.svoystva_all = []
        self.isalive = True
        self.food = 0
        self.needfood = 1
        self.svoystva_used_of_turn = []
        
    def need_food_count(self):
        self.needfood = 1
        for svoystvo in self.svoystva_all:
            self.needfood = self.needfood+svoystvo.need_food
        return self.needfood


# In[440]:


class Player:
    def __init__(self, number):
        self.number = number
        self.hand = []
        self.animals = []
        self.selected = None
        self.notpass = False
        self.an_add = ""

    def __str__(self):
        return "карты игрока" + str(self.printcard()) + "\nживотные игрока" + str(self.printanimals())
    
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
            if an.food < an.needfood:
                ans.append(an)
        return ans
    
    def add_animal(self):
        card_id = self.hand.index(self.selected)
        lan = self.animals.copy()
        lan.append(Animal())
        self.animals = lan
        del self.hand[card_id]
    
    def add_cards_from_deck(self, deck):
        if not self.animals:
            count_animals = 6
        else:
            count_animals = len(self.animals)+2
        for new_card in deck.get_cards(count_animals):
            self.hand.append(new_card)
        return
    
    def add_property(self, animal, prop_in_card):
        card_id = self.hand.index(self.selected)
        animal_id = self.animals.index(animal)
        svoysyvo = self.animals[animal_id].svoystva_all.copy()
        svoysyvo.append(prop_in_card)
        self.animals[animal_id].svoystva_all = svoysyvo
        del self.hand[card_id]
        return
    
    def feed_animal_red(self, animal, feed_base):
        if feed_base > 0 and animal.need_food_count() > animal.food:
            feed_base = feed_base - 1
            animal.food = animal.food + 1
        return feed_base

    def feed_animal_blue(self, animal):
        if animal.need_food_count() > animal.food:
            animal.food = animal.food + 1

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


class AddAnimalArea(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("add_animal.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 600))


# In[455]:

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

    # In[457]:

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






pygame.init()
W, H = 1800, 1000
SW, SH = 90, 120
display = pygame.display.set_mode((W, H))
screen = display.copy()

squares = []
rng = Random(5)
deck = Deck("deck2.csv")
rng.shuffle(deck.cards)
# for card in deck.cards:
#    print(card.info())

pl1 = Player(1)
pl1.add_cards_from_deck(deck)
pl1.an_add = AddAnimalArea()
pl2 = Player(2)
pl2.add_cards_from_deck(deck)
pl2.an_add = AddAnimalArea()
for x in range(len(pl1.hand)):
    pl1.hand[x].obj_rect = [pygame.Rect(x * 100 + 700, 800, SW, SH), False, "green", False]
    pl1.hand[x].x = x * 100 + 700
    pl1.hand[x].y = 800
for x in range(len(pl2.hand)):
    pl2.hand[x].obj_rect = [pygame.Rect(x * 100 + 700, 800, SW, SH), False, "green", False]
    pl2.hand[x].x = x * 100 + 700
    pl2.hand[x].y = 800
n = 1

while True:

    act_pl, en_pl = (pl2, pl1) if n == -1 else (pl1, pl2)
    squares = pygame.sprite.Group()
    for card in act_pl.hand:
        card.image = pygame.image.load(card.picture).convert_alpha()
        card.rect = card.obj_rect[0]
        squares.add(card)
    e = pygame.event.wait()
    if e.type == pygame.QUIT or e.type == pygame.KEYUP and e.key == 27:
        break
    elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        # for x in squares:
        #     x[3] = False
        for square in squares:
            if square.rect.collidepoint(e.pos):
                square.dragged = True
                act_pl.selected = square
                # square[3] = True
    elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
        for square in squares:
            if square.dragged:
                square.dragged = False
                square.rect.center = e.pos
    elif e.type == pygame.MOUSEMOTION and e.buttons[0]:
        for square in squares:
            if square.dragged:
                square.rect.center = e.pos
            if square.rect.colliderect(act_pl.an_add):
                act_pl.add_animal()
            for i in act_pl.animals:
                if square.rect.colliderect(i.rect):
                    act_pl.add_property(i, act_pl.selected.svoystva[0])
    elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
        n *= -1
    else:
        pass
        # print(e)
    screen.fill((255, 255, 255))
    display.blit(screen, (0, 0))
    display.blit(act_pl.an_add.image, act_pl.an_add.rect)
    for card in act_pl.hand:
        display.blit(card.image, card.rect)
    for an in act_pl.animals:
        x = 600 + 140 * act_pl.animals.index(an)
        y = 700
        an.rect = an.image.get_rect(center=(x, y))
        display.blit(an.image, an.rect)
        # y += 60
        print(an.svoystva_all)
        if an.svoystva_all:
            for i in an.svoystva_all:
                y -= 20
                print(i)
                i.rect = an.image.get_rect(center=(x, y))
                display.blit(i.image, i.rect)

    # squares.draw(display)
    pygame.display.update()
    pygame.display.flip()

pygame.quit()

