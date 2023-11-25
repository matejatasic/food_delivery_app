import tictactoe as ttt

def test_is_X_players_turn():
    board = [[ttt.O, ttt.EMPTY, ttt.EMPTY],
            [ttt.EMPTY, ttt.EMPTY, ttt.EMPTY],
            [ttt.EMPTY, ttt.EMPTY, ttt.EMPTY]]
    player = ttt.player(board)
    
    assert player == ttt.X

def test_is_O_players_turn():
    board = [[ttt.X, ttt.EMPTY, ttt.EMPTY],
            [ttt.EMPTY, ttt.EMPTY, ttt.EMPTY],
            [ttt.EMPTY, ttt.EMPTY, ttt.EMPTY]]
    player = ttt.player(board)
    
    assert player == ttt.O

def test_actions_returning_appropriate_result():
    board = [[ttt.EMPTY, ttt.X, ttt.O],
            [ttt.O, ttt.X, ttt.X],
            [ttt.X, ttt.EMPTY, ttt.O]]
    expexted_result = set()
    expexted_result.add((0, 0))
    expexted_result.add((2, 1))
    expexted_result = list(expexted_result)
    result = list(ttt.actions(board))

    assert expexted_result[0] == result[0]
    assert expexted_result[1] == result[1]

def test_result_returning_appropriate_result_when_action_is_valid():
    board = [[ttt.EMPTY, ttt.X, ttt.O],
            [ttt.O, ttt.X, ttt.X],
            [ttt.X, ttt.EMPTY, ttt.O]]
    action = (0, 0)

    result = ttt.result(board, action)

    assert result[0][0] == ttt.O

def test_result_returning_raising_exception_when_action_is_invalid():
    board = [[ttt.EMPTY, ttt.X, ttt.O],
            [ttt.O, ttt.X, ttt.X],
            [ttt.X, ttt.EMPTY, ttt.O]]
    action = (0, 1)

    try:
        result = ttt.result(board, action)
        assert 1 == 0
    except:
        assert 1 == 1

def test_winner_returning_adequate_winner_when_winner_wins_diagonally():
    board = [[ttt.O, ttt.EMPTY, ttt.X],
            [ttt.O, ttt.X, ttt.EMPTY],
            [ttt.X, ttt.O, ttt.X]]
    
    winner = ttt.winner(board)

    assert winner == ttt.X

def test_winner_returning_adequate_winner_when_winner_wins_horizontally():
    board = [[ttt.O, ttt.EMPTY, ttt.O],
            [ttt.X, ttt.X, ttt.X],
            [ttt.O, ttt.O, ttt.X]]
    
    winner = ttt.winner(board)

    assert winner == ttt.X

def test_winner_returning_adequate_winner_when_winner_wins_vertically():
    board = [[ttt.O, ttt.EMPTY, ttt.O],
            [ttt.O, ttt.X, ttt.X],
            [ttt.O, ttt.X, ttt.X]]
    
    winner = ttt.winner(board)

    assert winner == ttt.O

def test_winner_returning_none_when_no_winner_exists():
    board = [[ttt.O, ttt.EMPTY, ttt.EMPTY],
            [ttt.O, ttt.X, ttt.EMPTY],
            [ttt.X, ttt.O, ttt.X]]
    
    winner = ttt.winner(board)

    assert winner == None

def test_terminal_returning_true_when_winner_exists():
    board = [[ttt.O, ttt.EMPTY, ttt.X],
            [ttt.O, ttt.X, ttt.EMPTY],
            [ttt.X, ttt.O, ttt.X]]
    
    is_terminal = ttt.terminal(board)

    assert is_terminal == True

def test_terminal_returning_false_when_winner_does_not_exist():
    board = [[ttt.O, ttt.EMPTY, ttt.EMPTY],
            [ttt.O, ttt.X, ttt.EMPTY],
            [ttt.X, ttt.O, ttt.X]]
    
    is_terminal = ttt.terminal(board)

    assert is_terminal == False

def test_utility_returns_1_when_X_wins():
    board = [[ttt.O, ttt.EMPTY, ttt.X],
            [ttt.O, ttt.X, ttt.EMPTY],
            [ttt.X, ttt.O, ttt.X]]
    
    utility = ttt.utility(board)

    assert utility == ttt.X_WON

def test_utility_returns_minus_1_when_O_wins():
    board = [[ttt.O, ttt.X, ttt.X],
            [ttt.X, ttt.O, ttt.EMPTY],
            [ttt.O, ttt.X, ttt.O]]
    
    utility = ttt.utility(board)

    assert utility == ttt.O_WON

def test_utility_returns_0_when_is_tie():
    board = [[ttt.O, ttt.X, ttt.X],
            [ttt.X, ttt.O, ttt.O],
            [ttt.O, ttt.X, ttt.X]]
    
    utility = ttt.utility(board)

    assert utility == ttt.TIE

def test_minimax_returns_the_most_optimal_action_when_exists():
    board = [[ttt.EMPTY, ttt.X, ttt.O],
            [ttt.O, ttt.X, ttt.EMPTY],
            [ttt.X, ttt.EMPTY, ttt.O]]
    
    minimax_action = ttt.minimax(board)

    assert minimax_action == (2, 1)

test_is_X_players_turn()
test_is_O_players_turn()
test_actions_returning_appropriate_result()
test_result_returning_appropriate_result_when_action_is_valid()
test_result_returning_raising_exception_when_action_is_invalid()
test_winner_returning_adequate_winner_when_winner_wins_diagonally()
test_winner_returning_adequate_winner_when_winner_wins_horizontally()
test_winner_returning_adequate_winner_when_winner_wins_vertically()
test_winner_returning_none_when_no_winner_exists()
test_terminal_returning_true_when_winner_exists()
test_terminal_returning_false_when_winner_does_not_exist()
test_utility_returns_1_when_X_wins()
test_utility_returns_minus_1_when_O_wins()
test_utility_returns_0_when_is_tie()
test_minimax_returns_the_most_optimal_action_when_exists()