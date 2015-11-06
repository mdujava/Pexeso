import random
import math


#############################################################################
class EngineRandom:
    """Only random moves"""

    def playAll(self):
        while self.game.state() > 0:
            self.playOne()

    def playOne(self):
        self.game.uncover(math.floor(random.uniform(0, self.numberOfCards)))

    def getNumberOfMoves(self):
        return self.game.numberOfMoves

    def __init__(self, game, debug=False):
        self.game = game
        self.debug = debug
        self.numberOfCards = game.numberOfPairs * 2

#############################################################################
#***************************************************************************#
#############################################################################

class EngineMemory(EngineRandom):
    """Engine with memory of N cards, only for last N cards"""

    def playOne(self):
        lastCard = self.game.lastUncoveredCard()
        move = 0
        # second move in row
        if isinstance(lastCard, list):
            move = 1
            for i in range(0, len(self.memory)):
                if ((self.memory[i])[0] == lastCard[0]) and ((self.memory[i])[1] != lastCard[1]):
                    self.game.uncover((self.memory[i])[1]) 
                    self.memorizeCard(self.game.lastUncoveredCard())
                    move = -1
        # first move in row or we dont have second card in memory
        if move != -1:    
            # first move in row 
            nextMove = self.checkForPairInMemory()
            if nextMove != -1:
                self.game.uncover(nextMove)
                self.memorizeCard(self.game.lastUncoveredCard())
                return
            # we dont have second card in memory
            possibleMoves = self.game.possibleMoves()
            # remove memorized cards from possibleMoves
            for i in range(0, len(self.memory)):
                for j in range(0, len(possibleMoves)):
                    if self.memory[i][1] == possibleMoves[j]:
                        possibleMoves.pop(j)
                        break
            # pick random from card that is not in memory and is on playfield
            if (len(possibleMoves) > 0):
                pick = random.choice(possibleMoves)
                self.game.uncover(pick)
                self.memorizeCard(self.game.lastUncoveredCard())
            else:
                pick = random.choice(self.game.possibleMoves())
                self.game.uncover(pick)
                self.memorizeCard(self.game.lastUncoveredCard())

    def checkForPairInMemory(self):
        for i in range(0, len(self.memory)):
            for j in range(i + 1, len(self.memory)):
                if self.memory[i][1] == self.memory[j][1]:
                    return j
        return -1

    def memorizeCard(self, cardPosition):
        if not isinstance(cardPosition, list):
            return
        # check if I already have exact same card
        for i in range(0, len(self.memory)):
            if (self.memory[i])[0] == cardPosition[0]:
                if (self.memory[i])[1] == cardPosition[1]:
                    return
        # remove last cards to free up one space 
        while len(self.memory) >= self.sizeOfMemory:
            self.memory.pop(0)
        # append card to end of memory
        self.memory.append(cardPosition)

    def __init__(self, game, sizeOfMemory, debug=False):
        super(self.__class__, self).__init__(game, debug) # referring to parent INIT 
        if sizeOfMemory == -1:
            self.sizeOfMemory = self.numberOfCards
        else:
            self.sizeOfMemory = sizeOfMemory
        self.memory = []

#############################################################################
