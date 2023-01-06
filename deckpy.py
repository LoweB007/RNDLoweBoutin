import csv
import random


class Svoystvo:
    def __init__(self, name):
        self.name = name
        self.need_food = 0


class Card:
    def __init__(self, index, svoystva, out=False):
        self.index = index
        self.svoystva = svoystva
        self.out = out

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


class Camouflage(Svoystvo):
    def __init__(self, name):
        super().__init__(name)
        self.need_food = 0


class SharpVision(Svoystvo):
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
                self.cards.append(Card(index, [prop1, prop2]))
                index += 1

    def info(self):
        return len(self.cards)
