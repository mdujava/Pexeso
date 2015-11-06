import random
import copy


class Game:

    def playOneEngine(self):
        self.engineOne.playAll()

    def playTwoEngine(self):
        while self.state() > 0:
            if self.whichIsOnMove == 0:
                self.engineOne.playOne()
                self.engineTwo.memorizeCard(self.lastUncoveredCard())
            elif self.whichIsOnMove == 1:
                self.engineTwo.playOne()
                self.engineOne.memorizeCard(self.lastUncoveredCard())

            ### debug
            if self.debug:
                print(self.printState())
                res = input()
                if "-1" in res:
                    self.debug = False
                if "-2" in res:
                    self.debug = False
                    return [self.engineOneScore, self.engineTwoScore, -2]
            ###

        return [self.engineOneScore, self.engineTwoScore]
        
    def uncover(self, currentUncoveredIndex):
        currentUncovered = copy.deepcopy(self.playField[currentUncoveredIndex])
        if currentUncovered == -1:
            return currentUncovered

        if self.lastUncoveredIndex == currentUncoveredIndex:
            # end if try to uncover same card twice
            return -1

        self.removeUncoveredPair(currentUncovered, currentUncoveredIndex)

        return currentUncovered

    def removeUncoveredPair(self, currentUncovered, currentUncoveredIndex):
        # check if this is second move 
        if self.lastUncoveredIndex is None:
            self.lastUncoveredIndex = currentUncoveredIndex
            self.numberOfMoves += 1
        else:
            lastUncovered = self.playField[self.lastUncoveredIndex]
            if lastUncovered == currentUncovered:
                # remove cards from playField
                self.playField[self.lastUncoveredIndex] = -1
                self.playField[currentUncoveredIndex] = -1
                # add score
                if self.whichIsOnMove == 0:
                    self.engineOneScore += 1
                if self.whichIsOnMove == 1:
                    self.engineTwoScore += 1
            else:
                # change engine
                self.whichIsOnMove = 1 - self.whichIsOnMove 
            # after second move clean last card index
            self.lastUncoveredIndex = None
            self.numberOfMoves += 1

    def printState(self):
        if self.debug is True:
            # if debug print plain playField
            return self.playField
        temp = []
        for n, i in enumerate(self.playField):
            # change real card number to 0
            if i == -1:
                temp.append(-1)
            else:
                temp.append(0)
        return temp        

    def state(self):
        temp = 0
        for n, i in enumerate(self.playField):
            # if is in field nonBlank space add one pair
            if i != -1:
                temp += 1
        return temp

    def possibleMoves(self):
        tmp = []
        for n, i in enumerate(self.playField):
            if i != -1:
                tmp.append(n)
        return tmp

    def shuffle(self):
        random.shuffle(self.playField)

    def lastUncoveredCard(self):
        if self.lastUncoveredIndex != None:
            if self.playField[self.lastUncoveredIndex] != -1:
                # return array of card and it's position 
                return [self.playField[self.lastUncoveredIndex], self.lastUncoveredIndex]  
        return -1

    def inicializeEngines(self, engineOne, engineTwo = None):
        self.engineOne = engineOne
        self.engineOneScore = 0
        self.engineTwo = engineTwo
        self.engineTwoScore = 0
        self.whichIsOnMove = 0

    def __init__(self, numberOfPairs, debug = False):
        self.numberOfPairs = numberOfPairs
        self.debug = debug
        self.numberOfMoves = 0
        self.lastUncoveredIndex = None
        self.playField = list(range(1, numberOfPairs + 1)) + list(range(1, numberOfPairs + 1))
        self.shuffle()
        if self.debug:
            print("-1 = to disable debug for one game")
            print("-2 = to disable debug for all game")
            print("enter to continue press")
