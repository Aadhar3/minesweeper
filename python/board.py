import random
from enum import Enum
from termcolor import cprint

from cell import Cell, State


class Game(Enum):
    won = 'Congratulations! You won :)'
    lost = 'You clicked on a mine, you lost :('
    in_progress = 'Game in progress..'


class Board:
    def __init__(self, n, num_mines):
        """Create a new instance of the minesweeper board

        Arguments:
            n: number of rows and columns in the board
            num_mines: number of mines in the board
        """

        self.n = n
        self.num_mines = num_mines
        self.safe_cells_remaining = (self.n * self.n) - num_mines
        self.mine_locations = []
        self.game_result = Game.in_progress
        self.board = [[Cell() for _ in range(self.n)] for _ in range(self.n)]
        self.place_mines(self.num_mines)

    def get_board_dimensions(self):
        return self.n

    def print_board(self):
        """Print the board with row and column numbers, and colors to make it easy to play"""
        for i in range(self.n):
            print(" {}".format(i + 1), end=" ")
        print()

        for row in range(self.n):
            for col in range(self.n):
                cell = self.board[row][col]
                if not cell.covered and cell.mined:
                    cprint(cell, 'red', end="")
                elif cell.possible_adjacent_mines == 1 and not cell.covered:
                    cprint(cell, 'blue', end="")
                elif cell.possible_adjacent_mines == 2 and not cell.covered:
                    cprint(cell, 'green', end="")
                elif cell.possible_adjacent_mines == 3 and not cell.covered:
                    cprint(cell, 'red', end="")
                elif cell.covered:
                    cprint(cell, 'grey', 'on_white', end="")
                else:
                    print(cell, end="")

                if col == self.n - 1:
                    print(" {}".format(row + 1), end=" ")

            print()
        print()

    def place_mines(self, num_mines):
        """Place {num_mines} mines randomly around the board"""

        while num_mines > 0:
            row = random.randint(0, self.n - 1)
            col = random.randint(0, self.n - 1)
            if not self.board[row][col].mined:
                self.mine_locations.append((row, col))
                self.board[row][col].mined = True
                self.change_surrounding_cells(row, col, increment=True)
                num_mines -= 1

    def replace_mine(self, row, col):
        """Place a new mine and remove the mine at the specified cell"""
        self.place_mines(1)
        self.board[row][col].mined = False
        self.change_surrounding_cells(row, col, increment=False)

    def change_surrounding_cells(self, row, col, increment):
        """Increment/Decrement the number of adjacent mines at the specified cell"""
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i < 0 or j < 0 or i >= self.n or j >= self.n:
                    continue

                if increment:
                    self.board[i][j].possible_adjacent_mines += 1
                    self.board[i][j].adjacent_mines += 1
                else:
                    self.board[i][j].possible_adjacent_mines -= 1
                    self.board[i][j].adjacent_mines -= 1

    def click_cell(self, row, col, num_moves):
        """Click a cell on the board

        Returns: the set of cells that were opened up due to the click and have
                 at least 1 mine near them
        """
        s = set()
        if row < 0 or col < 0 or row >= self.n or col >= self.n:
            raise IndexError("Please enter a valid combination of a"
                             " row and column that represents a cell on the board")

        if not self.board[row][col].covered:
            return s

        self.board[row][col].covered = False

        if self.board[row][col].mined:
            if num_moves == 1:
                self.replace_mine(row, col)
            else:
                self.game_result = Game.lost
                # this is commented out to save a bit of time on the solver
                self.reveal_all_mines()
                return s

        if self.board[row][col].possible_adjacent_mines == 0:
            self.reveal_adjacent_cells(row, col, s)
        else:
            s.add((row, col))
            self.safe_cells_remaining -= 1

        if self.safe_cells_remaining == 0:
            self.game_result = Game.won

        return s

    def reveal_adjacent_cells(self, row, col, s):
        """Reveal all valid adjacent cells when a specified cell is clicked"""
        self.board[row][col].covered = False
        self.safe_cells_remaining -= 1

        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i < 0 or j < 0 or i >= self.n or j >= self.n:
                    continue

                if not self.board[i][j].covered:
                    continue
                if not self.board[i][j].mined:
                    if self.board[i][j].possible_adjacent_mines == 0:
                        self.reveal_adjacent_cells(i, j, s)
                    else:
                        s.add((i, j))
                        self.board[i][j].covered = False
                        self.safe_cells_remaining -= 1

    def reveal_all_mines(self):
        """Uncover all the mines when the game is lost"""
        for mine in self.mine_locations:
            mine_row = mine[0]
            mine_col = mine[1]
            self.board[mine_row][mine_col].covered = False

    def get_game_result(self):
        """Gets the game result"""
        return self.game_result


