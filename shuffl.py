# Shuffle decode/encode

from math import fabs as abs
from decimal import Decimal as d
from decimal import *

class shuffl:

    def __init__(self, text = None, totalObjects = 1):
        self.text = text
        self.totalObjects = 1
        
    def setPrecision(self,num):
        getcontext().prec = num

    def setTotalObjects(self,num):
        self.totalObjects = num


    @staticmethod
    def decToBin(n):
        total = ""
        while n > 0:
            total = str(n%d(2)) + total
            n = n//d(2)
        return total

    @staticmethod
    def binToDec(n):
        total = d(0)
        n = n[::-1]
        for i in range(len(n)):
            total += d(n[i])*(d(2)**d(i))
        return total

    @staticmethod
    def fact(n):
        n = d(n)
        n //= d(1)
        if (n == d(0)): return d(1)
        total = d(1)
        step = d(1)
        while step <= n:
            total *= step
            step += d(1)
        return total

    def textToNum(text,key='a',cypher=" abcdefghijklmnopqrstuvwxyz,./'@"):
        text = text.lower()
        dict = {letter:num for (num,letter) in enumerate(list(cypher))}
        bigboi = ""

        for letterNum,letter in enumerate(text):
            temp = "{0:b}".format((dict[letter] + dict[key[letterNum%(len(key))]]) % 32)
            while len(temp) != 6:
                temp = "0" + temp
            bigboi = bigboi + temp

        return binToDec(bigboi)

    def numToText(num,key='a',cypher=" abcdefghijklmnopqrstuvwxyz,./'@"):
        code = list(cypher)
        text = ""

        binNum = decToBin(num)
        while len(binNum)%6 != 0:
            binNum = "0" + binNum
        splitNums = [int(binNum[x:x+6],2) for x in range(0,len(binNum),6)]

        for splitID,splitNum in enumerate(splitNums):
            text = text + code[(splitNum - code.index(key[splitID%(len(key))]))%32]

        return text

    # convert a numerical value to a list of slot numbers
    def numToSlot(value,total):
        total = d(int(abs(total)))
        value = d(value)
        max = fact(total)      # calculate max combinations
        slotNum = total        # slot column number, starting with highest value and decrements
        slot = value           # slot value carried within loop for calculations

        slots = []             # slot numbers to return

        # kill if value is out of bounds
        if (value > max) or (value < d(0)):
            raise ValueError("Value too big to store")

        # loop until all necessary slots filled (total number of items shuffled - 1)
        for _ in range(int(total)-1):
            max /= slotNum                # reduce factorial by 1. (e.g. 4!/4 = 3!)
            slotNum -= d(1)               # decrement slot number
            slots.append(slot//max)       # add slot number as rounded-down quotient of the now reduced max and value
            slot %= max                   # get the remainder for next calculation

        return slots

    # convert a list of slot numbers to a numerical value
    def slotToNum(slots):
        total = len(slots)
        value = d(0)

        for slot in slots:
            value += (slot*fact(total))//1
            total -= d(1)

        return value

    # convert a list of slot numbers to a unique order of numbers
    def slotToOrder(slots):
        items = list(range(len(slots) + 1))
        order = []

        for slot in slots:
            order.append(items.pop(int(slot)))
        order.append(items[0])

        return order

    # convert a unique order of numbers to slot numbers
    def orderToSlot(order):
        if verifyOrder(order) != True:
            raise Exception("Invalid order list")

        total = len(order)
        items = list(range(total))
        slots = []

        for _ in range(total - 1):
            slots.append(items.index(int(order[0])))
            items.pop(items.index(int(order[0])))
            order.pop(0)

        return [d(slot) for slot in slots]

    def orderToCards(order):
        shape = ["Spd","Hrt","Diam","Clb"]
        symbol = ["A",'2','3','4','5','6','7','8','9','10','J','Q','K']
        return [symbol[item%13]+"-"+shape[item//13] for item in order]

    def cardsToOrder(cards):
        shape = ["S","H","D","C"]
        symbol = ["A",'2','3','4','5','6','7','8','9','10','J','Q','K']
        cards = [card.upper().split('-') for card in cards]
        return [symbol.index(card[0])+(13*shape.index(card[1][0])) for card in cards]


    # verify order integrity
    def verifyOrder(toCheck):
        toVerify = toCheck[:]
        toVerify.sort()
        perfect = list(range(toVerify[-1] + 1))
        return toVerify == perfect

    # shortcut
    def numToOrder(value,total):
        return slotToOrder(numToSlot(value,total))

    # shortcut
    def orderToNum(order):
        return slotToNum(orderToSlot(order))


def main():
    numShuffled = d(80)

    #                 _____________________________________
    text = textToNum("login at endium.com/horseradish")
    print(text)
    encoded = numToOrder(text,numShuffled)
    # print(orderToCards(encoded))
    print(encoded)
    # print(cardsToOrder(orderToCards(encoded)))
    encoded = orderToNum(encoded)
    print(encoded)
    encoded = numToText(encoded)
    print(encoded)

main()
