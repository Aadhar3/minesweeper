import random
from board import Board, Game


class Solver:
    def __init__(self, board):
        """Create a new instance of the minesweeper solver

        Arguments:
            board: the minesweeper board to be solved
        """
        self.board_object = board
        self.board = self.board_object.board
        self.n = self.board_object.get_board_dimensions()
        self.numbered_cells = set()
        self.flagged_cells = set()
        self.possible_moves = set()

    def num_cells(self, row, col, covered):
        """if covered is true:
                returns the set of covered cells around the cell at row,col
            if covered is false:
                returns the set of uncovered cells that have at least one mine
                around the cell at row,col
        """
        set_num_cells = set()
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i < 0 or j < 0 or i >= self.n or j >= self.n:
                    continue
                if i == row and j == col:
                    continue
                if covered:
                    if self.board[i][j].covered:
                        set_num_cells.add((i, j))
                else:
                    if not self.board[i][j].covered and self.board[i][j].adjacent_mines != 0:
                        set_num_cells.add((i, j))

        return set_num_cells

    def update_cells_around_flagged_cells(self, row, col):
        """Once a flagged cell (cell that is a mine) at row, col is found,
        tell it's neighbors that it is a flagged cell"""
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i < 0 or j < 0 or i >= self.n or j >= self.n:
                    continue
                if i == row and j == col:
                    continue
                self.board[i][j].flagged_mines.add((row, col))
                self.board[i][j].adjacent_mines -= 1

    def queue_moves(self, set_covered):
        """Queue up possible moves"""
        for cell in set_covered:
            if cell not in self.flagged_cells:
                self.possible_moves.add(cell)

    def flag_cells(self, set_flagged):
        """Update the solver once flagged cells (cells that are mines) are found"""
        for cell_flagged in set_flagged:
            if cell_flagged not in self.flagged_cells:
                self.flagged_cells.add(cell_flagged)
                self.update_cells_around_flagged_cells(cell_flagged[0], cell_flagged[1])

    def process_move(self, set_discovered):
        """Call this function after every move played to analyse the current board
           and find flagged cells (cells that are mines) and queue up possible moves
        """

        # only going through the new set of discovered cells
        for cell in set_discovered:
            row = cell[0]
            col = cell[1]
            set_num_covered = self.num_cells(row, col, covered=True)
            if len(set_num_covered) == self.board[row][col].possible_adjacent_mines:
                self.flag_cells(set_num_covered)

        # iterating again because it could be possible to not queue up a possible move,
        # if all the flagged cells are not found first
        for cell in set_discovered:
            row = cell[0]
            col = cell[1]
            if self.board[row][col].adjacent_mines == 0:
                set_num_covered = self.num_cells(row, col, covered=True)
                self.queue_moves(set_num_covered)

    def click_cell(self, cell, num_moves):
        """Click a particular cell, and process the move played afterwards"""
        set_discovered = self.board_object.click_cell(cell[0], cell[1], num_moves)
        self.numbered_cells = self.numbered_cells.union(set_discovered)
        self.process_move(set_discovered)

    def guess(self):
        """Make a reasonable guess, not choosing cells that are flagged as mines"""
        while True:
            row = random.randint(0, self.n - 1)
            col = random.randint(0, self.n - 1)
            if (row, col) not in self.flagged_cells and self.board[row][col].covered:
                return row, col

    def next_move(self):
        """Decide the next move, pick a move from self.possible_moves or guess"""

        # if no moves available, go through all numbered cells found, and see if there any moves.
        # this could create possible moves as the solver only goes through discovered cells
        # on each turn and not the full set of numbered cells found
        if len(self.possible_moves) == 0:
            self.process_move(self.numbered_cells)

        if len(self.possible_moves) != 0:
            cell = self.possible_moves.pop()
        else:
            cell = self.guess()
        return cell

    def solve(self) -> bool:
        """Returns if the solver is successfully able to solve the board"""

        # num_moves = 1 has is significant because the user cannot lose on the first click
        # so if the first click is a mine, the board places the mine somewhere else
        num_moves = 1
        while self.board_object.get_game_result() == Game.in_progress:
            cell = self.next_move()
            self.click_cell(cell, num_moves)
            num_moves += 1

        game_result = self.board_object.get_game_result()
        return game_result == Game.won
