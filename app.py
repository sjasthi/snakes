from flask import Flask, render_template, jsonify
from Grid import Grid
from main import load_quotes

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
