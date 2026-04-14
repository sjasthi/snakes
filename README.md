# 🐍 Snakes — A Multi-Lingual Puzzle Generator

**Course:** ICS 499 — Software Engineering & Capstone Project  
**Professor:** Siva Jasthi  
**Semester:** Spring 2026  
**Authors:** Nathan Vo · Rocky Vang  

---

A web-based puzzle book generator built with Python and Flask. The application takes a collection of quotes and generates printable puzzle books featuring Snake Word puzzles and Drop Quote puzzles. Users can manage their quote library, customize puzzle preferences, and print or export the generated puzzles.

---

## ✨ Features

- **Snake Puzzle** — Letters from a quote are placed in a grid in a winding snake path, surrounded by random filler letters. Players find the hidden quote by tracing the snake.
- **Drop Quote Puzzle** — Letters are dropped into columns above a blank answer grid. Players figure out which column each letter belongs to in order to reveal the quote.
- **Load Quotes** — Upload a `.txt` file of quotes and manage them with full CRUD support (Add, Remove, Replace).
- **Difficulty Levels** — Three grid sizes for Snake puzzles: Easy (10×10), Normal (15×15), Hard (20×20).
- **Column Width Preferences** — Adjustable column width for Drop Quote puzzles (10, 15, 20, 25).
- **Show / Hide Solution** — Toggle solution visibility before printing.
- **Print to PDF** — Print any puzzle page directly from the browser with clean page breaks.
- **jQuery DataTable** — Searchable, sortable, paginated quote library on the Load Quotes page.

---

## 🛠️ Tech Stack

| Layer           | Technology                     |
|-----------------|--------------------------------|
| Backend         | Python, Flask                  |
| Frontend        | HTML, CSS, Bootstrap 5, Jinja2 |
| JavaScript      | jQuery, DataTables             |
| Data            | Plain text file (`quotes.txt`) |
| Version Control | Git, GitHub                    |

---

## 📁 Project Structure

```
snakes/
│
├── app.py                  # Main Flask app — all routes and logic
├── Grid.py                 # Snake puzzle grid generation (backtracking)
├── Cell.py                 # Individual cell in the grid
├── DropQuote.py            # Drop Quote puzzle logic
├── main.py                 # Quote loading utility
├── quotes.txt              # Quote library (one quote per line)
├── requirements.txt        # Python dependencies
├── .env                    # Secret key (not committed to GitHub)
├── .gitignore
│
├── static/
│   ├── css/
|   |    ├── base.css       # (Global layout, Navbar, Pref Bar)
|   |    ├── snake.css      # (Grid, cells, snake game logic)
|   |    ├── dropquote.css  # (Letter banks, drop cells, solutions)
|   |    ├── rebus.css      # (Image clues, rebus blanks)
|   |    └── print.css      # (All your @media print rules)
│   └── js/
│       └── script.js       # DataTable init and CRUD functions
│
└── templates/
    ├── layout.html         # Base Jinja2 template with navbar
    ├── load_quotes.html    # Quote management page
    ├── snakes.html         # Snake puzzle page
    ├── dropquote.html      # Drop Quote puzzle page
    ├── rebus.html        # Rebus puzzle page (in progress)
    └── help.html           # Help page
```

---

## ⚙️ Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/sjasthi/snakes.git
cd snakes
```

### 2. Create a virtual environment
```bash
python -m venv .venv
```

Activate it:
- **Windows:** `.venv\Scripts\activate`
- **Mac/Linux:** `source .venv/bin/activate`

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file
Create a file named `.env` in the project root and add:
```
SECRET_KEY=your_random_secret_key_here
```

### 5. Run the app
```bash
python app.py
```

Open your browser and go to `http://127.0.0.1:5000`

---

## 📖 How to Use

### Load Quotes
- Go to **Load Quotes** in the navbar
- Upload a `.txt` file with one quote per line to populate the library
- Use the Add, Remove, and Replace fields to manage individual quotes
- The table supports search, sort, and pagination

### Snake Puzzles
- Go to **Snakes** in the navbar
- Select a difficulty level — Easy, Normal, or Hard
- Each puzzle displays a grid with the quote hidden inside as a snake path
- Click **Print PDF** to generate a printable puzzle book

### Drop Quote Puzzles
- Go to **DropQuote** in the navbar
- Select a column width preference
- Toggle **Show Solution** to reveal or hide answers
- Click **Print Puzzle Book** to generate a printable book

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.