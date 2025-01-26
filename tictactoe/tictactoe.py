"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

# First, we define three variables: X, O, and EMPTY, to represent possible moves of the board
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    # For this problem, we’ve chosen to represent the board as a list of three lists 

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # take a board state as input, and return which player’s turn it is (either X or O).
  
    count = 0
    for row in board:
        for cell in row:
            if cell:
                count += 1

    if count%2 == 0:
        return X
    else: 
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Each action should be represented as a tuple (i, j) 
    # where i corresponds to the row of the move (0, 1, or 2) 
    # and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
    all_actions = set()
    i = 0
    for row in board:
        j = 0
        for cell in row:
            if cell == EMPTY:
                all_actions.add((i,j))
            j+=1
        i += 1
    return all_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Importantly, the original board should be left unmodified: 
    # since Minimax will ultimately require considering many different board states during its computation.
    # If action is not a valid action for the board, your program should raise an exception.
    if action is None:
        raise Exception("action can not be None")
    
    i,j = action
    if board[i][j] is not None:
        raise Exception("cell is already occupied")
    
    if i >= 3 or j >= 3 or i < 0 or j < 0:
        raise Exception("action out of bounds")
    
    cur_player = player(board)
    new_board = deepcopy(board)
    new_board[i][j] = cur_player
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
    # If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the function should return None
    condition_1 = [X,X,X]
    condition_2 = [O,O,O]

    for row in board:
        if row == condition_1:
            return X
        elif row == condition_2:
            return O
        
    for j in range(0,3):
        col = [row[j] for row in board]
        if col == condition_1:
            return X
        elif col == condition_2:
            return O
        
    diag = []
    anti_diag = []
    for i in range(0,3):
        diag.append(board[i][i])
        anti_diag.append(board[i][2-i])
    if diag == condition_1 or anti_diag == condition_1:
        return X
    elif diag == condition_2 or anti_diag == condition_2:
        return O
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == None:
        return 0
    elif winner(board) == X:
        return 1
    else:
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is a terminal board, the minimax function should return None.
    if terminal(board):
        return None
    
    cur_player = player(board)

    def max_value(board):
        if terminal(board):
            return utility(board), None
        else:
            v = float('-inf')
            opt_action = None
            for action in actions(board):
                new_board = result(board, action)
                min_v = min_value(new_board)[0]
                if min_v > v:
                    v = min_v
                    opt_action = action
            return v, opt_action

    def min_value(board):
        if terminal(board):
            return utility(board), None
        else:
            v = float('inf')
            opt_action = None
            for action in actions(board):
                new_board = result(board, action)
                max_v = max_value(new_board)[0]
                if max_v < v:
                    v = max_v
                    opt_action = action
            return v, opt_action
        
    if cur_player == X:
        opt_action = max_value(board)[1]
    else:
        opt_action = min_value(board)[1]
    
    return opt_action
                

                    
                        
                

        
                      
                
                
            
            
