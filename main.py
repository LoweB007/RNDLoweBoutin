from deckpy import Deck, Card, Svoystvo
from frontend import choose_obj, choose_int
import random
BASENCARDS = 6


class Game:
    def __init__(self):
        self.deck = Deck()
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

    def add_animal(self, player, card):
        card_id = player.hand.index(card)
        lan = []
        lan.append(Animal())
        player.animals = lan
        del player.hand[card_id]

    def add_property(self, player, an_id, card, prop_in_card):
        card_id = player.hand.index(card)
        sv = player.animals[an_id].svoystva_all.copy()
        sv.append(prop_in_card)
        player.animals[an_id].svoystva_all = sv
        del player.hand[card_id]

    def evo_phase(self):
        self.players[0].plpass = True
        self.players[1].plpass = True
        raundcard = 1
        while any(self.players[0].plpass, self.players[1].plpass):
            if self.players[0].hand != [] and self.players[1].hand != []:
                print(f"***** {raundcard} раунд выкладывания карт")
            for playerid in range(2):
                if self.players[playerid].plpass and self.players[playerid].hand != []:
                    self.players[playerid].selected = choose_obj(self.players[playerid].printcard(),
                                                                 self.players[playerid].hand,
                                                                 f"0 - пас\nplayer{playerid + 1} введите номер карты:",
                                                                 True)
                    if self.players[playerid].selected != "":

                        action = choose_int(["1 - выложить как животное",
                                             "2 - выложить как свойство"],
                                            "введите номер действия:")
                        if action == 1:
                            self.add_animal(self.players[playerid], self.players[playerid].selected)
                        elif action == 2 and self.players[playerid].animals != []:
                            print("выберите номер животного:")
                            self.players[playerid].printanimals(self.players[playerid].animals)
                            an_id = int(input()) - 1
                            if self.players[playerid].selected.svoystva[1] != "":
                                prop_in_card = choose_obj([f"1 - {self.players[playerid].selected.svoystva[0].name}",
                                                           f"2 - {self.players[playerid].selected.svoystva[1].name}"],
                                                        self.players[playerid].selected.svoystva,
                                                          "0 - пас\nвыберите свойство:", True)
                            else:
                                prop_in_card = self.players[playerid].selected.svoystva[0]
                            self.add_property(self.players[playerid], an_id,
                                              self.players[playerid].selected, prop_in_card)
                        else:
                            self.players[playerid].plpass = False
                    else:
                        self.players[playerid].plpass = False
                else:
                    self.players[playerid].plpass = False
                raundcard = raundcard + 1

    def eat_phase(self):
        self.eat_base = random.randint(1, 7) + 2
        playerpasses = [True, True]
        raundkorm = 1
        while playerpasses[0] or playerpasses[1]:

            print(f"***** {raundkorm} раунд  кормления")
            for playerid in range(2):
                if playerpasses[playerid] and self.eat_base != 0 and self.players[playerid].is_hungry_animals() != []:
                    self.players[playerid].printanimals(self.players[playerid].is_hungry_animals())
                    ans = int(input(f"player{playerid + 1} введите номер животного:")) - 1
                    self.players[playerid].selected = choose_obj(self.players[playerid].printcard(),
                                                                 self.players[playerid].hand,
                                                                 f"player{playerid + 1} введите номер животного:")
                    self.players[playerid].selected = self.players[playerid].animals[ans]
                    self.players[playerid].selected.food += 1

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
        self.plpass = False

    def printanimals(self, animals):
        lst = []
        n = 1
        for i in animals:
            lst.append(f"животное {n} со свойствами: {[j.name for j in i.svoystva_all]}")
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
