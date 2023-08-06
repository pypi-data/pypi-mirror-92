"""The Diddi's Aleatoryous Object.
===============================================================================================================================
INTRODUCTION

This object was created to give the folowing values:
   1. A 'dice' algorythm.
   2. A 'coin' algorythm.
   3. A 'roulette' algorythm.

Also, in this edition we give a little guide of the posible custom methods of Aleatoryous.
===============================================================================================================================
USER GUIDE

To call this Object, type this:

>>>from aleat2 import Aleatoryous

Now, the object creation has two parameters that you should give:

>>>object = Aleatoryous("aleatory.dice", None)
                                 ^         ^
1. The 'mode'.
2. The objects (only for the 'roulette' syntax. In other cases, type None).

The method single() gets only one iteration, and can return a Value (String or Integer (In the case of the 'Dice')):

>>>coin = Aleatoryous("aleatory.coin", None)
>>>print(coin.single())
Head
>>>print(coin.single())
Head
>>>print(coin.single())
Tails

The method first_5() does the same 5 times and returns a list:

>>>dice = Aleatoryous("aleatory.dice", None)
>>>print(dice.first_5())
[6, 3, 5, 6, 1]

The methods first_5_basic() and refresh() are called internally ONLY.
The 'Roulette' syntax is more complex than the others. Look at this:

>>>roul = Aleatoryous("aleatory.roulette", 5)    # The second value means: the number of values included...
...
Enter a key for the roulette: Go to sleep
Enter a key for the roulette: Play videogames
Enter a key for the roulette: Play the guitar
Enter a key for the roulette: Make a phone call to Castol
Enter a key for the roulette: Nothing
Done

But the rest is not so different:

>>>print(roul.single())
Make a phone call to Castol
>>>print(dice.first_5())
["Make a phone call to Castol", "Play videogames", "Go to sleep", "Nothing", "Make a phone call to Castol"]

The methods first_10(), first_50() and first_100() are variations of first_5(), so they work as the same:

>>>dice = Aleatoryous("aleatory.dice", None)
>>>tot = dice.first_100
>>>print(tot[45])
4
>>>print(tot[99])
2
>>>print(tot[12:14])
[5, 1]
===============================================================================================================================
CREDITS

Created by Diego Ramirez and the Ramz Editions (c) Team. 2020 All rights reserved."""



import time
import random

class Aleatoryous():
    tot = 0
    cache = ""
    mode = ""
    parser = ""
    lst = []
    dict = {}
    it = None

    def __init__(self, mode, extras):
        if mode == "aleatory.coin":
            self.mode = "Coin"
        elif mode == "aleatory.dice":
            self.mode = "Dice"
        elif mode == "aleatory.roulette":
            self.mode = "Roulette"
            if extras is not None:
                self.parser = extras
            else:
                raise TypeError(f"Diddi-Aleatoryous Execution Error: __init__() Method Invalid Syntax (Unexpected parameter given)")
            try:
                print("...")
                time.sleep(3)
            except KeyboardInterrupt:
                raise KeyboardInterrupt(f"Diddi-Aleatoryous __init__() Error: Program Interrupted by User...")
            while self.parser != 0:
                self.it = input("Enter a key for the roulette: ")
                self.it = self.it.strip()
                self.dict[self.it] = self.parser
                self.parser = self.parser - 1
            print("Done")
        else:
            raise TypeError(f"Diddi-Aleatoryous Execution Error: __init__() Method Invalid Syntax (Unexpected modal-code given)")
        self.cache = ""
        self.it = None
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
        for time in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20]:
            self.first_5_basic()
        return self.lst
