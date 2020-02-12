from board import Board, Game
import argparse


def main(n, num_mines):
    board = Board(n, num_mines)
    board.print_board()

    num_moves = 1
    while board.get_game_result() == Game.in_progress:
        try:
            row, col = get_user_input()
            board.click_cell(row - 1, col - 1, num_moves)
            board.print_board()
            num_moves += 1
        except ValueError:
            print("Please enter an integer for the row or the column")
        except IndexError:
            print("Please enter a valid combination of a row and column that represents a cell on the board")

    print(board.get_game_result().value)


def get_user_input():
    print()
    row = int(input("Please enter a row: "))
    col = int(input("Please enter a column: "))
    print()
    return row, col

# DO NOT EDIT--------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', nargs='?', type=int, default=10)
    parser.add_argument('num_mines', nargs='?', type=int, default=10)
    return parser.parse_args() 

if __name__ == "__main__":
    args = parse_args()
    main(args.n, args.num_mines)

# DO NOT EDIT--------------------------------------------
