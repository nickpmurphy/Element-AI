#!/usr/bin/python3
# Authors: Daniel Nicholson-Gardner, Denzel Clarke, and Nick Murphy
# Created On: October 28, 2020
# Description:
# player.py contains the different player modes

from board import Board
from numpy import random as rn
import itertools
from itertools import permutations, product
import math
# manualPlayer is a class that takes player number


class manualPlayer():
    def __init__(self, playernum, board):
        self.playernum = playernum
        self.board = board
        self.playerType = "Manual"

    @property
    def getPlayerNum(self):
        return self.playernum

    # makeMove calls the move function in Board and draws tiles and asks users wehre it should be placed
    def makeMove(self):
        ask = int(input("How many tiles do you want?"))
        print(ask)
        tiles = self.board.drawTiles(ask)
        for tile in tiles:
            currTile = tile
            instr = input(
                "Where would you like to put {} type (x, y):  ".format(currTile))
            inList = [float(n) for n in instr.split(',')]
            point = tuple(inList)
            self.board.placeTile(point, currTile, self.playerType)
        self.board.move(self.playernum, 5 - ask)
#        if self.board.gameisnotOver == False:
#            print("IS GETTING HIT")


class Node():
    def __init__(self, value, tilesDrawn=0, nodeType=0, children=[]):
        self.tilesDrawn = tilesDrawn or 0
        self.value = value
        self.nodeType = nodeType or 0
        self.children = children or []

    # add does as it says and adds a new board state
    def add(self, newNode):
        self.children.append(newNode)


# the aiPlayer
class aiPlayer():
    def __init__(self, playernum, board, heuristic):
        self.playernum = playernum
        self.board = board
        self.heuristic = heuristic
        # Stuff for the misc. heuristics
        self.play = 0

        # tiles_and_moves is used to store the placements of the tile combinations and the moves that are made the key is formatted as ((tile combination), (location of the final position))
        self.tiles_and_moves = {}
        self.currentBestKey = ()
        self.BestKeysandTypes = []
        # moves is used to store the possible locations that the player can get to
        self.drawedtiles = None
        self.playerType = "AI"
        # offensiveHeuristic takes a board and returns and integer
        # that represents how many more tiles to win, this heuristic is very baseline
        # and assumes the player stays still
    # Three baseline heuristics: Attack, Defend, Suicide

    def offensiveHeuristic(self):
        # Exclusively tries to block the opponent
        if(self.playernum == 1):
            if(self.board.validMoves(self.board.playerLocation(2)) == list(self.board.playerLocation(2))):
                return 8
            else:
                self.board.validmove.clear()
                #print(len(self.board.validMoves(self.board.playerLocation(self.playernum))))
                return 8 - len(self.board.validMoves(self.board.playerLocation(2)))
        else:
            if(self.board.validMoves(self.board.playerLocation(1)) == list(self.board.playerLocation(1))):
                return 8
            else:
                self.board.validmove.clear()
                #print(len(self.board.validMoves(self.board.playerLocation(self.playernum))))
                return 8 - len(self.board.validMoves(self.board.playerLocation(1)))

    def suicidalHeuristic(self):
        # Tries to suicide itself
        if(self.board.validMoves(self.board.playerLocation(self.playernum)) == list(self.board.playerLocation(self.playernum))):
            return 8
        else:
            self.board.validmove.clear()
            return 8 - len(self.board.validMoves(self.board.playerLocation(self.playernum)))

    def defensiveHeuristic(self):
        # Exclusively tries to keep itself alive
        if(self.board.validMoves(self.board.playerLocation(self.playernum)) == list(self.board.playerLocation(self.playernum))):
            return -8
        else:
            return 0 + len(self.board.validMoves(self.board.playerLocation(self.playernum)))

    # A pair of blended heuristics based on how they prioritize: Keep Self Alive vs. Block Opponent
    def blendedFavorSelfHeuristic(self):
        # A blended heuristic favoring protecting self over blocking opponent

        if(self.playernum == 1):
            if(self.board.validMoves(self.board.playerLocation(2)) == list(self.board.playerLocation(2))):
                return 8
            elif(self.board.validMoves(self.board.playerLocation(1)) == list(self.board.playerLocation(1))):
                return -8
            else:
                return len(self.board.validMoves(self.board.playerLocation(1))) - len(self.board.validMoves(self.board.playerLocation(2)))
        else:
            if(self.board.validMoves(self.board.playerLocation(1)) == list(self.board.playerLocation(1))):
                return 8
            elif(self.board.validMoves(self.board.playerLocation(2)) == list(self.board.playerLocation(2))):
                return -8
            else:
                return len(self.board.validMoves(self.board.playerLocation(2))) - len(self.board.validMoves(self.board.playerLocation(1)))

    def blendedFavorOpponentHeuristic(self):
        # A blended heuristic favoring attacking the opponent over protecting itself
        if(self.playernum == 1):
            if(self.board.validMoves(self.board.playerLocation(2)) == list(self.board.playerLocation(2))):
                return 8
            elif(self.board.validMoves(self.board.playerLocation(1)) == list(self.board.playerLocation(1))):
                return -8
            return len(self.board.validMoves(self.board.playerLocation(2))) - len(self.board.validMoves(self.board.playerLocation(1)))
        else:
            if(self.board.validMoves(self.board.playerLocation(1)) == list(self.board.playerLocation(1))):
                return 8
            elif(self.board.validMoves(self.board.playerLocation(2)) == list(self.board.playerLocation(2))):
                return -8
            return len(self.board.validMoves(self.board.playerLocation(1)))-len(self.board.validMoves(self.board.playerLocation(2)))

    # A heuristic that plays a random other heuristic
    def randomHeuristic(self):
        # Plays a random Heuristic from the following
        # Offensive, Suicidal, Defensive, Blended (Prioritizing Self), Blended (Prioritizing Opponent)
        choiceToPlay = rn.randint(0, 5)
        if(choiceToPlay == 0):
            return self.offensiveHeuristic()
        if(choiceToPlay == 1):
            return self.suicidalHeuristic()
        if(choiceToPlay == 2):
            return self.defensiveHeuristic()
        if(choiceToPlay == 3):
            return self.blendedFavorSelfHeuristic()
        if(choiceToPlay == 4):
            return self.blendedFavorOpponentHeuristic()
    # a set of pass or play heuristics based on the preceding heuristics

    def passOrPlayOffensiveHeuristic(self):
        # A heuristic which decides randomly whether to play a board location or pass over it
        played = rn.randint(0, 2)
        if(played == 0):
            return -1
        else:
            return self.offensiveHeuristic()

    def passOrPlaySuicidalHeuristic(self):
        played = rn.randint(0, 2)
        if(played == 0):
            return -1
        else:
            return self.suicidalHeuristic()

    def passOrPlayDefensiveHeuristic(self):
        played = rn.randint(0, 2)
        if(played == 0):
            return -1
        else:
            return self.defensiveHeuristic()

    def passOrPlayBlendedSelfHeuristic(self):
        played = rn.randint(0, 2)
        if(played == 0):
            return -1
        else:
            return self.blendedFavorSelfHeuristic()

    def passOrPlayBlendedOpponentHeuristic(self):
        played = rn.randint(0, 2)
        if(played == 0):
            return -1
        else:
            return self.blendedFavorOpponentHeuristic()

    def passOrPlayRandomHeuristic(self):
        # A P.o.P. version of the Random Heuristic
        played = rn.randint(0, 2)
        if(played == 0):
            return -1
        else:
            return self.randomHeuristic()
    # Miscellaneous Heuristics

    def rotatingHeuristic(self):
        # Rotates through the initial 12 heuristics
        # (Offense, Suicide, Defense, Blended Self, Blended Opponent, Random
        #  popOffense, popSuicide, popDefense, popBlendedSelf, popBlendedOpponent, popRandom)
        if(self.play == 0):
            self.play = self.play+1
            return self.offensiveHeuristic()
        if(self.play == 1):
            self.play = self.play+1
            return self.suicidalHeuristic()
        if(self.play == 2):
            self.play = self.play+1
            return self.defensiveHeuristic()
        if(self.play == 3):
            self.play = self.play+1
            return self.blendedFavorSelfHeuristic()
        if(self.play == 4):
            self.play = self.play+1
            return self.blendedFavorOpponentHeuristic()
        if(self.play == 5):
            self.play = self.play+1
            return self.randomHeuristic()
        if(self.play == 6):
            self.play = self.play+1
            return self.passOrPlayOffensiveHeuristic()
        if(self.play == 7):
            self.play = self.play+1
            return self.passOrPlaySuicidalHeuristic()
        if(self.play == 8):
            self.play = self.play+1
            return self.passOrPlayDefensiveHeuristic()
        if(self.play == 9):
            self.play = self.play+1
            return self.passOrPlayBlendedSelfHeuristic()
        if(self.play == 10):
            self.play = self.play+1
            return self.passOrPlayBlendedOpponentHeuristic()
        if(self.play == 11):
            self.play == 0
            return self.passOrPlayRandomHeuristic()

    def chaoticHeuristic(self):
        # Like Rotating but RANDOM
        randomChoice = rn.randint(0, 12)
        if(randomChoice == 0):
            return self.offensiveHeuristic()
        if(randomChoice == 1):
            return self.suicidalHeuristic()
        if(randomChoice == 2):
            return self.defensiveHeuristic()
        if(randomChoice == 3):
            return self.blendedFavorSelfHeuristic()
        if(randomChoice == 4):
            return self.blendedFavorOpponentHeuristic()
        if(randomChoice == 5):
            return self.randomHeuristic()
        if(randomChoice == 6):
            return self.passOrPlayOffensiveHeuristic()
        if(randomChoice == 7):
            return self.passOrPlaySuicidalHeuristic()
        if(randomChoice == 8):
            return self.passOrPlayDefensiveHeuristic()
        if(randomChoice == 9):
            return self.passOrPlayBlendedSelfHeuristic()
        if(randomChoice == 10):
            return self.passOrPlayBlendedOpponentHeuristic()
        if(randomChoice == 11):
            return self.passOrPlayRandomHeuristic()

    def evenMoreChaoticHeuristic(self):
        # Randomly plays Rotating and Chaotic
        CHAOSFACTOR = rn.randint(0, 2)
        if(CHAOSFACTOR == 0):
            return self.rotatingHeuristic()
        if(CHAOSFACTOR == 1):
            return self.randomHeuristic()

    def CHAOSHeuristic(self):
        # gives the board a random value between -999999 and 999999 (inclusive)
        return rn.randint(-999999, 1000000)

    # THE FOLLOWING METHODS ARE HELPER FUNCTIONS FOR THE SUCCESSOR --------------'''

    # linearmovement given number of moves returns a list of  (x,y) tuples representing the board x,y place
    #  CP = Current Position
    #           x-n, y+n        x, y+n       x+n, y+n
    #           x-n, y            x                x+n, y
    #           x-n, y-n        x, y-n        x+n, y-n

    def movementChecker(self, nMoves, location):
        if nMoves == 1:
            return self.board.validMoves(location)

        moves = [(a, b) for a, b in product(list(range(location[0]-nMoves+1, location[1] + nMoves-1)), list(range(location[0]-nMoves+1, location[1]+nMoves-1)))]
        temp = []
        for move in moves:
            if int(move[0]) >= 1 and int(move[0]) <= 11 and int(move[1]) >= 1 and int(move[1]) <=11:
                temp.extend(self.board.validMoves(move))
        return list(set(temp))

    # aiChooseTile: given a list of tile returns a list of tuples of the tile and pl
    def aiChooseTile(self, listTiles):
        tempPlaces = self.board.validMoves(
            self.board.playerLocation(self.playernum))
#        print("Printing temp Places on line 321")
        # print(listTiles)
        # print(len(tempPlaces))
        tilePlace = []
        if(tempPlaces == True):
            return True
        for tile in listTiles:
            if(tempPlaces != []):
                i = rn.randint(0, len(tempPlaces))
                place = tempPlaces[i]
                tilePlace.append((place, tile))
                tempPlaces.pop(i)
        return tilePlace
    # --------------END OF HELPER FUNCTIONS-------------'''

##
# for draw in range(0,5):
#    expectedValue = self.expectedVal(draw)
#    if expectedValue > maxExpectedVal:
#        maxExpectedVal = expectedValue
#
#   p = factorial(len(tiles))*math.prod([bag.count(tiles[i])/len(bag) for i range(len(tiles)))
#   Probabilities^V
#   f = lambda n : math.prod(list(range(1,n+1)))
#
#   Child = self.board.copy()
#   set(tuple([tuple(sorted(x)) for x in permutations(bag,draw)]))
#   helper
#   function(tuple of tiles):


# make copy board
# score board
# checks to see if that score is higher than the current highest
# checks board to see if self kill is thing
# add score to sum
# tick counter
# (length of permutations of tiles) * P(of the tiles drawn) *(s/c)
#    return score
    def newExpectimax(self, tree):
        # look children in tree
        for child in tree.children:
            print(child.value)
            evList = [child.value for child in tree.children]
        return evList.index(max(evList))
        # choose node with highest expected value


    def evFunction(self, ntiles):
        if (self.board.gameisnotOver == True):
                nTiles = ntiles
                nMove = 5 - nTiles
                oldTiles = self.board.tiles.copy()  # getting a copy of the current tiles
                # getting a copy of the current board spots
                oldBoardSpots = self.board.boardSpaces.copy()
                current_maxValue = 0
                value = 0
                counter = 0
                if(nTiles != 0):
                    tileRep = []
                    for tile in oldTiles:
                        if tile == "W" and len(tileRep)<4:
                            tileRep.append(tile)
                        elif tile == "E" and len(tileRep)<8:
                            tileRep.append(tile)
                        elif tile == "A" and len(tileRep)<12:
                            tileRep.append(tile)
                        elif tile == "F" and len(tileRep)<16:
                            tileRep.append(tile)
                    tileCombos = list(set(tuple([tuple(sorted(x)) for x in permutations(tileRep, nTiles)])))
                    # getting places to put tiles
                    tilePlaces = list(set(tuple([tuple(x) for x in permutations(self.board.validMoves(self.board.getLoc()), nTiles)])))
                    # creating a set of  lists of tuples of tiles and lcoations
                    placesTilesProduct = []
                    for x in tileCombos:
                        for j in range(len(tilePlaces)):
                            placesTilesProduct.append((x,tilePlaces[j]))
                    for tile_places in placesTilesProduct:
                        current_maxValue = 0
                        tile = tile_places[0]
                        tilemove = tile_places[1]
                        for coordIndex in range(nTiles):
                            self.board.placeTile(tilemove[coordIndex], tile[coordIndex], self.playerType)
                        moves = self.movementChecker(nMove, self.board.playerLocation(self.playernum))
                        for move in moves:
                            counter = counter + 1
                            playermove = move
                            self.board.aiMove(playermove, self.playernum)
                            newValue = 0
                            if("2" in self.heuristic and len(self.heuristic) < 2):  # Dif. 2
                                newValue = self.offensiveHeuristic()
                                value = value + newValue
                            if("5" in self.heuristic):  # Dif. 5
                                newValue = self.defensiveHeuristic()
                                value = value + newValue
                            if("0" in self.heuristic and len(self.heuristic) < 2):  # Dif. 0
                                newValue = self.suicidalHeuristic()
                                value = value + newValue
                            if("9" in self.heuristic):  # Dif. 9
                                newValue = self.blendedFavorSelfHeuristic()
                                value = value + newValue
                            if("6" in self.heuristic):  # Dif. 6
                                newValue = self.blendedFavorOpponentHeuristic()
                                value = value + newValue
                            if("10" in self.heuristic):  # Dif. 10
                                newValue = self.randomHeuristic()
                                value = value + newValue
                            if("3" in self.heuristic and len(self.heuristic) < 2):  # Dif. 3
                                newValue = self.passOrPlayOffensiveHeuristic()
                                value = value + newValue
                            if("1" in self.heuristic and len(self.heuristic) < 2):  # Dif. 1
                                newValue = self.passOrPlaySuicidalHeuristic()
                                value = value + newValue
                            if("4" in self.heuristic and len(self.heuristic) < 2):  # Dif. 4
                                newValue = self.passOrPlayDefensiveHeuristic()
                                value = value + newValue
                            if("8" in self.heuristic):  # Dif. 8
                                newValue = self.passOrPlayBlendedSelfHeuristic()
                                value = value + newValue
                            if("7" in self.heuristic):  # Dif. 7
                                newValue = self.passOrPlayBlendedOpponentHeuristic()
                                value = value + newValue
                            if("11" in self.heuristic):  # Dif. 11
                                newValue = self.passOrPlayRandomHeuristic()
                                value = value + newValue
                            if("12" in self.heuristic):  # Dif. 12
                                newValue = self.rotatingHeuristic()
                                value = value + newValue
                            if("13" in self.heuristic):  # Dif. 13
                                newValue = self.chaoticHeuristic()
                                value = value + newValue
                            if("14" in self.heuristic):  # Dif. 14
                                newValue = self.evenMoreChaoticHeuristic()
                                value = value + newValue
                            if("15" in self.heuristic):  # Dif. 15
                                newValue = self.CHAOSHeuristic()
                                value = value + newValue
                            newkey = (tile, move)
                            if (newValue > current_maxValue):
                                current_maxValue = newValue
                                placeholderKeys = list(self.tiles_and_moves.keys())
                                for keys in placeholderKeys:
                                    if(newkey[0] == keys[0]):
                                        del self.tiles_and_moves[self.currentBestKey]
                                        self.tiles_and_moves[newkey] = self.board.boardSpaces.copy()                                    
                                self.tiles_and_moves[newkey] = self.board.boardSpaces.copy()
                                self.currentBestKey = newkey
                                self.board.boardSpaces = oldBoardSpots.copy()
                                self.board.tiles = oldTiles.copy()
                                self.board.playerturn = self.playernum
                                for key in self.board.boardSpaces:
                                    if self.board.boardSpaces[key] == "1":
                                        self.board.resetPlayerLocation(self.playernum, key)
                                    elif self.board.boardSpaces[key] == "2":
                                        self.board.resetPlayerLocation(self.playernum, key)
                            else:
                                self.board.boardSpaces = oldBoardSpots.copy()
                                self.board.tiles = oldTiles.copy()
                                self.board.playerturn = self.playernum
                                for key in self.board.boardSpaces:
                                    if self.board.boardSpaces[key] == "1" and self.playernum == 1:
                                        self.board.resetPlayerLocation(self.playernum, key)
                                    if self.board.boardSpaces[key] == "2" and self.playernum == 2:
                                        self.board.resetPlayerLocation(self.playernum, key)
                    return value/counter
                else:
                    for newState in self.movementChecker(nMove, self.board.playerLocation(self.playernum)):
                        counter = counter + 1
                        playermove = newState
                        newValue = 0
                        if("2" in self.heuristic and len(self.heuristic) < 2):  # Dif. 2
                            newValue = self.offensiveHeuristic()
                            value = value + newValue
                        if("5" in self.heuristic):  # Dif. 5
                            newValue = self.defensiveHeuristic()
                            value = value + newValue
                        if("0" in self.heuristic and len(self.heuristic) < 2):  # Dif. 0
                            newValue = self.suicidalHeuristic()
                            value = value + newValue
                        if("9" in self.heuristic):  # Dif. 9
                            newValue = self.blendedFavorSelfHeuristic()
                            value = value + newValue
                        if("6" in self.heuristic):  # Dif. 6
                            newValue = self.blendedFavorOpponentHeuristic()
                            value = value + newValue
                        if("10" in self.heuristic):  # Dif. 10
                            newValue = self.randomHeuristic()
                            value = value + newValue
                        if("3" in self.heuristic and len(self.heuristic) < 2):  # Dif. 3
                            newValue = self.passOrPlayOffensiveHeuristic()
                            value = value + newValue
                        if("1" in self.heuristic and len(self.heuristic) < 2):  # Dif. 1
                            newValue = self.passOrPlaySuicidalHeuristic()
                            value = value + newValue
                        if("4" in self.heuristic and len(self.heuristic) < 2):  # Dif. 4
                            newValue = self.passOrPlayDefensiveHeuristic()
                            value = value + newValue
                        if("8" in self.heuristic):  # Dif. 8
                            newValue = self.passOrPlayBlendedSelfHeuristic()
                            value = value + newValue
                        if("7" in self.heuristic):  # Dif. 7
                            newValue = self.passOrPlayBlendedOpponentHeuristic()
                            value = value + newValue
                        if("11" in self.heuristic):  # Dif. 11
                            newValue = self.passOrPlayRandomHeuristic()
                            value = value + newValue
                        if("12" in self.heuristic):  # Dif. 12
                            newValue = self.rotatingHeuristic()
                            value = value + newValue
                        if("13" in self.heuristic):  # Dif. 13
                            newValue = self.chaoticHeuristic()
                            value = value + newValue
                        if("14" in self.heuristic):  # Dif. 14
                            newValue = self.evenMoreChaoticHeuristic()
                            value = value + newValue
                        if("15" in self.heuristic):  # Dif. 15
                            newValue = self.CHAOSHeuristic()
                            value = value + newValue
                        newkey = ((), newState)
                        if (newValue > current_maxValue):
                            current_maxValue = newValue
                            placeholderKeys = list(self.tiles_and_moves.keys())
                            for keys in placeholderKeys:
                                if(newkey[0] == keys[0]):
                                    del self.tiles_and_moves[self.currentBestKey]
                                    self.tiles_and_moves[newkey] = self.board.boardSpaces.copy()                                    
                            self.tiles_and_moves[newkey] = self.board.boardSpaces.copy()
                            self.currentBestKey = newkey
                            self.board.boardSpaces = oldBoardSpots.copy()
                            self.board.tiles = oldTiles.copy()
                            self.board.playerturn = self.playernum
                            for key in self.board.boardSpaces:
                                if self.board.boardSpaces[key] == "1" and self.playernum == 1:
                                    self.board.resetPlayerLocation(self.playernum, key)
                                elif self.board.boardSpaces[key] == "2" and self.playernum == 2:
                                    self.board.resetPlayerLocation(self.playernum, key)
                        else:
                            self.board.boardSpaces = oldBoardSpots.copy()
                            self.board.tiles = oldTiles.copy()
                            self.board.playerturn = self.playernum
                            for key in self.board.boardSpaces:
                                if self.board.boardSpaces[key] == "1" and self.playernum == 1:
                                    self.board.resetPlayerLocation(self.playernum, key)
                                elif self.board.boardSpaces[key] == "2" and self.playernum == 2:
                                    self.board.resetPlayerLocation(self.playernum, key)
                    return value/counter
                
    # def expectedVal(self, tilesDrawn):
    #     EV of board = 1/n (sum hueristic(board))
    #     return sum(Probability_of_Draw * expectedValue(allpossibleboards))

    def makeMove(self):
        self.board.validMoves(self.board.playerLocation(self.playernum))
        if(self.board.gameisnotOver == False):
            return False
        else:
            if (self.board.gameisnotOver == True):
                tree = Node(0)
                for i in range(0, 5):
                    expectedValue = self.evFunction(i)
                    if(expectedValue == 0.0):
                        tree.add(Node(0, i, 1, []))
                    else:
                        tree.add(Node(expectedValue, i, 1, []))
                ntiles = self.newExpectimax(tree)
                tileList = tuple(sorted(self.board.drawTiles(ntiles)))
                key = ()
                for keys in list(self.tiles_and_moves.keys()):
                    if keys[0] == tileList:
                        key = keys
                try:
                    self.board.boardSpaces = self.tiles_and_moves[key].copy()
                except KeyError:
                    return False
                self.tiles_and_moves.clear()
            else:
                return False


'''
        The code that follows is for use by the AI class.
        These methods modulize the code to allow use to change the difficulty
        of our AI.This way we can create various forms of diffculty.
'''

#                *
# [0,1, value=(probabilty shit), {combinations of tiles drawn} ]-----1-----1-----1----1
# [0, 2, value= max of the moves children{}]    {}    {}     {}  {}

# [{combination of tiles placed and how they are placed} 3 value created the movement
