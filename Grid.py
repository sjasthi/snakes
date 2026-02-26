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
    def __init__(self, quote: str):
        self.quote = quote
        self.size = 15

        # print(self.get_quote())
        self.parsed_quote = self.parse_quote()

        # Create grid with empty cells
        self.grid = [[Cell.Cell(row, col) for col in range(self.size)] for row in range(self.size)]
        self.starting_cell = self.starting_spot()
        # print(f'Starting Position: {self.starting_cell.get_position()}')
        self.insert(self.starting_cell)
        self.fill()
        # self.print_grid()

    def get_quote(self) -> str:
        return self.quote

    def parse_quote(self) -> str:
        """
        Remove all special characters from quote

        :return: Cleaned string with all special characters removed
        """
        cleaned_string_all_removed = re.sub(r'[^a-zA-Z0-9]', '', self.quote)
        return cleaned_string_all_removed

    def print_grid(self) -> None:
        """
        Unpack each row and separate each element inside the row with a blank space. Print the result.
        ex:
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ]

            becomes:
                1 2 3
                4 5 6
                7 8 9

        :return: None
        """
        for row in self.grid:
            print(*row, sep=' ')

    def starting_spot(self) -> Cell:
        """
        Pick a random cell to be the starting position
        :return: An empty cell
        """
        rand_row = random.randrange(self.size)
        rand_col = random.randrange(self.size)

        starting_cell = self.grid[rand_row][rand_col]

        return starting_cell

    def insert(self, start_cell: Cell) -> None:
        """
        Insert the parsed quote into the grid using backtracking.
        Ensures that only the previous cell can be non-empty for each move
        :param start_cell: The starting cell

        :return: None
        """

        def backtrack(index: int, current_cell: Cell, visited: set) -> bool:
            """
            Recursive helper function to place letters
            :param index: Index of the character in parsed_quote
            :param current_cell: The current cell to place the letter
            :param visited: Set of cell positions already used in this path

            :return: True if the quote was fully placed, False otherwise
            """
            if index >= len(self.parsed_quote):
                return True  # All letters placed

            r, c = current_cell.get_position()
            current_cell.update_letter(self.parsed_quote[index])
            visited.add((r, c))

            # up left, up, up right, left, right, down left, down, down right
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

            # Collect all valid neighbors
            neighbors = []
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    candidate = self.grid[nr][nc]
                    if candidate.get_empty() and (nr, nc) not in visited:
                        # Check to make sure only previous cell is non-empty
                        valid = True
                        for ndr, ndc in directions:
                            nnr, nnc = nr + ndr, nc + ndc
                            if 0 <= nnr < self.size and 0 <= nnc < self.size:
                                neighbor_cell = self.grid[nnr][nnc]
                                if (nnr, nnc) != (r, c) and not neighbor_cell.get_empty():
                                    valid = False
                                    break
                        if valid:
                            neighbors.append(candidate)

            random.shuffle(neighbors)

            # Try each neighbor recursively
            for neighbor in neighbors:
                if backtrack(index + 1, neighbor, visited):
                    return True

            # Backtrack: undo current cell
            current_cell.empty = True
            current_cell.letter = 'None'
            visited.remove((r, c))
            return False

        # Start backtracking from the initial cell
        success = backtrack(0, start_cell, set())
        if not success:
            print("Failed to insert the entire quote.")

    def fill(self) -> None:
        """
        Loops through the grid and assigns a letter to every empty cell.

        :return: None
        """
        for row in self.grid:
            for cell in row:
                if cell.empty:
                    cell.random_letter()
