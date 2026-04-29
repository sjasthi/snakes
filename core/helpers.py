import unicodedata

QUOTE_FILES = {
    "english": "data/quotes.txt",
    "telugu":  "data/quotes_telugu.txt",
}

def get_quote_file(lang: str) -> str:
    return QUOTE_FILES.get(lang, QUOTE_FILES["english"])


def rewrite_text_file(q, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        for quote in q:
            f.write(f'{quote}\n')


def add_quote(q, add, filepath):
    q.append(add)
    rewrite_text_file(q, filepath)


def remove_quote(q, q_index, filepath):
    del q[q_index - 1]
    rewrite_text_file(q, filepath)


def replace_quote(q, q_index, string, filepath):
    q[q_index - 1] = string
    rewrite_text_file(q, filepath)


def count_letters(quote: str) -> int:
    """Count all letters in a quote, including Unicode (e.g. Telugu)."""
    return sum(1 for ch in quote if unicodedata.category(ch)[0] in ("L", "M"))


def filter_quotes_by_grid(quotes, grid_size):
    limits = {10: 30, 15: 999, 20: 999}
    max_letters = limits.get(grid_size, 999)
    return [q for q in quotes if count_letters(q) <= max_letters]


def load_quotes(filepath) -> list:
    """Read quotes from a text file (one quote per line) and return a list."""
    quotes = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                quotes.append(line)
    return quotes


def print_quotes(quotes: list) -> None:
    for i, q in enumerate(quotes[:10], start=1):
        print(f"{i}. {q}")


if __name__ == '__main__':
    quotes = load_quotes(get_quote_file("english"))