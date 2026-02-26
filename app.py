from flask import Flask, render_template, redirect, request
from Grid import Grid
from DropQuote import DropQuote
from main import load_quotes
from DropQuote import DropQuote

app = Flask(__name__)

@app.route('/')
def index():
    quotes = load_quotes("quotes.txt")
    all_puzzles = []

    for q in quotes:
        puzzle = Grid(q)
        all_puzzles.append({
            "quote": q,
            "grid": puzzle.grid
        })

    return render_template("game.html", all_puzzles=all_puzzles)

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

@app.route("/load-quotes")
def load_quotes_page():
    quotes = load_quotes("quotes.txt")
    return render_template("load_quotes.html", quotes=quotes)


if __name__ == "__main__":
    app.run(debug=True)