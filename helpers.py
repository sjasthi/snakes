import re

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

