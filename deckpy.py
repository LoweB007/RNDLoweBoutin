import csv
import random
import pygame


class Svoystvo:
    def __init__(self, name):
        self.name = name
        self.need_food = 0
        self.image = pygame.image.load("BigSv.png").convert_alpha()
        self.rect = self.image.get_rect(center=(200, 200))

    def protection(self, animal, carnivore):
        return


class Card:
    def __init__(self, index, svoystva, picture, out=False):
        self.image = pygame.image.load("evolution.jpg").convert_alpha()
        self.rect = self.image.get_rect(center=(200, 200))
        self.index = index
        self.svoystva = svoystva
        self.picture = picture
        self.x = 200
        self.y = 200
        self.dragged = False
        self.out = out
        self.angle = 0

    def info(self):
        a = self.svoystva[0]
        b = self.svoystva[1]
        if b != "":
            return a.name, b.name
        return a.name, b


class Carnivore(Svoystvo):
    def __init__(self, name):
        super().__init__(name)
        self.need_food = 1

    def attack(self, animal, player, target, attaked_player):
        if animal.food < animal.need_food_count():
            attack_success = False
            if self.detect_need_props(animal, target):
                attack_success = True
                print("атака успешна")
            if attack_success:
                attaked_player.animals.remove(target)
                player.feed_animal_blue(animal)
                player.feed_animal_blue(animal)

    def detect_need_props(self, animal, target):
        attack_props_types = set()
        for prop in animal.svoystva_all:
            attack_props_types.add(type(prop))
        for prop in target.svoystva_all:
            if prop.protection(animal, target):
                if prop.counter_prop not in attack_props_types:
                    print(f"нет свойства {prop.counter_prop}")
                    return False

        return True


class Camouflage(Svoystvo):
    def __init__(self, name):
        super().__init__(name)
        self.need_food = 0
        self.counter_prop = SharpVision

    def protection(self, animal, carnivore):
        return SharpVision


class Big(Svoystvo):
    def __init__(self, name):
        super().__init__(name)
        self.need_food = 1
        self.counter_prop = Big
        self.image = pygame.image.load("BigSv.png").convert_alpha()
        self.rect = self.image.get_rect(center=(200, 200))
        self.angle = 0

    def protection(self, animal, carnivore):
        return Big


class SharpVision(Svoystvo):
    def __init__(self, name):
        super().__init__(name)
        self.need_food = 0


class FatTissue(Svoystvo):
    def __init__(self, name):
        super().__init__(name)
        self.need_food = 0


# In[351]:


class Deck:
    def __init__(self, name):
        self.cards = []
        self.read_cards(name)
        # self.remix_cards()

    def get_cards(self, n):
        if len(self.cards) >= n:
            res = self.cards[0:n]
            del self.cards[0:n]
            return res

    def remix_cards(self):
        random.shuffle(self.cards)

    def read_cards(self, name):
        csvfile = open(name, encoding="utf8")
        reader = csv.reader(csvfile, delimiter=';')
        index = 0
        for line_dict in list(reader)[1:]:
            kol = int(line_dict[1])
            for _ in range(kol):
                props = line_dict[0].split(' / ')
                prop1 = eval(props[0])(props[0])
                prop2 = ""
                if len(props) > 1:
                    prop2 = eval(props[1])(props[1])
                self.cards.append(Card(index, [prop1, prop2], line_dict[2]))
                index += 1

    def info(self):
        return len(self.cards)
