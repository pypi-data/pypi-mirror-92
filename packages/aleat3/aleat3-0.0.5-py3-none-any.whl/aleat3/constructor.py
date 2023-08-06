# The whole syntax of Aleatoryous3

__all__ = ["__author__",
           "__version__",
           "InitError",
           "Aleatoryous",
           "coinToBinary"]

__author__ = "Diego Ramirez"
__version__ = "0.0.4"


import random
from aleat3.errors import init_errors as IE


class InitError(TypeError):
    pass


class Aleatoryous():
    "New since 0.0.4: Some variables deleted or recycled"
    tot = 0
    #__cache = ["Coin", "Dice", "Roulette"]
    __mode = ""
    parser = ""
    lst = []
    __methods = ["__init__",
                 "__len__",
                 "__dir__",
                 "refresh",
                 "single",
                 "first_5",
                 "first_10",
                 "first_50",
                 "first_100",
                 "first_given",
                 "getmode",
                 "changemode"]
    dict = {}
    #it = None

    def __init__(self, mode="aleatory.coin", extras=None):
        if mode == "aleatory.coin":
            self.__mode = "Coin"
        elif mode == "aleatory.dice":
            self.__mode = "Dice"
        elif mode == "aleatory.roulette":
            self.__mode = "Roulette"
            if extras is not None:
                self.parser = extras
            elif not isinstance(self.parser, "list"):
                raise InitError(IE.parameter_bug())
            else:
                pass
            for i in range(len(self.parser)):
                self.it = i + 1
                self.dict[self.parser[i]] = self.it
        else:
            raise InitError(IE.modal_bug())
        #self.cache = ""
        self.__modetye = mode
        self.parser = ""


    def refresh(self):
        self.tot = ""
        self.lst = []


    def single(self):
        if self.__mode == "Coin":
            self.tot = random.randint(0, 1)
            if self.tot == 1:
                return "Head"
            elif self.tot == 0:
                return "Tails"
            else:
                return None

        elif self.__mode == "Dice":
            self.tot = random.randint(1, 6)
            return self.tot

        elif self.__mode == "Roulette":
            self.tot = random.randint(1, len(self.dict))
            for k, v in self.dict.items():
                if v == self.tot:
                    self.tot = k
                    break
            return self.tot


    def first_5_basic(self):
        for time in [1, 2, 3, 4, 5]:
            if self.__mode == "Coin":
                self.tot = random.randint(0, 1)
                if self.tot == 1:
                    self.lst.append("Head")
                elif self.tot == 0:
                    self.lst.append("Tails")
                else:
                    self.lst.append(None)
            elif self.__mode == "Dice":
                self.tot = random.randint(1, 6)
                self.lst.append(self.tot)
            elif self.__mode == "Roulette":
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

    def getmode(self):
        "New since 0.0.3: get the private mode."
        self.refresh()
        return self.__modetype

    def changemode(self, mode, extras=None):
        "New since 0.0.3: restart the object with a new mode."
        self.__init__(mode, extras)

    # Some built-in functions
    def __len__(self):
        return 3  # The 3 modes
    def __dir__(self):
        return self.__methods
    def __str__(self):
        return "Aleatoryous" + " " + self.__modetype


def coinToBinary(res):
    if res.strip().lower() == "head":
        return 1
    elif res.strip().lower() == "tails":
        return 0
    else:
        return None

if __name__ == '__main__':
    # Try the new function Aleatoryous.changemode() of version 0.0.3
    _i = Aleatoryous("aleatory.dice")
    _i.changemode("aleatory.coin")
    print("Done")
