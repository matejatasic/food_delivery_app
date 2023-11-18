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

    possible_optimal_results = get_possible_optimal_results(board)     
    print(possible_optimal_results)
        
    return (2, 1)

def get_possible_optimal_results(board):
    possible_actions = actions(board)
    possible_results = []
    current_player = player(board)
    results = []
    possible_optimal_results = []
    
    for action in possible_actions:
        possible_results.append(result(board, action))
    
    for current_result in possible_results:
        if terminal(current_result):
            scenario_winner = winner(current_result)
            outcome = determine_outcome(current_player, scenario_winner)
            
            results.append((action, outcome))
            
            continue
        
        possible_optimal_results += get_possible_optimal_results(current_result)
    
    index_of_most_optimal_result = 0
    smallest_outcome = 2

    if not len(possible_optimal_results):
        return results

    for index, possible_optimal_result in enumerate(possible_optimal_results):
        if possible_optimal_result[1] < smallest_outcome:
            smallest_outcome = possible_optimal_result[1]
            index_of_most_optimal_result = index

    return possible_optimal_results[index_of_most_optimal_result]

def determine_outcome(current_player, actual_winner):
    if not actual_winner:
        return 0
    
    return 1 if current_player == actual_winner else -1
