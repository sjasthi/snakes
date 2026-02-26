from flask import Flask, render_template, jsonify, request, redirect
from Grid import Grid
from DropQuote import DropQuote
from main import load_quotes

app = Flask(__name__)


def rewrite_text_file(q):
    with open('quotes.txt', 'w', encoding='utf-8') as f:
        pass
    with open('quotes.txt', 'a', encoding='utf-8') as f:
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


@app.route('/')
def index():
    # Load quotes
    quotes = load_quotes("quotes.txt")

    all_puzzles = []

    # Loop through every quotes to generate a grid for each
    for q in quotes:
        # Generate puzzle
        puzzle = Grid(q)
        
        # Store the quote text and its specific grid layout together
        all_puzzles.append ({
            "quote": q,
            "grid": puzzle.grid
        })

    return render_template(
        "snakes.html",
        all_puzzles=all_puzzles
    )

@app.route('/load-quotes')
def load_quotes_page():
    quotes = load_quotes("quotes.txt")
    return render_template(
        "load_quotes.html",
        quotes=quotes
    )

@app.route('/dropquote')
def dropquote():
    quotes = load_quotes("quotes.txt")

    all_puzzles = []

    for q in quotes:
        dq = DropQuote(q)
        rows = dq.split_quote()
        columns = dq.columns
        max_col_height = max(len(c) for c in columns) if any(columns) else 0

        all_puzzles.append({
            "quote": q,
            "rows": rows,
            "columns": columns,
            "max_col_height": max_col_height
        })

    return render_template(
        "dropquote.html",
        all_puzzles=all_puzzles
    )


@app.route("/quotes/add", methods=["POST"])
def add():
    data = request.get_json()
    quote = data.get("quote")

    q = load_quotes()
    add_quote(q, quote)

    return jsonify({"message": "Quote added", "quote": quote})


@app.route("/quotes/remove", methods=["POST"])
def remove():
    data = request.get_json()
    index = data.get("index")

    q = load_quotes()
    remove_quote(q, index)

    return jsonify({"message": "Quote removed", "index": index})


@app.route("/quotes/replace", methods=["POST"])
def replace():
    data = request.get_json()
    index = data.get("index")
    new_text = data.get("quote")

    q = load_quotes()
    replace_quote(q, index, new_text)

    return jsonify({"message": "Quote replaced", "index": index, "new": new_text})


if __name__ == '__main__':
    app.run(debug=True)
