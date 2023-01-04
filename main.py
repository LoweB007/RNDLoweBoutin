from deckpy import Deck, Card, Svoystvo
from frontend import choose_obj
import random
BASENCARDS = 6


class Game:
    def __init__(self):
        self.deck = Deck("test_deck.csv")
        self.players = [Player(1, self.deck.get_cards(BASENCARDS)),
                        Player(2, self.deck.get_cards(BASENCARDS))]
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

    def add_animal(self, player):
        card_id = player.hand.index(player.selected)
        lan = player.animals.copy()
        lan.append(Animal())
        player.animals = lan
        del player.hand[card_id]

    def add_property(self, player, an, card, prop_in_card):
        card_id = player.hand.index(card)
        an_id = player.animals.index(an)
        sv = player.animals[an_id].svoystva_all.copy()
        sv.append(prop_in_card)
        player.animals[an_id].svoystva_all = sv
        del player.hand[card_id]

    def prop_chooses(self, player):
        an = choose_obj([player.printanimals()],
                        player.animals,
                        "0 - пас\nвыберите номер животного:", True)
        pr1 = player.selected.svoystva[0].name
        pr2 = player.selected.svoystva[1].name if player.selected.svoystva[1] != "" else ""
        prop_in_card = choose_obj([f"1 - {pr1}",
                                   f"2 - {pr2}"],
                                  player.selected.svoystva,
                                  "0 - пас\nвыберите свойство:", True)
        self.add_property(player, an,
                          player.selected, prop_in_card)

    def act_choose(self, player):
        player.selected = choose_obj(player.printcard(),
                                     player.hand,
                                     f"0 - пас\nplayer{player.number} введите номер карты:",
                                     True)
        if player.selected != "":  # игрок нажал пас
            action = choose_obj(["1 - выложить как животное",
                                 "2 - выложить как свойство"],
                                [self.add_animal, self.prop_chooses],
                                "введите номер действия:", True)
            if action != "":
                action(player)
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
        self.eat_base = random.randint(1, 7) + 2
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
                    player.selected.food += 1

                else:
                    playerpasses[playerid] = False
            raundkorm = raundkorm + 1

    def dead_phase(self):
        for pl in self.players:
            for an in range(len(pl.animals)):
                pl.animals.pop(an)
        print("все животные погибли")

    def score_phase(self):
        for pl in self.players:
            pl.printanimals(pl.animals)
        print("Конец игры")

    def testprimer(self):
        for pl in self.players:
            pass


class Animal:
    def __init__(self, svoystva_all=[], food=0, svoystva_used_of_turn=[]):
        self.svoystva_all = svoystva_all
        self.isalive = True
        self.food = food
        self.needfood = 1
        self.svoystva_used_of_turn = svoystva_used_of_turn


class Player:
    def __init__(self, number, hand=[], animals=[]):
        self.number = number
        self.hand = hand
        self.animals = animals
        self.selected = None
        self.notpass = False

    def printanimals(self):
        lst = []
        n = 1
        for i in self.animals:
            lst.append(str(f"животное {n} со свойствами: {', '.join([j.name for j in i.svoystva_all])}"))
            n += 1
        return lst

    def printcard(self):
        print(f"   карты {self.number} игрока:")
        lst = []
        n = 1
        for i in self.hand:
            lst.append(str(" ".join(i.info()) + " " + str(n)))
            n += 1
        return lst

    def vvodproverka(self, dost):
        pass

    def is_hungry_animals(self):
        ans = []
        for an in self.animals:
            if an.food < an.needfood:
                ans.append(an)
        return ans


new = Game()
# print("   карты 1 игрока:")
# for i in new.player1.cards:
#     print(*i.info())
#
# print()
#
# print("   карты 2 игрока:")
# for i in new.player2.cards:
#     print(*i.info())
# 1
# 1
# 1
# 1
# 2
# 1
# 2
# 1
# 3
# 1
# 3
# 1
# 1
# 2
# 1
# 1
# 1
# 2
# 1
# 1
# 1
# 2
# 1
# 1
# 1
# 2
# 1
# 1
# 1
# 2
# 1
# 1
# 1
# 2
# 1
# 1

