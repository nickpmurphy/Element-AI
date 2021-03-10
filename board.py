#!/usr/bin/python3
# Authors: Daniel Nicholson-Gardner, Denzel Clarke, and Nick Murphy
# Created On: October 28, 2020
# Description:
# board.py contains the board and its state.
import math
from numpy import random as rn
import sys

class Board():
    # We want to be able to build a board from another board so
    # allowing Board to be initalized with current board_spots and current tiles
    def __init__(self, currboardSpots=None, currtiles=None, playerTurn=None):
        self.playerTurn = -1  # Initalized as nothing
        self.boardSpaces = {}
        self.tiles = []
        self.gameisnotOver = True
        self.validmove = []
        # Added in self.player1_position and self.player2_position for use of tracking where the players are without running issue of messing up dictionary~D.C.
        self.player1_position = (5, 6)
        self.player2_position = (7, 6)
        # Adding windJumpLength for the purpose of fixing a mental jump later
        self.windJumpLength = 0
        # adding in a tracker for the double earth locations
        self.mountainLoc = []
        # Water Tracker For finding the longestt chain of waters and storing their locations
        self.waterChain1 = []
        self.waterChain2 = []
        self.waterToggle = 0
        if not (currboardSpots is None):
            self.boardSpaces = currboardSpots.copy()
        else:
            # Initalizing the 11X11 grid held in the board_spots dictionary
            # key = tuple(x,y)
            # value  = string
            # Added in player initial positions~D.C.
            for i in range(1, 12):
                for j in range(1, 12):
                    if(i == 5 and j == 6):
                        self.boardSpaces[(i, j)] = "1"
                    elif(i == 7 and j == 6):
                        self.boardSpaces[(i, j)] = "2"
                    else:
                        self.boardSpaces[(i, j)] = "-"

        if not (currtiles is None):
            self.tiles = currtiles.copy()
        else:
            # Intiallizing all the tiles if none was given
            # 120 tiles of 4 elements
            elements = ["W", "E", "A", "F"]
            for j in elements:
                for i in range(30):
                    self.tiles.append(j)
        if not (playerTurn is None):
            self.playerTurn = playerTurn

    # clearBoard does as it says and clears the board to the previous state
    def clearBoard(self):
        for i in range(1, 12):
            for j in range(1, 12):
                self.boardSpaces[(i, j)] = "-"



    # Returns a list of tuples of the dictionary
    @property
    def getEmptySpaces(self):
        emptySpaces = []
        for key in self.boardSpaces:
            if self.boardSpaces[key] == "-":
                emptySpaces.append((key, self.boardSpaces[key]))
        return emptySpaces

    @property
    def getTiles(self):  # getTiles delivers the list of current tiles available to pull  
        return self.tiles
    @property
    def game_not_over(self):
        if(self.validMoves(self.playerLocation(self.playerTurn)) == [self.playerLocation(self.playerTurn)]):
            return False
        else:
            return True

    def getLoc(self):
        if(self.playerTurn == 1):
            return self.player1_position
        else:
            return self.player2_position
    # repr makes a string representation of the board
    def __repr__(self):
        represent = '\n\n-------------------------------------------------------------------\n'
        temp = list(self.boardSpaces.values())  # temp list of values
        for i in range(11):
            values = temp[i * 11:((i + 1) * 11)]  # every row of the board
            for value in values:
                represent += '|  {}  '.format(value)
            represent += '| {}\n'.format(i + 1)
            represent += '-------------------------------------------------------------------\n'
        represent += '   1     2     3     4     5     6     7     8     9     10    11  \n'

        numTilesLeft = len(self.tiles)
        W = self.tiles.count("W")
        E = self.tiles.count("E")
        A = self.tiles.count("A")
        F = self.tiles.count("F")
        represent += f'Number tiles left: {numTilesLeft} Water: {W} Earth: {E} Air: {A} Fire: {F}\n'
        return represent



    # clearTiles just reinitlizes the tiles

    def clearTiles(self):
        elements = ["W", "E", "A", "F"]
        self.tiles = []
        for i in range(30):
            for j in elements:
                self.tiles.append(j)

    # drawTiles generates a random array with size of numberwanted
    def drawTiles(self, numberwanted):
        tilesList = []
        if(numberwanted > 0):
            for tiles in range(int(numberwanted)):
                if(self.tiles == []):
                    break
                x = rn.randint(0, len(self.tiles)-1)
                tilesList.append(self.tiles.pop(x))
        return tuple(tilesList)


    def playerLocation(self, playernum):
        if playernum == 1:
            return self.player1_position
        else:
            return self.player2_position
    # validMoves checks the spaces surrounding the player and returns all spaces with valid moves (Air exceptions will come after writing the Air rules)
    def validMoves(self, location):
        self.validmove =[]
        xposition = location[0]
        yposition = location[1]
        #print(self.playerLocation(self.playerTurn))
        for i in range(-1, 2):
            for j in range(-1, 2):
                if(self.boardSpaces.get((xposition+i, yposition+j), "Off Board") == "-"):
                    self.validmove.append((xposition+i, yposition+j))
                elif("A" in self.boardSpaces.get((xposition+i, yposition+j), "Off Board")):
                    self.windJumpLength = len(self.boardSpaces.get((xposition+i, yposition+j)))
                    if(self.airMove(location, (xposition+i,yposition+j))!="Off Board"):
                        self.validmove.append(self.airMove(location, (xposition+i,yposition+j)))
                        self.windJumpLength = 0
                    else:
                        self.windJumpLength = 0
                elif("E" in self.boardSpaces.get((xposition+i, yposition), "Off Board") and "E" in self.boardSpaces.get((xposition, yposition+j), "Off Board")):
                    if(self.earthMove((xposition+i, yposition)) != True):
                        self.validmove.append((xposition+i, yposition+j))
                elif(self.boardSpaces.get((xposition+i,yposition+j),"Off Board") == self.playerLocation(self.playerTurn)):
                    self.validmove.append((xposition+i, yposition+j))

        if(self.validmove != []):
            return self.validmove
        else:
            return [location]
    # move takes a the player and their number of moves (1-5) and recursively iterates through asking the player to enter coordinates for each move after providing the list of available spaces

    def move(self, player, moves):
        validslots = self.validMoves(self.playerLocation(player))
        if(validslots != True):
            print("Your valid moves are:")
            print(validslots)
            # should be no greater than 8 ~D.C.
            new_location_index = int(input(
                "Please enter the index of the location you would like to choose: "))
            new_location = validslots[new_location_index]
            if(player == 1):
                self.boardSpaces[self.player1_position] = "-"
                self.boardSpaces[new_location] = "1"
                self.player1_position = new_location
            else:
                self.boardSpaces[self.player2_position] = "-"
                self.boardSpaces[new_location] = "2"
                self.player2_position = new_location
            if(moves > 1):
                moves = moves-1
                self.validmove.clear()
                print(self.validmove)
                return self.move(player, moves)
            else:
                self.validmove.clear()
                print(self.validmove)
                self.validmove.clear()
                return "Finished"


    
    def placeTile(self, point, tile, playerType):
        npoint = point
#        print(self.tiles)
#        print(tile)
        self.tiles.remove(tile)
        if(self.boardSpaces[npoint] == "-"):
            self.boardSpaces[npoint] = tile
            if(tile == "F"):
                self.elementFire(npoint)
            elif(tile == "W"):
                self.elementWater(npoint, playerType)
        elif(self.replaceCheck(self.boardSpaces[npoint], tile) == True):
            self.boardSpaces[npoint] = tile
            if(tile == "F"):
                self.elementFire(npoint)
            elif(tile == "W"):
                self.elementWater(npoint, playerType)
        elif(tile in self.boardSpaces.get(npoint, "Off Board") and (tile != "F" or tile != "W")):
            if(len(self.boardSpaces[npoint]) < 2):
                self.boardSpaces[npoint] = self.boardSpaces.get(npoint) + tile
                if(tile == "E"):
                    self.mountainLoc = self.mountainLoc + [npoint]
            else:
                if(tile != "E" and len(self.boardSpaces[npoint])<4):
                    self.boardSpaces[npoint] = self.boardSpaces.get(npoint) + tile 
    # Element rules
    def airMove(self, access, airPosition):
        # Takes the position of the accessing player, and the position of the air element and will check the tiles on the opposite side
        # playerPosition = access
        # airPosition = elemPosition
        # When called semi recursively access becomes the position of the first element and position to check becomes the air position
        xPlayer = access[0]
        yPlayer = access[1]
        xAir = airPosition[0]
        yAir = airPosition[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if(xAir == xPlayer+i and yAir == yPlayer+j):
                    positionToCheck = (xAir+i, yAir+j)
                    if("A" in self.boardSpaces.get(positionToCheck, "Off Board")):
                        self.windJumpLength =self.windJumpLength + len(self.boardSpaces.get(positionToCheck))
                        return self.airMove(airPosition, positionToCheck)
                else:
                    positionToMove= (xAir+self.windJumpLength, yAir+self.windJumpLength)
                    if("-" in self.boardSpaces.get(positionToMove, "Off Board")):
                        return positionToMove
                    elif("Off Board" in self.boardSpaces.get(positionToMove, "Off Board")):
                        return "Off Board"
                    else:
                        return "Off Board"

    def earthMove(self, earthPosition):
        # Takes the position of the earth tile and recursively checks through the spaces around it to see if they are earth and in the mountainLoc variable
        if self.mountainLoc != None and earthPosition in self.mountainLoc:
            return False
        else:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    npoint = (earthPosition[0]+i, earthPosition[1]+j)
                    if("E" in self.boardSpaces.get(npoint, "Off Board") and i!=0 and j!=0):
                        return self.earthMove(npoint)
                    else:
                        return True

    def elementFire(self, firePlaced):
        # Takes the position of the fire placed and checks the y and x axis for spreading
        for i in range(-1, 2):
            for j in range(-1, 2):
                npointXCheck = (firePlaced[0]+i, firePlaced[1])
                npointYCheck = (firePlaced[0], firePlaced[1]+j)

                if(i != 0):
                    if("F" in self.boardSpaces.get(npointXCheck, "Off Board")):
                        # store the i value and recur through the board on the y-axis to check where the next non-fire space is
                        # and whether or not that space is able to have a fire tile placed on it
                        self.elementFireSpread(npointXCheck, i,"x")
                if(j != 0):
                    if("F" in self.boardSpaces.get(npointYCheck, "Off Board")):
                        self.elementFireSpread(npointYCheck, j, "y")

    def elementFireSpread(self, fireLocation, direction, axis):
        # Takes the direction accessed and the location of the current tile and checks along the corresponding axis for the next non-fire space to see if fire can be placed there
        if(axis == "x"):
            npoint = (fireLocation[0]+direction, fireLocation[1])
            if("F" in self.boardSpaces.get(npoint, "Off Board")):
                self.elementFireSpread(npoint, direction, axis)
            elif("-" in self.boardSpaces.get(npoint, "Off Board") or "A" in self.boardSpaces.get(npoint, "Off Board")):
                self.boardSpaces[npoint] = "F"
                for tiles in range(len(self.tiles)):
                    if self.tiles[tiles] == "F":
                        self.tiles.pop(tiles)
                        break

        elif(axis == "y"):
            npoint = (fireLocation[0], fireLocation[1]+direction)
            if("F" in self.boardSpaces.get(npoint, "Off Board")):
                self.elementFireSpread(npoint, direction, axis)
            elif("-" in self.boardSpaces.get(npoint, "Off Board") or "A" in self.boardSpaces.get(npoint, "Off Board")):
                self.boardSpaces[npoint] = "F"
                for tiles in range(len(self.tiles)):
                    if self.tiles[tiles] == "F":
                        self.tiles.pop(tiles)
                        break


# aimove: given a tuple and integer updates the board dictionary and updates playernum

    def aiMove(self, point, playernum):
        if(playernum == 1):
            self.boardSpaces[self.player1_position] = "-"
            self.boardSpaces[point] = "1"
            self.player1_position = point
        else:
            self.boardSpaces[self.player2_position] = "-"
            self.boardSpaces[point] = "2"
            self.player2_position = point


    def elementWater(self, waterPlaced, playerType):
        # Needs to find the longest line from the point placed and call the waterMove with that counter
        for i in range(-1, 2):
            npointXCheck = (waterPlaced[0]+i, waterPlaced[1])
            npointYCheck = (waterPlaced[0], waterPlaced[1]+i)
#            print("printing npointXCheck")
#            print(npointXCheck)
#            print("printing npointYCheck")
#            print(npointYCheck)
            if(i != 0):
                if("W" in self.boardSpaces.get(npointXCheck, "Off Board")):
                    self.elementWaterCounter(npointXCheck, i, "x")
                if("W" in self.boardSpaces.get(npointYCheck, "Off Board")):
                    self.elementWaterCounter(npointYCheck, i, "y")
        if(playerType == "Manual"):
            self.waterMove(waterPlaced)
        else:
            direction_to_travel_index = 0
            self.waterMoveAI(waterPlaced, direction_to_travel_index)

    def elementWaterCounter(self, waterLocation, direction, axis):
        # counting the waters to determine the longest water chain and getting a list of the water tile locations for purpose of making the moves
        if(self.waterToggle == 0):
            if(axis == "x"):
                npoint = (waterLocation[0]+direction, waterLocation[1])
                self.waterChain1.append(npoint)
                if("W" in self.boardSpaces.get(npoint, "Off Board")):
                    self.elementWaterCounter(npoint, direction, axis)
                self.waterToggle = 1
                
            elif(axis == "y"):
                npoint = (waterLocation[0], waterLocation[1]+direction)
                self.waterChain1.append(npoint)
                if("W" in self.boardSpaces.get(npoint, "Off Board")):
                    self.elementWaterCounter(npoint, direction, axis)
                self.waterToggle = 1
        else:
            if(axis == "x"):
                npoint = (waterLocation[0]+direction, waterLocation[1])
                self.waterChain2.append(npoint)
                if("W" in self.boardSpaces.get(npoint, "Off Board")):
                    self.elementWaterCounter(npoint, direction, axis)
            elif(axis == "y"):
                npoint = (waterLocation[0], waterLocation[1]+direction)
                self.waterChain2.append(npoint)
                if("W" in self.boardSpaces.get(npoint, "Off Board")):
                    self.elementWaterCounter(npoint, direction, axis)
            if(len(self.waterChain2) > len(self.waterChain1)):
                self.waterChain1 = []
                self.waterChain1 = self.waterChain2
            self.waterToggle = 0
            self.waterChain2 = []

    def waterMove(self, waterPlaced):
        # Moves the water chain
        while(len(self.waterChain1) > 0):
            direction_to_travel = input(
                "Please enter the number corresponding to the direction you want the chain to move: \n 0. Left\n 1. Up\n 2. Right\n 3. Down\n")
            if("0" in direction_to_travel and self.replaceCheck((waterPlaced[0]-1, waterPlaced[1]), "W")):
                newWater = (waterPlaced[0]-1, waterPlaced[1])
                self.waterChain2.append(newWater)
                self.boardSpaces[self.waterChain1[-1]] = "-"
                self.waterChain1.pop()
            elif("1" in direction_to_travel and self.replaceCheck((waterPlaced[0], waterPlaced[1]+1), "W")):
                newWater = (waterPlaced[0], waterPlaced[1]+1)
                self.waterChain2.append(newWater)
                self.boardSpaces[self.waterChain1[-1]] = "-"
                self.waterChain1.pop()
            elif("2" in direction_to_travel and self.replaceCheck((waterPlaced[0]+1, waterPlaced[1]), "W")):
                newWater = (waterPlaced[0]+1, waterPlaced[1])
                self.waterChain2.append(newWater)
                self.boardSpaces[self.waterChain1[-1]] = "-"
                self.waterChain1.pop()
            elif("3" in direction_to_travel and self.replaceCheck((waterPlaced[0], waterPlaced[1]-1), "W")):
                newWater = (waterPlaced[0], waterPlaced[1]-1)
                self.waterChain2.append(newWater)
                self.boardSpaces[self.waterChain1[-1]] = "-"
                self.waterChain1.pop()
            else:
                print("You have attempted to make an invalid move, please select a different path")
        if(self.waterChain2 != []):
            for i in range(len(self.waterChain2)):
                self.boardSpaces[self.waterChain2[i]] = "W"
            self.waterChain2 = []

    # The element replacements rule method takes an element in the form of a single character string and
    # the location it is trying to be placed at and will return True if the replacement is valid and False otherwise
    def replaceCheck(self, location, element):
        if(self.boardSpaces.get(location, "Off Board") == "F" and element == "W"):
            return True
        elif("A" in self.boardSpaces.get(location, "Off Board") and element == "F"):
            return True
        elif("E" in self.boardSpaces.get(location, "Off Board") and element == "A" and self.earthMove(location)):
            return True
        elif(self.boardSpaces.get(location, "Off Board") == "W" and element == "E"):
            return True
        elif(self.boardSpaces.get(location, "Off Board") == "-"):
            return True
        else:
            return False

    # AI MOVE SECTION:
    # For the two methods that require user input they are modified slightly to take the input as part of the call

    def waterMoveAI(self, waterPlaced, direction_to_travel):
        # Moves the water chain
        directional_list = [0,1,2,3]
        if(self.waterChain1 != []):
            while(len(self.waterChain1) > 0):
                if(directional_list[direction_to_travel] == 0):
                    newWater = (waterPlaced[0]-1, waterPlaced[1])
                if(directional_list[direction_to_travel] == 1):
                    newWater = (waterPlaced[0], waterPlaced[1]+1)
                if(directional_list[direction_to_travel] == 2):
                    newWater = (waterPlaced[0]+1, waterPlaced[1])
                if(directional_list[direction_to_travel] == 3):
                    newWater = (waterPlaced[0], waterPlaced[1]-1)
                if("-" in self.boardSpaces.get(newWater,"Not on Board")):
                    self.waterChain2.append(newWater)
                    self.boardSpaces[self.waterChain1[0]] = "-"
                    self.waterChain1.pop(0)
                else:
                    direction_to_travel_new = direction_to_travel
                    if direction_to_travel <3:
                            direction_to_travel_new = direction_to_travel+1
                            direction_to_travel = direction_to_travel_new
                    else:
                        break
            for i in range(len(self.waterChain2)):
                self.boardSpaces[self.waterChain2[i]] = "W"
            self.waterChain2 = []

    def resetPlayerLocation(self, player, location):
        if player == 1:
            self.player1_position = location
        else:
            self.player2_position = location