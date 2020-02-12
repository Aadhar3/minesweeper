from enum import Enum


class State(Enum):
    cell_covered = ' X '
    cell_mined = ' M '
    cell_empty = ' . '


class Cell:
    def __init__(self):
        self.possible_adjacent_mines = 0
        self.adjacent_mines = 0
        self.covered = True
        self.mined = False
        self.flagged_mines = set()

    def __repr__(self):
        state = self.state()
        if state == State.cell_covered:
            return State.cell_covered.value
        elif state == State.cell_mined:
            return State.cell_mined.value
        elif state == 0:
            return State.cell_empty.value
        return " {} ".format(str(state))

    def state(self):
        if self.covered:
            return State.cell_covered
        elif self.mined:
            return State.cell_mined
        else:
            return self.possible_adjacent_mines
