import string
import random


class Cell:
    """
    The Cell class represents a cell in the Grid class. It contains attributes about the cell's position and its
    contents.

    Attributes:
        empty (bool): Whether the cell is empty (True) or contains a letter (False).
        letter (str): The letter stored in the cell. Initially set to 'None'.
        row (int): The row index of the cell within the grid.
        col (int) The column index of the cell within the grid.
    """

    def __init__(self, row: int, col: int):
        """
        Initializes a cell with the given row and column indices. The cell is initially empty and contains the letter
        'None'
        :param row: The row index of the cell within the cell
        :param col: The column index of the cell within the cell
        """
        self.empty = True
        self.letter = 'None'
        self.row = row
        self.col = col

    def get_empty(self):
        return self.empty

    def get_letter(self):
        return self.letter

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_position(self):
        position = (self.row, self.col)
        return position

    def update_letter(self, letter: str) -> None:
        """
        Updates the cell with a new letter and marks it as not empty. The letter will be converted to uppercase
        :param letter: (str) The letter to assign to the cell

        :return: None
        """
        self.letter = letter.upper()
        self.empty = False

    def random_letter(self) -> None:
        """
        Assign a random letter to the cell and marks it as not empty. The letter will be converted to uppercase

        :return: None
        """
        self.letter = random.choice(string.ascii_letters).upper()
        self.empty = False

    def __str__(self) -> str:
        """
        Returns a string representation of the cell

        :return: (str) '-' if the cell is empty, or the letter if the cell is not empty
        """
        if self.empty:
            return '-'
        else:
            return self.letter
