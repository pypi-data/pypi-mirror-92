# The whole syntax of Aleatoryous3

__all__ = ["__author__",
           "__version__",
           "InitError",
           "Aleatoryous",
           "coinToBinary"]

__author__ = "Diego Ramirez (dr01191115@gmail.com) @DiddiLeija"
__version__ = "0.0.7"


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
    __it = 0

    def __init__(self, mode="aleatory.coin", extras=None):
        if mode == "aleatory.coin":
            self.__mode = "Coin"
            self.__it = 2
        elif mode == "aleatory.dice":
            self.__mode = "Dice"
            self.__it = 6
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
            self.__it = len(self.parser)
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
        "New since 0.0.6: Faster operations"
        for time in [1, 2, 3, 4, 5]:
            self.lst.append(self.single())


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


    def first_given(self, how, /, repeat=True):
        "New since 0.0.6: You can iterate with no repetition"
        "New since 0.0.7: No-repetition operation corrected"
        self.refresh()
        if not isinstance(how, "int"):
            raise SyntaxError(f"Expected integers, %s given" % type(how))
        if not isinstance(rep, "bool"):
            raise SyntaxError(f"At parameter 'repeat', you must enter True or False, not %s" % repeat)
        else:
            if self.__mode == "Coin" and repeat is False:
                raise SyntaxError(f"'No-repetition' feature is not available for 'aleatory.dice' objects")
            if not repeat and how > self.__it:
                raise SyntaxError(f"Cannot give more than %s iterations without repetitions." % self.__it)
        if repeat:
            for time in range(how):
                self.lst.append(self.single())
        else:
            while len(self.lst) != how:
                possible = self.single()
                if possible in self.lst:
                    continue
                self.lst.append(possible)
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
        return "Aleatoryous " + self.__modetype


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
