from flask import Flask, render_template, jsonify, request, session, redirect
from core.helpers import (add_quote, load_quotes, remove_quote, replace_quote, filter_quotes_by_grid)
from core.Grid import Grid
from core.DropQuote import DropQuote
from core.Rebus import Rebus, generate_image
from core.RebusPixabay import RebusPixabay, generate_image_pixabay
from core.RebusTelugu import RebusTelugu, generate_image_pixabay as telugu_image_pixabay
from dotenv import load_dotenv
import json
import os

app = Flask(__name__)

load_dotenv()  # Load environment variables from .env file
app.secret_key = os.getenv("SECRET_KEY")
QUOTE_FILE = "data/quotes.txt"
CACHE_DIR = "cache"

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    quotes = load_quotes(QUOTE_FILE)
    return render_template("home.html", total_quotes=len(quotes))


@app.route('/snake')
def snake():
    difficulty = request.args.get('difficulty', 'normal')
    show_solution = request.args.get('show_solution', 'false') == 'true'

    if difficulty not in ('easy', 'normal', 'hard'):
        difficulty = 'normal'

    size_map = {'easy': 10, 'normal': 15, 'hard': 20}
    grid_size = size_map[difficulty]

    filename = f'cache_snakes_{difficulty}.json'
    cache_file = os.path.join(CACHE_DIR, filename)

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            all_puzzles = json.load(f)
    else:
        quotes = load_quotes(QUOTE_FILE)
        filtered_quotes = filter_quotes_by_grid(quotes, grid_size)
        all_puzzles = []

        for q in filtered_quotes:
            puzzle = Grid(q, size=grid_size)
            all_puzzles.append({
                "quote": q,
                "grid": [[str(cell) for cell in row] for row in puzzle.grid],
                "size": puzzle.size,
                "solution_path": puzzle.solution_path
            })

        # Ensure the folder exists before writing it -> Make directory(if its exist, ignore)
        os.makedirs(CACHE_DIR, exist_ok=True)

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
    quotes = load_quotes(QUOTE_FILE)
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

    filename = f'cache_dropquote_w{col_width}.json'
    cache_file = os.path.join(CACHE_DIR, filename)

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            all_puzzles = json.load(f)
    else: 
        quotes = load_quotes(QUOTE_FILE)
        all_puzzles = []

        for q in quotes:
            dq             = DropQuote(q, width=col_width)
            rows           = dq.split_quote()
            columns        = dq.columns
            max_col_height = max(len(c) for c in columns) if any(columns) else 0

            # Build answer rows — same structure but show actual letters
            answer_rows = []
            for row in rows:
                answer_row = []
                for char in row:
                    if char == '_':
                        answer_row.append('LETTER')  # placeholder, we'll fill below
                    else:
                        answer_row.append(char)
                answer_rows.append(answer_row)

            # Fill in the actual letters from the quote
            letter_index = 0
            quote_upper  = q.upper()
            for r_idx, row in enumerate(rows):
                for c_idx, char in enumerate(row):
                    if char == '_':
                        # Find the next letter in the original quote
                        while letter_index < len(quote_upper) and not quote_upper[letter_index].isalnum():
                            letter_index += 1
                        if letter_index < len(quote_upper):
                            answer_rows[r_idx][c_idx] = quote_upper[letter_index]
                            letter_index += 1

            all_puzzles.append({
                "quote":          q,
                "rows":           rows,
                "answer_rows":    answer_rows, 
                "columns":        columns,
                "max_col_height": max_col_height,
                "col_width":      col_width
            })

        # Ensure the folder exists before writing it -> Make directory(if its exist, ignore)
        os.makedirs(CACHE_DIR, exist_ok=True)
        
        with open(cache_file, 'w') as f:
            json.dump(all_puzzles, f)
    return render_template(
        "dropquote.html",
        all_puzzles=all_puzzles,
        col_width=col_width,
        show_solution=show_solution
    )


@app.route('/rebus', methods=['GET', 'POST'])
def rebus():
    puzzles = []
    rebus_type = session.get('rebus_type', 'pixabay')

    selected_count = 1  # default

    if request.method == 'POST':
        selected_type = request.form.get('rebus_type')
        if selected_type in ('pixabay', 'hugging_face', 'telugu'):
            session['rebus_type'] = selected_type
            rebus_type = selected_type

        # NEW: capture which button was clicked
        selected_count = int(request.form.get("count", 1))

        # process words
        words = []
        single_word = request.form.get('word', '').strip().upper()
        if single_word:
            words = [single_word]

        file = request.files.get('wordFile')
        if file and file.filename:
            content = file.read().decode('utf-8', errors='ignore')
            words = [w.strip().upper() for w in content.splitlines() if w.strip()]

        used_words = set()

        for word in words:
            for _ in range(selected_count):  # <-- generate multiple puzzles
                if rebus_type == 'pixabay':
                    r = RebusPixabay(word, used_words=used_words)
                elif rebus_type == 'telugu':
                    r = RebusTelugu(word)
                else:
                    r = Rebus(word, used_words=used_words)

                puzzle = r.to_dict()

                # process images
                for clue in puzzle['clues']:
                    if clue['clue_word']:
                        if rebus_type == 'pixabay':
                            img_path = generate_image_pixabay(clue['clue_word'])
                            clue['image_url'] = f"img/rebus/{clue['clue_word'].lower()}.png" if img_path else None

                        elif rebus_type == 'telugu':
                            english = clue.get("english")
                            if english:
                                img_path = telugu_image_pixabay(english)
                                clue['image_url'] = f"img/rebus/{english.lower()}.png" if img_path else None
                            else:
                                clue['image_url'] = None

                        elif rebus_type == 'hugging_face':
                            img_path = generate_image(clue['clue_word'])
                            clue['image_url'] = f"img/rebus/{clue['clue_word'].lower()}.png" if img_path else None

                puzzles.append(puzzle)

    return render_template(
        "rebus.html",
        puzzles=puzzles,
        rebus_type=rebus_type,
        selected_count=selected_count
    )


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        rebus_type = request.form.get('rebus_type', 'pixabay')
        session['rebus_type'] = rebus_type
        return redirect(request.referrer or '/')

    # Default if not set yet
    rebus_type = session.get('rebus_type', 'pixabay')

    return render_template('settings.html', rebus_type=rebus_type)


MAX_QUOTE_LENGTH = 500


def clear_puzzle_cache():
    """Remove all cached puzzle JSON files so stale data is never served."""
    if os.path.exists(CACHE_DIR):
        for filename in os.listdir(CACHE_DIR):
            file_path = os.path.join(CACHE_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


# ── CRUD ──────────────────────────────────────────────────────────────────────

@app.route("/quotes/add", methods=["POST"])
def add():
    data  = request.get_json()
    quote = data.get("quote", "").strip()
    if not quote:
        return jsonify({"error": "Empty quote"}), 400
    if len(quote) > MAX_QUOTE_LENGTH:
        return jsonify({"error": f"Quote exceeds {MAX_QUOTE_LENGTH} characters"}), 400
    q = load_quotes(QUOTE_FILE)
    add_quote(q, quote)
    clear_puzzle_cache()
    return jsonify({"message": "Quote added", "quote": quote})


@app.route("/quotes/remove", methods=["POST"])
def remove():
    data  = request.get_json()
    index = data.get("index")
    q     = load_quotes(QUOTE_FILE)
    if not index or index < 1 or index > len(q):
        return jsonify({"error": "Invalid index"}), 400
    remove_quote(q, index)
    clear_puzzle_cache()
    return jsonify({"message": "Quote removed", "index": index})


@app.route("/quotes/replace", methods=["POST"])
def replace():
    data     = request.get_json()
    index    = data.get("index")
    new_text = data.get("quote", "").strip()
    q        = load_quotes(QUOTE_FILE)
    if not index or index < 1 or index > len(q) or not new_text:
        return jsonify({"error": "Invalid input"}), 400
    if len(new_text) > MAX_QUOTE_LENGTH:
        return jsonify({"error": f"Quote exceeds {MAX_QUOTE_LENGTH} characters"}), 400
    replace_quote(q, index, new_text)
    clear_puzzle_cache()
    return jsonify({"message": "Quote replaced", "index": index, "new": new_text})

@app.route('/clear-cache', methods=['POST'])
def clear_cache():
    clear_puzzle_cache()
    return jsonify({"message": "Cache folder cleared"})


if __name__ == '__main__':
    app.run(debug=True)
