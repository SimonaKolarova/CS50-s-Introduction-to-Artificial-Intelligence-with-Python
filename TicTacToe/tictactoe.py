"""
Tic Tac Toe Player
"""

import math
import copy
from  itertools import chain 

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

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_num = 0
    o_num = 0

    for i in range(len(board)):
        x_num += board[i].count(X)
        o_num += board[i].count(O)
    
    if x_num > o_num:
        return O
    else:
        return X
   
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_list = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_list.add((i, j))

    return actions_list

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Move not valid")

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    X_win = [X,X,X]
    O_win = [O,O,O]

    # Horizontal win
    if X_win in (board[0], board[1], board[2]):
        return X
    if O_win in (board[0], board[1], board[2]):
        return O

    # Vertical win
    if X_win in (([item[0] for item in board]),([item[1] for item in board]),([item[2] for item in board])):
        return X
    if O_win in (([item[0] for item in board]),([item[1] for item in board]),([item[2] for item in board])):
        return O

    # Diagonal win
    if X_win in (([board[0][0], board[1][1], board [2][2]]), ([board[0][2], board[1][1], board [2][0]])):
        return X
    if O_win in (([board[0][0], board[1][1], board [2][2]]), ([board[0][2], board[1][1], board [2][0]])):
        return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    if EMPTY not in chain(*board): 
        return True

    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    
    if winner(board) == O:
        return -1
    
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    alpha = float('-inf')
    beta = float('inf')

    def maximizer(board):
        if terminal(board):
            return utility(board)
        
        alpha = float('-inf')
        nonlocal beta

        for action in actions(board):
            alpha = max(alpha, minimizer(result(board, action)))
            if alpha > beta:
                break

        return alpha

    def minimizer(board):
        if terminal(board):
            return utility(board)
        
        nonlocal alpha
        beta = float('inf')

        for action in actions(board):
            beta = min(beta, maximizer(result(board, action)))
            if beta < alpha:
                break
            
        return beta

    if terminal(board):
        return None

    if player(board) == X:
        alpha = maximizer(board)
        for action in actions(board):
            if alpha == minimizer(result(board, action)):
                return action            
                
    if player(board) == O:
        beta = minimizer(board)
        for action in actions(board):
            if beta == maximizer(result(board, action)):
                return action