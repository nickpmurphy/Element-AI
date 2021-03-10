# Element

This is a python implimentation of the board game Element.

## How To Run This Game

To run the program download game.py, board.py, and player.py all into the same folder

Now to actually play the game you will need to run game.py in either your terminal or in your IDE.

## Making a Local Copy

To make a copy of the repo on your machine just type:
`git clone https://github.iu.edu/dnn1/Element.git`

## Committing Edits

To prevent us from ruinning the master branch all we have to follow a few steps:

1. Before making any changes to the code always make sure you are in a separate branch from master. You can do this by the following commands:

`git branch new-branch`

`git checkout new-branch`

You may also use:
`git checkout -b new-branch`

2. Commit changes to said branch
3. Make Pull request on Github.com and someone will approve of them.

Sticking to these rules will allow us to not step on each other's code.

## About Board.py

board.py initalizes the board object and contains mutiple functions to aid in the implimentation of the game:

# Key Things to Note:

1.  The Board.boardSpaces is a dictionary with the key and value pair like (x,y: object-on-space. For Instance: (1,1): 'W', this means that there is Water on space 1, 1.
