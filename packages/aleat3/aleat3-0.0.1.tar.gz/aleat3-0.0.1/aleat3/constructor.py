# The whole syntax of Aleatoryous3

__all__ = ["__author__",
           "__version__",
           "InitError",
           "Aleatoryous",
           "coinToBinary"]

__author__ = "Diego Ramirez"
__version__ = "3.1"


import random
from aleat3.errors import init_errors as IE


class InitError(TypeError):
    pass


class Aleatoryous():
    tot = 0
    cache = ""
    mode = ""
    parser = ""
    lst = []
    methods = ["__init__", "__len__", "__dir__", "refresh", "single", "first_5", "first_10", "first_50", "first_100", "first"]
    dict = {}
    it = None

    def __init__(self, mode="aleatory.coin", extras=None):
        if mode == "aleatory.coin":
            self.mode = "Coin"
        elif mode == "aleatory.dice":
            self.mode = "Dice"
        elif mode == "aleatory.roulette":
            self.mode = "Roulette"
            if extras is not None:
                self.parser = extras
            else:
                raise InitError(IE.parameter_bug())
            if not isinstance(self.parser, "list"):
                raise InitError(IE.parameter_bug())
            for i in range(len(self.parser)):
                self.it = i + 1
                self.dict[self.parser[i]] = self.it
        else:
            raise InitError(IE.modal_bug())
        self.cache = ""
        self.type = mode
        self.parser = ""


    def refresh(self):
        self.tot = ""
        self.lst = []


    def single(self):
        if self.mode == "Coin":
            self.tot = random.randint(0, 1)
            if self.tot == 1:
                return "Head"
            elif self.tot == 0:
                return "Tails"
            else:
                return None

        elif self.mode == "Dice":
            self.tot = random.randint(1, 6)
            return self.tot

        elif self.mode == "Roulette":
            self.tot = random.randint(1, len(self.dict))
            for k, v in self.dict.items():
                if v == self.tot:
                    self.tot = k
                    break
            return self.tot


    def first_5_basic(self):
        for time in [1, 2, 3, 4, 5]:
            if self.mode == "Coin":
                self.tot = random.randint(0, 1)
                if self.tot == 1:
                    self.lst.append("Head")
                elif self.tot == 0:
                    self.lst.append("Tails")
                else:
                    self.lst.append(None)
            elif self.mode == "Dice":
                self.tot = random.randint(1, 6)
                self.lst.append(self.tot)
            elif self.mode == "Roulette":
                self.tot = random.randint(1, len(self.dict))
                for k, v in self.dict.items():
                    if v == self.tot:
                        self.lst.append(k)
            else:
                pass


    def first_5(self):
        self.refresh()
        self.first_5_basic()
        return self.lst


    def first_10(self):
        self.refresh()
        for time in [1, 2]:
            self.first_5_basic()
        return self.lst


    def first_50(self):
        self.refresh()
        for chance in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            self.first_5_basic()
        return self.lst


    def first_100(self):
        self.refresh()
        for time in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20]:
            self.first_5_basic()
        return self.lst

    def first_given(self, how):
        self.refresh()
        if not isinstance(how, "int"):
            raise InitError(f"Expected integers, % given" % type(how))
        tmp = []
        for time in range(how):
            tmp.append(time + 1)
        for time in tmp:
            self.first_5_basic()
        return self.lst

    # Some built-in functions
    def __len__(self):
        return 3
    def __dir__(self):
        return self.methods
    def __str__(self):
        return "Aleatoryous" + " " + self.mode

def coinToBinary(res):
    if res == "Head":
        return 1
    elif res == "Tails":
        return 0
    else:
        return None
