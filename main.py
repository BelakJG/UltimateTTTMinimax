from functools import cache
import math

def print_board(board):
    for big_row in range(3):
        for inner_row in range(3):
            output = []
            for big_col in range(3):
                b = big_row * 3 + big_col
                sub = board[b]

                for inner_col in range(3):
                    idx = inner_row * 3 + inner_col
                    cell = sub[idx]
                    output.append(str(idx + 1) if cell == "." else cell)

                if big_col != 2:
                    output.append("|")

            print(" ".join(output))

        if big_row != 2:
            print("------+-------+------")

@cache
def score_board(full_board):
    outer_board = ""
    score = 0
    for inner_board in full_board:
        result = score_inner_board(inner_board)
        if result == math.inf:
            outer_board += "X"
            score += 50000
        elif result == -math.inf:
            outer_board += "O"
            score -= 50000
        elif result == 0 and "." not in inner_board:
            outer_board += "D"
        else:
            outer_board += "."
            score += result
    return score + (score_inner_board(outer_board) * 1000)

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
        line = inner_board_string[a] + inner_board_string[b] + inner_board_string[c]
        x_count = line.count("X")
        o_count = line.count("O")
        empty = line.count(".")

        if x_count == 3:
            return math.inf
        if o_count == 3:
            return -math.inf
        if x_count == 2 and empty == 1:
            score += 20
        if o_count == 2 and empty == 1:
            score -= 20

    single_scores = [2,1,2,1,6,1,2,1,2]
    for i in range(9):
        if inner_board_string[i] == "X":
            score += single_scores[i]
        elif inner_board_string[i] == "O":
            score -= single_scores[i]
    #check draw
    if "." not in inner_board_string:
        return 0
    #no winner, game still going
    return score

def minimax(turn, outer_index, outer_board, depth = 10, alpha = -math.inf, beta = math.inf):
    score = score_board(outer_board)
    if score in (math.inf, -math.inf, 0) or depth == 0:
        return score
    valid_boards = []
    target_board_score = score_inner_board(outer_board[outer_index])
    if target_board_score not in (math.inf, -math.inf) and "." in outer_board[outer_index]:
        valid_boards = [outer_index]
    else:
        valid_boards = [i for i in range(9) if score_inner_board(outer_board[i]) not in (math.inf, -math.inf, 0)]
    if not valid_boards:
        return 0

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

def find_best(turn, board, outer_index = 0):
    best_move = {"board": board, "score": -math.inf if turn == "X" else math.inf, "played-inner": -1, "played-outer": -1}
    valid_boards = []
    target_board_score = score_inner_board(board[outer_index])
    if target_board_score not in (math.inf, -math.inf) and "." in board[outer_index]:
        valid_boards = [outer_index]
    else:
        valid_boards = [i for i in range(9) if (score_inner_board(board[i]) not in (math.inf, -math.inf) and "." in board[i])]
        print(valid_boards)
    for valid_outer in valid_boards:
        for i in range(9):
            if board[valid_outer][i] == ".":
                new_board = board[:valid_outer] + (board[valid_outer][:i] + turn + board[valid_outer][i+1:],) + board[valid_outer+1:]
                new_score = minimax("O" if turn == "X" else "X", i, new_board, 4)
                if (turn == "X" and new_score > best_move["score"]) or (turn == "O" and new_score < best_move["score"]):
                    best_move["board"] = new_board
                    best_move["score"] = new_score
                    best_move["played-inner"] = i + 1
                    best_move["played-outer"] = valid_outer + 1
    print(f"Your best move is (outer: {best_move['played-outer']}, inner: {best_move['played-inner']}, score: {best_move['score']})")
    return best_move["board"], best_move["played-inner"] - 1


if __name__ == '__main__':
    board = (".........",".........",".........",".........",".........",".........",".........",".........",".........")
    next_outer = 0
    turn = "X"
    while True:
        print_board(board)
        new_board, played_inner = find_best(turn, board, next_outer)
        if (score_board(new_board)) in (math.inf, -math.inf):
            break

        turn = "O" if turn == "X" else "X"
        if score_inner_board(new_board[played_inner]) in (math.inf, -math.inf) or "." not in new_board[played_inner]:
            next_outer = int(input("What outer board did your opponent play?: ")) - 1
        else:
            next_outer = played_inner
        op_inner = int(input("What inner board index did your opponent play?: ")) - 1
        board = new_board[:next_outer] + (new_board[next_outer][:op_inner] + turn + new_board[next_outer][op_inner+1:],) + new_board[next_outer+1:]
        turn = "O" if turn == "X" else "X"
        next_outer = op_inner
        if score_board(board) in (math.inf, -math.inf):
            break

    print(f"Player {turn} wins!")
