import string
import random
import requests


def telugu_filler():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    api_url = 'https://jasthi.com/ananya/api.php/characters/filler?language=telugu&count=100'
    response = requests.get(api_url, headers=headers)
    data = response.json()

    return data['result']


tel_filler = telugu_filler()


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

    def random_letter(self, english) -> None:
        """
        Assign a random letter to the cell and marks it as not empty. The letter will be converted to uppercase

        :return: None
        """
        if english:
            self.letter = random.choice(string.ascii_letters).upper()
            self.empty = False
        else:
            self.letter = self.letter = random.choice(tel_filler)
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
