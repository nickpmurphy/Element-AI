#!/usr/bin/python3
# Authors: Daniel Nicholson-Gardner, Denzel Clarke, and Nick Murphy
# Created On: October 28, 2020
# Description:
# game.py contains the functions necessary to run the game

# this class was just for me to see if my functions were doing what I intended
import random
import unittest
import player
from board import Board


class testingBoard(unittest.TestCase):
    testDict1 = {(1, 5): "nf",
                 (2, 5): "nf",
                 (3, 2): "nf",
                 (4, 5): "nf",
                 (3, 7): "1",
                 (7, 8): "nf",
                 (6, 5): "nf",
                 }
    testDict2 = {
        (1, 5): "nf",
        (2, 5): "nf",
        (3, 2): "nf",
        (4, 5): "nf",
        (3, 7): "1",
        (7, 8): "nf",
        (6, 5): "nf",
        (23, 12): "nf",
        (23, 5): "nf",
        (43, 2): "nf",
        (23, 6): "nf",
        (3, 43): "1",
        (123, 8): "nf",
        (234, 5): "nf",
    }
    bd0 = Board()
    bd1 = Board(testDict1)
    bd2 = Board(testDict2)

    def testgetEmpty(self):
        self.assertEqual(len(self.bd0.getEmptySpaces), 11 * 11)
        self.assertEqual(len(self.bd1.getEmptySpaces), 6)
        self.assertEqual(len(self.bd2.getEmptySpaces), 12)

class playGame():
    def __init__(self, p1, p2, board):
        self.p1 = p1
        self.p2 = p2
        self.board = board

    def runGame(self):
        print("This is the board")
        print(bd)
        self.board.playerTurn = 1
        while (self.board.game_not_over):
            if self.board.playerTurn == 1:
                p1.makeMove()
                self.board.playerTurn = 2
                print(bd)
            elif self.board.playerTurn == 2:
                p2.makeMove()
                self.board.playerTurn = 1
                print(bd)


if __name__ == "__main__":
    bd = Board()
    print("Hi there welcome to Element!\n")
    modeChoice = input("Please select the mode you want to see:\n 1. Human VS AI \n 2. AI VS AI \n 3. Human VS Human")
    if("1" in modeChoice):
        aiChoice = input(
            "Please enter the number corresponding to the level of difficulty of AI you want to play against: \n 0. suicidal\n 1. popSuicidal\n 2. offensive\n 3. popOffensive\n 4. popDefensive\n 5. defensive\n 6. BlendedOpponent\n 7. popBlendedOppponent\n 8. BlendedSelf\n 9. popBlendedSelf\n 10. Random\n 11. popRandom\n 12. rotating\n 13. chaotic\n 14. moreChaotic\n 15. MAXIMUMCHAOS\n Your choice:  ")
        humanplayernum = random.randint(1, 2)
        aiplayernum = 0

        if humanplayernum == 1:
            aiplayernum = 2
            p1 = player.manualPlayer(humanplayernum, bd)
            p2 = player.aiPlayer(aiplayernum, bd, aiChoice)
        else:
            aiplayernum = 1
            p2 = player.manualPlayer(humanplayernum, bd)
            p1 = player.aiPlayer(aiplayernum, bd, aiChoice)
        g = playGame(p1, p2, bd)
        g.runGame()
    if("2" in modeChoice):
        aiChoice1 = input(
            "Please enter the number corresponding to the level of difficulty of the first AI: \n 0. suicidal\n 1. popSuicidal\n 2. offensive\n 3. popOffensive\n 4. popDefensive\n 5. defensive\n 6. BlendedOpponent\n 7. popBlendedOppponent\n 8. BlendedSelf\n 9. popBlendedSelf\n 10. Random\n 11. popRandom\n 12. rotating\n 13. chaotic\n 14. moreChaotic\n 15. MAXIMUMCHAOS\n Your choice:  ")
        aiChoice2 = input(
            "Please enter the number corresponding to the level of difficulty of the second AI: \n 0. suicidal\n 1. popSuicidal\n 2. offensive\n 3. popOffensive\n 4. popDefensive\n 5. defensive\n 6. BlendedOpponent\n 7. popBlendedOppponent\n 8. BlendedSelf\n 9. popBlendedSelf\n 10. Random\n 11. popRandom\n 12. rotating\n 13. chaotic\n 14. moreChaotic\n 15. MAXIMUMCHAOS\n Your choice:  ")
        ai1playernum = random.randint(1, 2)
        print(ai1playernum)
        if ai1playernum == 1:
            ai2playernum = 2
            p1 = player.aiPlayer(ai1playernum, bd, aiChoice1)
            p2 = player.aiPlayer(ai2playernum, bd, aiChoice2)
        else:
            ai2playernum = 1
            p2 = player.aiPlayer(ai1playernum, bd, aiChoice2)
            p1 = player.aiPlayer(ai2playernum, bd, aiChoice1)
        g = playGame(p1, p2, bd)
        g.runGame()
    if("3" in modeChoice):
        humanplayer1num = random.randint(1, 2)
        humanplayer2num = 0

        if humanplayernum == 1:
            humanplayer2num = 2
            p1 = player.manualPlayer(humanplayer1num, bd)
            p2 = player.manualPlayer(humanplayer2num, bd)
        else:
            humanplayer2num = 1
            p2 = player.manualPlayer(humanplayer1num, bd)
            p1 = player.manualPlayer(humanplayer2num, bd)
        g = playGame(p1, p2, bd)
        g.runGame()