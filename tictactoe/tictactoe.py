"""
Tic Tac Toe Player
"""
import copy
import math

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
    Count_x = 0
    Count_o = 0
    # Count the total number of X and O
    for row in board:
        for cell in row:
            if cell == "X":
                Count_x += 1
            elif cell == "O":
                Count_o += 1

    # Check who's turn it is
    if len(actions(board)) == 9:
        return "X"
    elif Count_x == Count_o:
        return "X"
    else:
        return "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    # Check the value of each cell if EMPTY and record the coordinates of the empty ones
    for row_idx, row in enumerate(board):
        for cell_idx, cell in enumerate(row):
            if cell == EMPTY:
                actions.add((row_idx, cell_idx))

    return actions


results_count = 0


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action is None:
        raise NotImplementedError
    else:
        row = action[0]
        cell = action[1]

    # Check if the cell is empty
    if board[row][cell] != EMPTY:
        raise Exception("Invalid move")

    # Create a new board
    board_new = copy.deepcopy(board)

    # Assign the player's symbol into the cell
    board_new[row][cell] = player(board)

    return board_new


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner_col_1 = []
    winner_col_2 = []
    winner_col_3 = []
    winner_diagonal_1 = []
    winner_diagonal_2 = []
    winner_accumulative = []

    # Check if there is a winner by row
    for idx, row in enumerate(board):
        if row.count(row[0]) == len(row):
            return row[0]
        else:
            winner_col_1.append(row[0])
            winner_col_2.append(row[1])
            winner_col_3.append(row[2])
            winner_diagonal_1.append(row[idx])
            winner_diagonal_2.append(row[2 - idx])
    # Check if the winner is in any other direction
    winner_accumulative.extend([winner_col_1, winner_col_2, winner_col_3, winner_diagonal_1, winner_diagonal_2])
    for each in winner_accumulative:
        if each.count(each[0]) == len(each):
            return each[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    elif len(actions(board)) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    current_player = player(board)

    # Check who's player turn it is
    # For every available action check what the opponent would do
    # Keep track of the utility for each action
    # return the action with the best utility

    alpha = -math.inf
    beta = math.inf

    if current_player == "X":
        best_utility = -math.inf
        for max_action in actions(board):
            action_utility = min_value(result(board, max_action), alpha, beta)
            if action_utility > best_utility:
                best_max_action = max_action
                best_utility = action_utility
            alpha = max(alpha, action_utility)
        return best_max_action
    else:
        best_utility = math.inf
        for min_action in actions(board):
            action_utility = max_value(result(board, min_action), alpha, beta)
            if action_utility < best_utility:
                best_min_action = min_action
                best_utility = action_utility
            beta = min(beta, action_utility)
        return best_min_action


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v
