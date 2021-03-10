#!/usr/bin/python3
# Authors: Daniel Nicholson-Gardner, Denzel Clarke, and Nick Murphy
# Created On: October 28, 2020
# Description:
# testingRuntime.py contains the functions necessary to run the game

# this class was just for me to see if my functions were doing what I intended
import datetime
import player
from board import Board
from game import playGame


# heuristicTime given a heuristic returns the time it took to make a move with the first
def heuristicTimeForFirstMove(heuristic):
    bd = Board(playerTurn=1)
    aiplayer1 = player.aiPlayer(1, bd, heuristic)
    manualPlayer = player.manualPlayer(2, bd)
    g = playGame(aiplayer1, manualPlayer, bd)
    start = datetime.datetime.now()
    g.p1.makeMove()
    end = datetime.datetime.now()
    time = str((end - start).total_seconds())
    return time

# aiGame given one heuristic and another returns the length of time it took to run and finish the game


def aiGame(heuristic1, heuristic2):
    bd = Board(playerTurn=1)
    aiplayer1 = player.aiPlayer(1, bd, heuristic1)
    aiplayer2 = player.aiPlayer(2, bd, heuristic2)
    g = playGame(aiplayer1, aiplayer2, bd)
    start = datetime.datetime.now()
    g.runGame()
    end = datetime.datetime.now()
    time = str((end - start).total_seconds())
    return time


# loops to gather data on all of the heuristics
choices = ["suicidal", "popSuicidal", "offensive", "popOffensive", "popDefensive", "defensive", "BlendedOpponent",
           "popBlendedOppponent", "BlendedSelf", "popBlendedSelf", "Random", "popRandom", "rotating", "chaotic", "moreChaotic", "MAXIMUMCHAOS"]


def loopThrough():
    data = "\nHeuristic |  Time (seconds)"
    battle = "\n                Heuristic            |      Time (seconds) "
    for i in range(15):
        heuristic1 = str(i)
        data += "\n{} | {}\n".format(choices[i],
                                     heuristicTimeForFirstMove(heuristic1))
        for j in range(15, 0,):
            heuristic2 = str(j)
            battle += "\n{}  vs {}    |   {}\n".format(
                choices[i], choices[j], aiGame(heuristic1, heuristic2))
    return "{}   {}".format(data, battle)


if __name__ == "__main__":
    results = open("runtimetest.txt", "w+")
    for i in range(15):
        data = loopThrough()
        string = "{}\n {}".format(i, data)
        results.write(string)
    results.close()
