import random
import re
import requests
import unicodedata
from Cell import Cell


def ananya(quote: str) -> list[str]:
    """
    Uses api to break a given quote into individual character. Works for English and Telugu characters.
    Args:
        quote (str): The quote to break down

    Returns:
        A list of each character in the string
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    api_url = f'https://jasthi.com/ananya/api.php/characters/logical?string={quote}&language=Telugu'
    response = requests.get(api_url, headers=headers)
    data = response.json()

    return data['result']


class Grid:
    """
    The Grid class represents a grid of size 15x15 that contains cells in each space.

    Attributes:
        quote (str): The quote that will be placed in the grid.
        size (int): The size of the grid. Set to be 15x15.
    """

    def __init__(self, quote: str, size: int = 15):
        self.quote = quote
        self.size = size

        self.parsed_quote = self.parse_quote()

        # Create grid with empty cells
        self.grid = [
            [Cell(row, col) for col in range(self.size)] 
            for row in range(self.size)
        ]
        
        self.starting_cell = self.starting_spot()
        # print(f'Starting Position: {self.starting_cell.get_position()}')
        self.insert(self.starting_cell)
        self.fill()
        # self.print_grid()

    def parse_quote(self) -> list[str]:
        """
        Remove all special characters from quote. Works for telugu characters.

        :return: Cleaned string with all special characters removed
        """
        return [cluster
                for cluster in self.quote
                if all(unicodedata.category(ch)[0] in ("L", "N", "M") for ch in cluster)]

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


if __name__ == '__main__':
    q = 'You do not have to be great to start but you have to start to be great.'
    q1 = 'పక్షులు మనకు సహజమైన స్నేహితులు - వారు మనకు నేర్పిస్తారు సహనం మరియు ప్రేమను.'
    g = Grid(q1)

    print(g.quote)
    print(g.parsed_quote)
    # g.print_grid()
