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


if __name__ == '__main__':
    board = "........./........./........./........./........./........./........./........./........."
    print_board(board)
