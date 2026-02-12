import Grid


def load_quotes(filepath="quotes.txt") -> list:
    """Read quotes from a text file (one quote per line) and return a list."""
    quotes = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:  # skip empty lines
                quotes.append(line)
    return quotes


def print_quotes(quotes: list[str]) -> None:
    # Print the first 10 quotes to confirm it works
    for i, q in enumerate(quotes[:10], start=1):
        print(f"{i}. {q}")


def generate_puzzles(quotes: list[str]) -> list[Grid]:
    """
    Generate puzzles using the given list of quotes
    :param quotes: List of quotes
    :return: List of puzzles
    """
    puzzles = []
    for quote in quotes[:10]:
        puzzle = Grid.Grid(quote=quote)
        # puzzle.print_grid()
        # print("\n")
        puzzles.append(puzzle)

    return puzzles


if __name__ == '__main__':
    quotes = load_quotes("quotes.txt")
    # print_quotes(quotes=quotes)

    puzzles = generate_puzzles(quotes=quotes)
    for puzzle in puzzles:
        print(puzzle.get_quote())
        puzzle.print_grid()
        print('\n')
