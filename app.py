from flask import Flask, render_template, jsonify
from Grid import Grid
from main import load_quotes

app = Flask(__name__)


@app.route('/')
def index():
    # Load quotes
    quotes = load_quotes("quotes.txt")
    quote = quotes[1]

    # Generate puzzle
    puzzle = Grid(quote)

    display_grid = puzzle.grid

    puzzle.print_grid()

    return render_template(
        "game.html",
        grid=display_grid,
        quote=quote
    )


if __name__ == '__main__':
    app.run(debug=True)
