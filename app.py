from flask import Flask, render_template, jsonify, request, session, redirect
from Grid import Grid
from DropQuote import DropQuote
from Rebus import Rebus, generate_image
from RebusPixabay import RebusPixabay, generate_image
from main import load_quotes
from dotenv import load_dotenv
import re
import json
import os

app = Flask(__name__)

load_dotenv()  # Load environment variables from .env file
app.secret_key = os.getenv("SECRET_KEY")


# ── Helpers ───────────────────────────────────────────────────────────────────

def rewrite_text_file(q):
    with open('quotes.txt', 'w', encoding='utf-8') as f:
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


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    difficulty = request.args.get('difficulty', 'normal')
    show_solution = request.args.get('show_solution', 'false') == 'true'

    if difficulty not in ('easy', 'normal', 'hard'):
        difficulty = 'normal'

    size_map = {'easy': 10, 'normal': 15, 'hard': 20}
    grid_size = size_map[difficulty]

    cache_file = f'cache_snakes_{difficulty}.json'

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            all_puzzles = json.load(f)
    else:
        quotes = load_quotes("quotes.txt")
        filtered_quotes = filter_quotes_by_grid(quotes, grid_size)
        all_puzzles = []

        for q in filtered_quotes:
            puzzle = Grid(q, size=grid_size)
            all_puzzles.append({
                "quote": q,
                "grid": [[str(cell) for cell in row] for row in puzzle.grid],
                "size": puzzle.size
            })

        with open(cache_file, 'w') as f:
            json.dump(all_puzzles, f)

    return render_template(
        "snakes.html",
        all_puzzles=all_puzzles,
        difficulty=difficulty,
        grid_size=grid_size,
        show_solution=show_solution,
        total_quotes=len(all_puzzles),
        shown_quotes=len(all_puzzles)
    )


@app.route('/load-quotes')
def load_quotes_page():
    quotes = load_quotes("quotes.txt")
    return render_template("load_quotes.html", quotes=quotes)


@app.route('/dropquote')
def dropquote():
    col_width = request.args.get('col_width', '20')
    show_solution = request.args.get('show_solution', 'false') == 'true'

    valid_widths = [10, 15, 20, 25]
    try:
        col_width = int(col_width)
        if col_width not in valid_widths:
            col_width = 20
    except ValueError:
        col_width = 20

    quotes = load_quotes("quotes.txt")
    all_puzzles = []

    for q in quotes[:2]:
        dq = DropQuote(q, width=col_width)
        rows = dq.split_quote()
        columns = dq.columns
        max_col_height = max(len(c) for c in columns) if any(columns) else 0

        all_puzzles.append({
            "quote":          q,
            "rows":           rows,
            "columns":        columns,
            "max_col_height": max_col_height,
            "col_width":      col_width
        })

    return render_template(
        "dropquote.html",
        all_puzzles=all_puzzles,
        col_width=col_width,
        show_solution=show_solution
    )


@app.route('/rebus', methods=['GET', 'POST'])
def rebus():
    puzzles = []

    rebus_type = session.get('rebus_type', 'pixabay')  # default if not set

    if request.method == 'POST':
        # get form data
        selected_type = request.form.get('rebus_type')
        if selected_type in ('pixabay', 'hugging_face'):
            session['rebus_type'] = selected_type
            rebus_type = selected_type

        # then process words as usual
        words = []
        single_word = request.form.get('word', '').strip().upper()
        if single_word:
            words = [single_word]

        file = request.files.get('wordFile')
        if file and file.filename:
            content = file.read().decode('utf-8', errors='ignore')
            words = [w.strip().upper() for w in content.splitlines() if w.strip()]

        for word in words:
            if rebus_type == 'pixabay':
                r = RebusPixabay(word)
            else:
                r = Rebus(word)  # HuggingFace
            puzzle = r.to_dict()

            for clue in puzzle['clues']:
                if clue['clue_word']:
                    if rebus_type == 'pixabay':
                        img_path = generate_image(clue['clue_word'])
                        clue['image_url'] = f"img/rebus/{clue['clue_word'].lower()}.png" if img_path else None
                    else:
                        clue['image_url'] = None

            puzzles.append(puzzle)

    return render_template("rebus.html", puzzles=puzzles, rebus_type=rebus_type)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        rebus_type = request.form.get('rebus_type', 'pixabay')
        session['rebus_type'] = rebus_type
        return redirect(request.referrer or '/')

    # Default if not set yet
    rebus_type = session.get('rebus_type', 'pixabay')

    return render_template('settings.html', rebus_type=rebus_type)


# ── CRUD ──────────────────────────────────────────────────────────────────────

@app.route("/quotes/add", methods=["POST"])
def add():
    data  = request.get_json()
    quote = data.get("quote", "").strip()
    if not quote:
        return jsonify({"error": "Empty quote"}), 400
    q = load_quotes("quotes.txt")
    add_quote(q, quote)

    return jsonify({"message": "Quote added", "quote": quote})


@app.route("/quotes/remove", methods=["POST"])
def remove():
    data  = request.get_json()
    index = data.get("index")
    q     = load_quotes("quotes.txt")
    if not index or index < 1 or index > len(q):
        return jsonify({"error": "Invalid index"}), 400
    remove_quote(q, index)

    return jsonify({"message": "Quote removed", "index": index})


@app.route("/quotes/replace", methods=["POST"])
def replace():
    data     = request.get_json()
    index    = data.get("index")
    new_text = data.get("quote", "").strip()
    q        = load_quotes("quotes.txt")
    if not index or index < 1 or index > len(q) or not new_text:
        return jsonify({"error": "Invalid input"}), 400
    replace_quote(q, index, new_text)
    return jsonify({"message": "Quote replaced", "index": index, "new": new_text})

@app.route('/clear-cache', methods=['POST'])
def clear_cache():
    for f in ['cache_snakes_easy.json',
              'cache_snakes_normal.json',
              'cache_snakes_hard.json']:
        if os.path.exists(f):
            os.remove(f)
    return jsonify({"message": "Cache cleared"})


if __name__ == '__main__':
    app.run(debug=True)
