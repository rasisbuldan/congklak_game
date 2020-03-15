# -*- coding: utf-8 -*-
"""
Updated on Sun March 08 22:04:48 2020

@author: Team 03
"""

# randint(a,b,c), a is smallest value, b is biggest values, c is how much the random number is generated in list/array
from numpy.random import randint
from congklak_model import CongklakModel
from congklak_player import CongklakPlayer

from copy import deepcopy
import sys


class CongklakPlayer03(CongklakPlayer):

    ## ----- AI CODE -----
    __virtualBoard = []  # For virtualizing new board 2x8 array
    # Player 1 7x3 7 = every house, 3 = [house index(1-7), end Board, delta]
    __max1 = []
    __min1 = []  # Player 2
    __maxMinRAM = []  # Player 1

    __warehouseMax = []
    __warehouseMin = []
    __delta = []
    __index = []

    def __init__(self):
        super().__init__('Coooongkyiezz')

        self.board = []
        self.container = []
        self.turn = 1  # Player 1 or 2 giliran
        self.player = 1  # Player 1 or 2 daerah lubang
        self.lastDecision = 0  # between 1-8
        self.gameNotation = []
        self.totalTurn = 0

    '''
    First AI
    '''

    def getVirtualBoard(self):
        return self.__virtualBoard

    def getMax1(self):
        return self.__max1

    def getMin1(self):
        return self.__min1

    def getBoard(self):
        return self.board

    def getTurn(self):
        return self.turn

    def getLastDecision(self):
        return self.lastDecision

    def setTurn(self, turn):
        self.turn = turn

    def setNewDataIndex(self, decision):
        newDataIndex = [decision]
        return newDataIndex

    # player : 1-2, decision : 1-7
    def move(self, player, decision):

        if player > 2 or decision > 7:
            print("the player or decision is not valid!")
            sys.exit()

        # get the marbles
        self.container = self.__virtualBoard[player-1][decision-1]
        self.__virtualBoard[player-1][decision-1] = 0

        # move the marbles
        while self.container > 0:
            self.container -= 1

            # change to the next house
            decision += 1
            # print('House Index to put the marble', decision)

            # Skip the opponent house
            if decision == 8 and self.turn != player:
                decision += 1

            # Change the player house
            if decision > 8:
                player += 1
                if player > 2:
                    player -= 2
                decision -= 8

            # put marble in the next house
            self.__virtualBoard[player-1][decision-1] += 1

        # Set the last player house
        self.player = player

        # Set the last decision
        self.lastDecision = decision

        # print("New Board", self.__virtualBoard)
        # print("Last Index: Region =", self.player, "House = ", self.lastDecision)

        # print("total marble in the last house", self.__virtualBoard[self.player-1][self.lastDecision-1])
        # ----- END CONDITION -----
        # end in the warehouse
        if self.lastDecision == 8:
            # print("END IN WAREHOUSE")
            return self.__virtualBoard

            # if self.turn == 1:
            #     player1Move()
            # else:
            #     player2Move()

        # Move again at the last house
        if self.__virtualBoard[self.player-1][self.lastDecision-1]-1 == 0:
            # print("MOVE AGAIN")
            return self.move(self.player, self.lastDecision)

        # empty in own house
        elif self.turn == self.player:
            # print("END IN OWN HOUSE")
            self.__virtualBoard[0][self.lastDecision -
                                   1] += self.__virtualBoard[1][self.lastDecision-1]
            self.__virtualBoard[1][self.lastDecision-1] = 0
            # print('End Board', self.__virtualBoard)
            # print("")
            return self.__virtualBoard

        # empty in enemy house
        else:
            # print('END IN ENEMY HOUSE')
            # print('End Board', self.__virtualBoard)
            # print("")
            return self.__virtualBoard

    def updateMax1(self):
        rule = 0
        if self.nomor == 0:
            rule = 1
        else:
            rule = 2

        self.turn = rule
        self.__max1 = []
        self.__virtualBoard = deepcopy(self.board)

        for i in range(1, self.totalNotNullHouse(rule)+1):
            # print('-----DECISION-----', i)
            # Deep copy the real board to virtualBoard
            self.__virtualBoard = deepcopy(self.board)
            # self.totalNotNullHouse(1)
            notNullHouseMax = self.notNull(rule, i)

            # get Virtual Board from moving a marble house
            newMax = self.setNewDataIndex(notNullHouseMax)
            newMax.append(self.move(1, notNullHouseMax))
            newMax.append(self.__virtualBoard[0][7] - self.board[0][7])
            self.__max1.append(newMax)

        '''
        Priority Queue  
        '''
        # test = PriorityQueue()
        # test.put([110, "test"])
        # test.put([20, "test"])
        # print(test.get())
        # print(test)

    def updateMin1(self):
        rule = 0
        if self.nomor == 0:
            rule = 2
        else:
            rule = 1

        self.turn = rule
        self.__warehouseMax = []
        self.__warehouseMin = []
        self.__delta = []
        self.__index = []

        # Loop for all Max
        for max1Index in range(0, len(self.__max1)):

            # tiap"nya
            # Dicari hasil papan dari move tiap lubang
            self.__min1 = []

            # Mencoba tiap langkah kalau lubang tidak kosong
            for langkahCoba in range(1, 8):
                self.__virtualBoard = deepcopy(self.__max1[max1Index][1])
                # Memastika isi lubang tidak kosong
                langkahCoba = self.notNull(rule, langkahCoba)
                # print("HRSNYA G NOL", self.__virtualBoard, langkahCoba)
                # print("pilihan", langkahCoba)
                # print("isi" ,self.__virtualBoard[1][langkahCoba-1])
                if langkahCoba == 999:
                    self.__min1.append(self.__virtualBoard)
                else:
                    self.__min1.append(self.move(rule, langkahCoba))

            # Dicari nilai delta terbesar dari self.__min1
            biggestIndex = 0
            biggestValue = -100
            for mencariTerbesar in range(0, len(self.__min1)):
                if self.__virtualBoard[0][7] - self.__virtualBoard[1][7] > biggestValue:
                    biggestIndex = mencariTerbesar

            # Print isi __min1
            # for indexMin1 in range (0, len(self.__min1)):
            #     print('ISI MIN1', self.__min1[indexMin1])

            self.__warehouseMax.append(self.__min1[biggestIndex][0][7])
            self.__warehouseMin.append(self.__min1[biggestIndex][1][7])
            self.__index.append(self.__max1[max1Index][0])
        # print(len(self.__warehouseMax))

        for indexWarehouseMaxMin in range(0, len(self.__warehouseMax)):
            self.__delta.append(
                self.__warehouseMax[indexWarehouseMaxMin] - self.__warehouseMin[indexWarehouseMaxMin])

    # Just for change the
    def start(self):
        self.updateMax1()
        self.updateMin1()

        # Search the biggest delta
        theBestIndex = 0
        theBestValue = -98

        for index in range(0, len(self.__delta)):
            if self.__delta[index] > theBestValue:
                theBestIndex = index
        return self.__index[theBestIndex]

    # Count not number of not null house
    def totalNotNullHouse(self, player):
        theTotal = 0
        for i in range(0, 7):
            # print(self.__virtualBoard)
            if self.__virtualBoard[player-1][i] != 0:
                theTotal += 1
        # print('LOOK AT THIS', self.__virtualBoard)
        # print("theTOTAL", theTotal)
        return theTotal

    # To skip null house
    def notNull(self, player, house):
        if self.totalNotNullHouse(player) != 0:
            if self.checkHouse(player, house):
                house += 1
                if house > 7:
                    house -= 7
                return self.notNull(player, house)
            else:
                return house-1
        else:
            return 999

    # Return 0 if null
    def checkHouse(self, player, house):
        if self.__virtualBoard[player-1][house-1] == 0:
            return 1
        else:
            return 0

    # Pemain beraksi
    # Gunakan informasi dari papan untuk memilih nomor
    # lubang mulai
    def main(self, papan):
        self.board = papan
        lubang = papan.getLubang(self.nomor)

        # Update Prediction Board
        self.predictionBoard = []
        newBoard = papan.getLubang(0)
        newBoard.append(papan.getTabungan(0))
        self.predictionBoard.append(newBoard)
        newBoard = papan.getLubang(1)
        newBoard.append(papan.getTabungan(1))
        self.predictionBoard.append(newBoard)
        # Copy board dari pa eko ke virtual board
        self.board = deepcopy(self.predictionBoard)
        # self.__virtualBoard = deepcopy(self.board)

        # Execute AI Decision
        bestDecision = self.start()
        self.totalTurn += 1

        return bestDecision
