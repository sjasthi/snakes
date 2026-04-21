import re
# import core.Grid as Grid

QUOTE_FILE = "data/quotes.txt"

def rewrite_text_file(q):
    with open(QUOTE_FILE, 'w', encoding='utf-8') as f:
        for quote in q:
            f.write(f'{quote}\n')


def add_quote(q, add):
    q.append(add)
    rewrite_text_file(q)


def remove_quote(q, q_index):
    del q[q_index - 1]
    rewrite_text_file(q)


def replace_quote(q, q_index, string):
    q[q_index - 1] = string
    rewrite_text_file(q)


def filter_quotes_by_grid(quotes, grid_size):
    # For 10x10, only allow quotes with 30 letters or fewer (safe limit)
    # For 15x15 and 20x20, all quotes fit fine
    limits = {10: 30, 15: 999, 20: 999}
    max_letters = limits.get(grid_size, 999)
    return [q for q in quotes
            if len(re.sub(r'[^a-zA-Z]', '', q)) <= max_letters]


def load_quotes(filepath=QUOTE_FILE) -> list:
    quotes = []
    """Read quotes from a text file (one quote per line) and return a list."""
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


# def generate_puzzles(quotes: list[str]):
#     """
#     Generate puzzles using the given list of quotes
#     :param quotes: List of quotes
#     :return: List of puzzles
#     """
#     puzzles = []
#     for quote in quotes[:10]:
#         puzzle = Grid.Grid(quote=quote)
#         # puzzle.print_grid()
#         # print("\n")
#         puzzles.append(puzzle)

#     return puzzles


if __name__ == '__main__':
    quotes = load_quotes("data/quotes.txt")
    # print_quotes(quotes=quotes)

