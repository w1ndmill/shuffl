# Shuffle decode/encode

from math import fabs as abs
from math import ceil
from decimal import Decimal as d
from decimal import *

class shuffl:

    def __init__(self, data = None, totalObjects = 1):
        self.data = data
        self.dataType = None
        self.totalObjects = totalObjects

    cypher32  = " abcdefghijklmnopqrstuvwxyz,./'@"
    cypher64a = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz."
    cypher64b = " 1234567890abcdefghijklmnopqrstuvwxyz!@#$%^&*()-=_+;':\",./<>?~`|"

    def setPrecision(self,num):
        getcontext().prec = num

    def setTotalObjects(self,num):
        self.totalObjects = num

    def textToNum(self, text, key='a', cypher = shuffl.cypher32):
        text = text.lower()
        code = {letter:num for (num,letter) in enumerate(list(cypher))}
        bigboi = ""

        # convert text characters to binary, then append to string
        for letterNum,letter in enumerate(text):
            temp = "{0:b}".format((code[letter] + code[key[letterNum%(len(key))]]) % len(code))
            while len(temp) != 6:
                temp = "0" + temp
            bigboi = bigboi + temp

        # return value in Decimal
        return binToDec(bigboi)

    def numToText(self,num,key='a',cypher = shuffl.cypher32):
        code = list(cypher)
        text = ""

        binNum = decToBin(num)
        while len(binNum)%6 != 0:
            binNum = "0" + binNum
        splitNums = [int(binNum[x:x+6],2) for x in range(0,len(binNum),6)]

        for splitID,splitNum in enumerate(splitNums):
            text = text + code[(splitNum - code.index(key[splitID%(len(key))])) % len(code)]

        return text

    # convert a numerical value to a list of slot numbers
    def numToSlot(self,value,total):
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
    def slotToNum(self,slots):
        total = len(slots)
        value = d(0)

        for slot in slots:
            value += (slot*fact(total))//1
            total -= d(1)

        return value

    # convert a list of slot numbers to a unique order of numbers
    def slotToOrder(self,slots):
        items = list(range(len(slots) + 1))
        order = []

        for slot in slots:
            order.append(items.pop(int(slot)))
        order.append(items[0])

        return order

    # convert a unique order of numbers to slot numbers
    def orderToSlot(self,order):
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

    # shortcut
    def numToOrder(value,total):
        return slotToOrder(numToSlot(value,total))

    # shortcut
    def orderToNum(order):
        return slotToNum(orderToSlot(order))

    # suggested precision for # of objects given
    # 0.509x^1.24+1 --- Best under 1000 objects
    @staticmethod
    def suggestedPrecision(n):
        return ceil(0.509*(n**1.24))+1

    # verify order integrity
    # (i.e. sequence ordered is 0,1,2...n-1,n)
    @staticmethod
    def verifyOrder(toCheck):
        toVerify = toCheck[:]
        toVerify.sort()
        perfect = list(range(toVerify[-1] + 1))
        return toVerify == perfect

    # convert from decimal to binary supporting Decimal
    @staticmethod
    def decToBin(n):
        total = ""
        while n > 0:
            total = str(n%d(2)) + total
            n = n//d(2)
        return total

    # convert from binary to decimal supporting Decimal
    @staticmethod
    def binToDec(n):
        total = d(0)
        n = n[::-1]
        for i in range(len(n)):
            total += d(n[i])*(d(2)**d(i))
        return total

    # performs factorial supporting Decimal
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
