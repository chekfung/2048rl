'''
Title: 2048 Hackathon Project using Reinforcement Learning
Author: Jason Ho, Jeremy Chen, Steven Cheung, Hwai-Liang Tung
Date: January 26th - 27th 2019
'''

# Python library imports
import random
import numpy as np
from collections import defaultdict


class Board:
    '''
    Board is a class method that creates the board that is used for the 2048
    game using numpy arrays to display. In addition, its methods allow for
    full functionality of the game board.

    As its own discrete object, its possible to use it for our reinforcement
    learning object, or as a game by itself that a user can play.
    '''

    def __init__(self, gameOver=False, score=0):
        '''
        Default initialiser which just sets the actual numpy representation
        of the board to be four by four, sets score to be zero and starts the
        game.
        '''
        self.board = np.zeros((4, 4))
        self.gameOver = gameOver
        self.score = score

    def addTile(self):
        '''
        addTile is a method that functions as the randomized part of the 2048
        game that adds a 2 or 4 tile each time that the user moves the board.
        '''
        listOfEmptys = []

        # Double for loop that allows for each element to be checked to see if
        # deemed an empty space, meaning that it has a value of zero.
        for i, x in enumerate(self.board):
            for j, y in enumerate(x):
                if y == 0:
                    listOfEmptys.append((i, j))

        # Finds random place to put the tile by looking at all empty spaces
        element = listOfEmptys[random.randint(0, len(listOfEmptys)-1)]

        # Determines tile value; 90% to be 2, 10% to be 4
        if random.random() < 0.9:
            num = 2
        else:
            num = 4

        # Adds element to the internal board stored in the class variables
        self.board[element[0], element[1]] = num

    def rotateBoardLeft(self):
        '''
        rotateBoardLeft rotates the board ninety degrees to the left in the
        counterclockwise dimension. This method solely exists such that it is
        easier to do computations with the board when combining tiles for score.

        Also, this method makes it easier to permute the board in different
        directions when using the different commands.
        '''
        self.board = np.rot90(self.board)

    def rotateBoardRight(self):
        '''
        rotateBoardRight literally rotates the entire numpy array board to the
        right, or clockwise ninety degrees. Again, this will be used as a
        helper function since it is easier to understand what this is doing
        rather than just having the numpy syntax for rotating the board.
        '''
        self.board = np.rot90(self.board, 3)

    def moveAndUpdateRowLeft(self, j):
        '''
        moveAndUpdateRowLeft is a method that essentially works on one row at
        a time. It takes one row and then moves all of the nonzero digits to the
        left into a new list, l. It then appends zeroes to the end to make up
        for the difference and make sure that the board is still the same square
        that it was beforehand.

        Parameters
        ----------
        j : int
            Represents the row number that the method is called upon in the
            game board array.

        Returns
        ----------
        l : list
            Represents the new row where entire row is moved to the left
        '''
        l = []

        # Iterates through each item in the row and if not zero, appends to l
        for i in range(0, self.board.shape[1]):
            if self.board[j, i] != 0:
                l.append(self.board[j, i])

        # Adds zeroes to the end of l until same size as the original row length
        while len(l) < self.board.shape[1]:
            l.append(0)
        return l

    def moveAndUpdateBoardLeft(self):
        '''
        moveAndUpdateBoardLeft is a method that takes the entire board and then
        moves the board to the left. At the same time, it updates the score of
        the game session when two tiles of the same value hit each other when
        updated and moved to the left.

        In essence this is the master method that is used in order to update
        the board in every single direction.
        '''
        arrayToReturn = []

        # Loop for each row of the board
        for j in range(0, self.board.shape[0]):
            x = self.moveAndUpdateRowLeft(j)

            # Loop to go through each of the elements
            for i in range(0, self.board.shape[1]-1):
                if x[i] == x[i+1] and x[i] != 0:

                    # Fixes score and board when two of a kind touch each other
                    self.board[j, i] = 2 * x[i]
                    self.score += self.board[j, i]
                    self.board[j, i+1] = 0

                # Sets x to be the new board row
                x = self.board[j]

            # Appends the fixed row to the new array
            arrayToReturn.append(self.moveAndUpdateRowLeft(j))

        # Sets board equal to the new fixed board
        self.board = np.array(arrayToReturn)

    def moveAndUpdateBoard(self, move):
        '''
        moveAndUpdateBoard is a method that takes in the move query and then
        translates that into the board. Since everything is handled by helper
        functions defined beforehand, this part of the script is much shorter.

        Parameters
        ----------
        move : str
            Represents the move that is inputted either by the reinforcement
            learning program or the human user
        '''

        # if the user wants to move up
        if move == "Up":
            self.rotateBoardLeft()
            self.moveAndUpdateBoardLeft()
            self.rotateBoardRight()

        # if the user wants to move down
        elif move == "Down":
            self.rotateBoardRight()
            self.moveAndUpdateBoardLeft()
            self.rotateBoardLeft()

        # if the user wants to move left
        elif move == "Left":
            self.moveAndUpdateBoardLeft()

        # if the user wants to move right
        elif move == "Right":
            self.rotateBoardLeft()
            self.rotateBoardLeft()
            self.moveAndUpdateBoardLeft()
            self.rotateBoardRight()
            self.rotateBoardRight()

        # adds tile randomly after move on the board
        self.addTile()

    def availableActions(self):
        '''
        availableActions is a method that finds all of the possible moves that
        the reinforcement learning program or the user can input. Since once
        the board fills up in one direction, it is no longer possible to move
        the board in that direction.

        This method accounts for that and allows for the the correct inputs and
        can provide the correct print statements when a user tries to input
        something that is not allowed.

        Returns
        ---------
        toReturn : list of strings
            Represents the list of moves that are possible and can be used
        '''
        dimension = self.board.shape[0]
        toReturn = []

        # Checks to see if up is a valid move
        for i in range(0, dimension):
            if self.board[0, i] != 0:
                break
        else:
            toReturn.append("Up")

        # Checks to see if down is a valid move
        for i in range(0, dimension):
            if self.board[dimension-1, i] != 0:
                break
        else:
            toReturn.append("Down")

        # Checks to see if Left is a valid move
        for i in range(0, dimension):
            if self.board[i, 0] != 0:
                break
        else:
            toReturn.append("Left")

        # Checks to see if Right is a valid move
        for i in range(0, dimension):
            if self.board[i, dimension] != 0:
                break
        else:
            toReturn.append("Right")
        return toReturn

    def isOver(self):
        '''
        isOver is a method that checks whether or not the end of the game has been
        encountered, meaning that there are no spots that new tiles can be put
        and the board cannot be reduced to make space for new tiles.

        In order words, this means that there are no possible moves available.

        Returns
        -------
        over : boolean
            Represents whether or not a game is over by looking at the board; If
            there are moves that are possible, then the game is not over.
        '''
        aBoolean = False

        for j in range(0, self.board.shape[0]):
            x = self.board[j, :]
            for i in range(0, self.board.shape[1]):
                if x[i] == 0:
                    break
        else:
            aBoolean = True

        over = (self.availableActions() == [] and aBoolean)
        return over
