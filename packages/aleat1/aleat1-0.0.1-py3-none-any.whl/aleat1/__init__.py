"""The Diddi's Aleatoryous Object."""

"""This object was created to give 2 values:
   1. A 'dice' algorythm.
   2. A 'coin' algorythm.

Created by Diego Ramirez and the Ramz Editions (c) Team. 2020 All rights reserved."""

import time
import random

class Aleatoryous():
    tot = 0
    mode = ""
    lst = []
    it = None

    def __init__(self, mode):
        if mode == "aleatory.coin":
            self.mode = "Coin"
        elif mode == "aleatory.dice":
            self.mode = "Dice"
        else:
            print("Diddi-Aleatoryous Execution Error: '__init__' Method Invalid Syntax (Unexpected code given)")
            quit()


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
        for time in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20]:
            self.first_5_basic()
        return self.lst
