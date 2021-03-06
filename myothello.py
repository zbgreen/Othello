#Zachary Green

from othello import *

#previous version of my code to test against
from old import *

class Nutello(othello_player):
    #  This will be called once at the beginning of the game, after
    #  a few random moves have been made.  Boardstate is the initial
    #  boardstate for the game, totalTime is the total amount of time
    #  (in seconds) in the range 60-1800 that your player will get for
    #  the game.  For our tournament, I will generally set this to 300.
    #  color is one of Black or White (which are just constants defined
    #  in the othello.py file) saying what color the player will be
    #  playing.
    def initialize(self, boardstate, totalTime, color):
        print("Initializing", self.name)
        self.mycolor = color
        pass;

    # This should return the utility of the given boardstate.
    # It can access (but not modify) the to_move and _board fields.
    def calculate_utility(self, boardstate):
        """
        Calculates the corners (see if corner can be taken), legal (current
        player moves available), potential mobility (amount of empty spaces
        around opponent pieces), and advantage (current piece advantage over
        opponent). Returns a weighted sum of the heuristics.
        """
        corners = self.check_corners(boardstate)
        legal = len(boardstate.calculate_legal_moves())
        mobility = self.get_potential_mobility(boardstate)
        advantage = self.mycount_difference(boardstate)
        return (2 * corners) + legal + (1.25 * mobility) + (.5 * advantage)

    def alphabeta_parameters(self, boardstate, remainingTime):
        # This should return a tuple of (cutoffDepth, cutoffTest, evalFn)
        # where any (or all) of the values can be None, in which case the
        # default values are used:
        #        cutoffDepth default is 4
        #        cutoffTest default is None, which just uses cutoffDepth to
        #            determine whether to cutoff search
        #        evalFn default is None, which uses your boardstate_utility_fn
        #            to evaluate the utility of board states.

        #switch to depth 2 if less than 1 minute remains and more than 30
        #spaces remain
        if remainingTime < 61 and self.get_empty_spaces(boardstate) > 30:
            return (2, None, None)
        #switch to depth 2 if less than 30 secs remain and more than 20
        #spaces remain
        elif remainingTime < 30 and self.get_empty_spaces(boardstate) > 20:
            return (2, None, None)
        #switch to depth 2 if less than 10 secs remain and more than 10
        #spaces remain
        elif remainingTime < 10 and self.get_empty_spaces(boardstate) > 10:
            return (2, None, None)
        #attempt depth 4
        else:
            return (4,None, None)

    def mycount_difference(self, boardstate):
        """
        Returns the difference between class's pieces and the opponent.
        """
        return (boardstate._board.count(self.mycolor) -
                boardstate._board.count(opponent(self.mycolor)))

    def get_potential_mobility(self, boardstate):
        """
        Determine the potential mobility by determining how many opponent
        pieces have adjacent empty spaces. Searches spaces 11-89 to avoid
        uselessly checking outer spaces.
        """
        potential_mobility = 0
        board = boardstate._board
        for space in range(11, 90):
            if board[space] == opponent(self.mycolor):
                if board[space] + 1 == Empty:
                    potential_mobility += 1
                if board[space] - 1 == Empty:
                    potential_mobility += 1
                if board[space] + 10 == Empty:
                    potential_mobility += 1
                if board[space] - 10 == Empty:
                    potential_mobility += 1
                if board[space] + 9 == Empty:
                    potential_mobility += 1
                if board[space] + 11 == Empty:
                    potential_mobility += 1
                if board[space] - 9 == Empty:
                    potential_mobility += 1
                if board[space] - 11 == Empty:
                    potential_mobility += 1
        return potential_mobility

    def check_corners(self, boardstate):
        """
        Checks if a corner can be taken. Potential corners increase utility
        """
        board = boardstate._board
        #print(board)
        utility = 0
        if board[11] == self.mycolor:
            utility = utility + 25
        if board[18] == self.mycolor:
            utility = utility + 25
        if board[82] == self.mycolor:
            utility = utility + 25
        if board[89] == self.mycolor:
            utility = utility + 25
        return utility

    def get_empty_spaces(self, boardstate):
        """
        Gets the # of empty spaces from the boardstate.
        """
        empty = 0
        #Checks 11-89 to skip the outer spaces.
        for space in range(11, 90):
            if boardstate._board[space] == 0:
                empty += 1
        return empty

def count_difference(boardstate):
    return (boardstate._board.count(boardstate.to_move)
            - boardstate._board.count(opponent(boardstate.to_move)))

#play_othello(Othello(), 300, Nutello("Nutello"), old("old"))
#start_graphical_othello_game(Nutello("Nutello"), othello_player("Fred"))
