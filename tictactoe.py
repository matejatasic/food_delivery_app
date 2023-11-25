"""
Tic Tac Toe Player
"""

import math
import copy


X = "X"
O = "O"
EMPTY = None

X_WON = 1
O_WON = -1
TIE = 0


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
    x = 0
    o = 0

    for row in board:
        for column in row:
            if column == X:
                x += 1
            if column == O:
                o += 1
    
    return O if x > o else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()

    for row_index, row in enumerate(board):
        for column_index, column in enumerate(row):
            if column == EMPTY:
                result.add((row_index, column_index))

    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result = copy.deepcopy(board)

    for row_index, row in enumerate(board):
        for column_index, column in enumerate(row):
            if row_index == action[0] and column_index == action[1]:
                if column != EMPTY:
                    raise Exception("This is not a valid action")
                current_player = player(board)
                result[row_index][column_index] = current_player

    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check winner diagonally
    if (
        board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != EMPTY
    ):
        return board[0][0]
    if (
        board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[2][0] != EMPTY
    ): 
        return board[2][0]

    for index in range(len(board)):
        # check winner vertically
        if (
            board[0][index] == board[1][index] 
            and board[1][index] == board[2][index]
            and board[0][index] != EMPTY
        ):
            return board[0][index]
        
        #check winner horizontally
        if (
            board[index][0] == board[index][1]
            and board[index][1] == board[index][2]
            and board[index][0] != EMPTY
        ):
            return board[index][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    for row in board:
        for column in row:
            if column == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_result = winner(board)

    if not winner_result:
        return TIE

    return X_WON if winner_result == X else O_WON 


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    board_copy = copy.deepcopy(board)

    if terminal(board_copy):
        return None
    
    last_action = [None]

    is_maximizing_player = True if player(board) == X else False
    minimax_score = handle_minimax(board, is_maximizing_player, last_action)
    
    return last_action[0]

def handle_minimax(board, is_maximizing_player, last_action):
    if terminal(board):
        return utility(board)
    
    if is_maximizing_player:
        value = -1
        
        for action in actions(board):
            current_result = result(board, action)
            minimax_value = handle_minimax(current_result, False, last_action)            

            if minimax_value > value:
                value = minimax_value
                last_action[0] = action
        
        return value
    
    value = 2

    for action in actions(board):
        current_result = result(board, action)
        minimax_value = handle_minimax(current_result, True, last_action)
        
        if minimax_value < value:
                value = minimax_value
                last_action[0] = action

    return value
