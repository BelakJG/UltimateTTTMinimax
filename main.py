from functools import cache
import math

def print_board(board):
    for outer_row in range(3):
        for inner_row in range(3):
            r = outer_row * 3 + inner_row
            row = board[r]

            output = []

            for big_col in range(3):
                chunk = row[big_col * 3:(big_col + 1) * 3]

                for inner_col, cell in enumerate(chunk):
                    if cell == ".":
                        index = inner_row * 3 + inner_col
                        output.append(str(index))
                    else:
                        output.append(cell)

                if big_col != 2:
                    output.append("|")

            print(" ".join(output))

        if outer_row != 2:
            print("------+-------+------")

@cache
def score_board(full_board):
    outer_board = ""
    score = 0
    for inner_board in full_board:
        result = score_inner_board(inner_board)
        if result == math.inf:
            outer_board += "X"
        elif result == -math.inf:
            outer_board += "O"
        elif result == 0:
            outer_board += "D"
        else:
            outer_board += "."
        score += result
    return score + (score_inner_board(outer_board) * 100)

@cache
def score_inner_board(inner_board_string):
    win_positions = [
        #horizontals
        (0,1,2),
        (3,4,5),
        (6,7,8),
        #columns
        (0,3,6),
        (1,4,7),
        (2,5,8),
        #diags
        (0,4,8),
        (6,4,2)
    ]
    score = 0
    for a, b, c in win_positions:
        if inner_board_string[a] not in (".", "D"):
            if inner_board_string[a] == inner_board_string[b] == inner_board_string[c]:
                return math.inf if inner_board_string[a] == "X" else -math.inf
            else:
                if inner_board_string[a] == inner_board_string[b]:
                    score += (10 if inner_board_string[a] == "X" else -10)
                if inner_board_string[a] == inner_board_string[c]:
                    score += (10 if inner_board_string[a] == "X" else -10)
                if inner_board_string[b] not in (".", "D") and inner_board_string[b] == inner_board_string[c]:
                    score += (10 if inner_board_string[b] == "X" else -10)

    #check draw
    if "." not in inner_board_string:
        return 0
    #no winner, game still going
    return score

def minimax(turn, outer_index, outer_board, depth = 10, alpha = -math.inf, beta = math.inf):
    score = score_board(outer_board)
    if score == math.inf or score == -math.inf or depth == 0:
        return score
    valid_boards = []
    if outer_board[outer_index].count(".") > 0:
        valid_boards = [outer_index]
    else:
        valid_boards = [i for i in range(9) if outer_board[i].count(".") > 0]

    for valid_outer_index in valid_boards:
        if turn == "X":
            for i in range(9):
                if outer_board[valid_outer_index][i] == ".":
                    new_full_board = outer_board[:valid_outer_index] + (outer_board[valid_outer_index][:i] + turn + outer_board[valid_outer_index][i+1:],) + outer_board[valid_outer_index + 1:]
                    alpha = max(alpha, minimax("O", i, new_full_board, depth - 1, alpha, beta))
                    if alpha >= beta:
                        return alpha
        else:
            for i in range(9):
                if outer_board[valid_outer_index][i] == ".":
                    new_full_board = outer_board[:valid_outer_index] + (
                        outer_board[valid_outer_index][:i] + turn + outer_board[valid_outer_index][i + 1:],) + outer_board[
                                         valid_outer_index + 1:]
                    beta = min(beta, minimax("X", i, new_full_board, depth - 1, alpha, beta))
                    if beta <= alpha:
                        return beta
    return alpha if turn == "X" else beta

def is_hashable(*args):
    try:
        hash(args)
        return True
    except TypeError:
        return False

if __name__ == '__main__':
    board = (".........",".........",".........",".........",".........",".........",".........",".........",".........")
    print_board(board)
    print(minimax("X", 0, board))
