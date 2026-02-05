import random
import re
import Cell


class Grid:
    """
    The Grid class represents a grid of size 15x15 that contains cells in each space.

    Attributes:
        quote (str): The quote that will be placed in the grid.
        size (int): The size of the grid. Set to be 15x15.
    """
    def __init__(self, quote):
        self.quote = quote
        print(self.get_quote())
        self.parsed_quote = self.parse_quote()
        self.size = 15
        self.grid = [[Cell.Cell(row, col) for col in range(self.size)] for row in range(self.size)]
        self.starting_cell = self.starting_spot()
        print(f'Starting Position: {self.starting_cell.get_position()}')
        self.insert(self.starting_cell)
        # self.fill()
        self.print_board()

    def get_quote(self):
        return self.quote

    def parse_quote(self):
        char = []
        cleaned_string_all_removed = re.sub(r'[^a-zA-Z0-9]', '', self.quote)

        for character in cleaned_string_all_removed:
            char.append(character)
        return char

    def print_board(self):
        for row in self.grid:
            print(*row, sep=' ')

    def starting_spot(self):
        rand_row = random.randrange(self.size)
        rand_col = random.randrange(self.size)
        # print(f'Starting row:{rand_row} Starting col:{rand_col}')

        starting_cell = self.grid[rand_row][rand_col]
        return starting_cell

    def insert(self, cell):
        # print(type(start))
        for character in self.parsed_quote:
            try:
                cell.update_letter(letter=character)
                cell = self.next_cell(cell)
            except AttributeError:
                pass

    def next_cell(self, cell):
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        row = cell.get_row()
        col = cell.get_col()

        neighbors = []
        for d_row, d_col in directions:
            new_row = row + d_row
            new_col = col + d_col
            if 0 <= new_row <= self.size - 1 and 0 <= new_col <= self.size - 1:
                neighbors.append((new_row, new_col))

        random.shuffle(neighbors)

        for r, c in neighbors:
            next_c = self.grid[r][c]
            if next_c.get_empty():
                return next_c

        # debug
        print(f'Stopped here:{cell.get_position()}')
        print(f'{cell.get_letter()}')
        print('No empty neighbors')

    def fill(self):
        for row in self.grid:
            for cell in row:
                if cell.empty:
                    cell.random_letter()
