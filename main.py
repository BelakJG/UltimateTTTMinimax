from functools import cache

def print_board(board_string):
    boards_array = board_string.split("/")

    for outer_row in range(3):
        for inner_row in range(3):
            r = outer_row * 3 + inner_row
            row = boards_array[r]

            output = []

            for big_col in range(3):
                chunk = row[big_col*3:(big_col+1)*3]

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
def check_winner(full_board_string):
    inner_boards = full_board_string.split("/")
    outer_board = ""
    for inner_board in inner_boards:
        result = check_inner_board_winner(inner_board)
        if result == 1:
            outer_board += "X"
        elif result == -1:
            outer_board += "O"
        elif result == 0:
            outer_board += "D"
        elif result is None:
            outer_board += "."
    return check_inner_board_winner(outer_board)

@cache
def check_inner_board_winner(inner_board_string):
    #horizontals
    for i in range(0, 7, 3):
        if (inner_board_string[0 + i] != "." and inner_board_string[0 + i] != "D") and (inner_board_string[0 + i] == inner_board_string[1 + i] == inner_board_string[2 + i]):
            return 1 if inner_board_string[0 + i] == "X" else -1
    #verticals
    for i in range(3):
        if (inner_board_string[0 + i] != "." and inner_board_string[0 + i] != "D") and (inner_board_string[0 + i] == inner_board_string[3 + i] == inner_board_string[6 + i]):
            return 1 if inner_board_string[0 + i] == "X" else -1
    #diags
    if (inner_board_string[0] != "." and inner_board_string[0] != "D") and (inner_board_string[0] == inner_board_string[4] == inner_board_string[8]):
        return 1 if inner_board_string[0] == "X" else -1
    if (inner_board_string[6] != "." and inner_board_string[6] != "D") and (inner_board_string[6] == inner_board_string[4] == inner_board_string[2]):
        return 1 if inner_board_string[6] == "X" else -1
    #check draw
    if "." not in inner_board_string:
        return 0
    #no winner, game still going
    return None


if __name__ == '__main__':
    board = "........./........./........./........./........./........./........./........./........."
    print_board(board)
    print(check_winner(board))
