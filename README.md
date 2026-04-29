# 🐍 Snakes — A Multi-Lingual Puzzle Generator

**Course:** ICS 499 — Software Engineering & Capstone Project  
**Professor:** Siva Jasthi  
**Semester:** Spring 2026  
**Authors:** Nathan Vo · Rocky Vang  

---

A web-based puzzle book generator built with Python and Flask. The application takes a collection of quotes and generates printable puzzle books featuring three puzzle types — Snake Word puzzles, Drop Quote puzzles, and Rebus image puzzles — with full support for both English and Telugu languages.


---

## 📋 Table of Contents

- [End-User Guide](#-end-user-guide)
  - [Getting Started](#getting-started)
  - [Managing Quotes](#managing-quotes)
  - [Snake Puzzle](#snake-puzzle)
  - [Drop Quote Puzzle](#drop-quote-puzzle)
  - [Rebus Puzzle](#rebus-puzzle)
  - [Printing](#printing)
- [Developer Guide](#-developer-guide)
  - [Tech Stack](#tech-stack)
  - [Project Structure](#project-structure)
  - [Installation & Setup](#installation--setup)
  - [Environment Variables & API Keys](#environment-variables--api-keys)
  - [External APIs & Dependencies](#external-apis--dependencies)
  - [Caching System](#caching-system)
  - [Adding a New Language](#adding-a-new-language)

## 👤 End-User Guide

This section is for anyone who wants to use Snakes to generate puzzle books — no coding knowledge required.

### Getting Started

When you open the app, you land on the **Home page**. From here you can navigate to any puzzle type using the navbar at the top. The navbar logo always brings you back to the home page.

The app has five main pages:

| Page | What it does |
|---|---|
| **Load Quotes** | Upload and manage the quotes used to generate puzzles |
| **Snakes** | Generate Snake Word grid puzzles |
| **Drop Quote** | Generate Drop Quote column puzzles |
| **Rebus** | Generate Rebus image puzzles |
| **Settings** | Choose the Rebus image source |

---

### Managing Quotes

Before generating puzzles, you need a quote library loaded into the app.

**Go to Load Quotes in the navbar.**

- **Switch language** — Use the 🇺🇸 English / 🇮🇳 Telugu toggle at the top to manage English or Telugu quotes separately.
- **Upload a file** — Prepare a `.txt` file with one quote per line, then upload it on the Load Quotes page to replace the current library.
- **Add a quote** — Type a new quote into the Add Quote field and click **Add**.
- **Remove a quote** — Enter the quote number (shown in the # column) and click **Remove**.
- **Replace a quote** — Enter the quote number and new text, then click **Replace**.
- **Search** — Use the search box above the table to filter quotes instantly.

> **Note:** Editing quotes automatically clears the puzzle cache so the next puzzle you generate reflects your changes.

---

### Snake Puzzle

**Go to Snakes in the navbar.**

Each puzzle hides a quote inside a letter grid. The quote snakes through the grid in a continuous winding path — your job is to trace it from start to finish.

**Preferences (top bar):**

| Option | Description |
|---|---|
| **Grid Size** | Easy (10×10) · Normal (15×15) · Hard (20×20) |
| **Solution** | Hidden — blank grid only · Revealed — path highlighted |
| **Language** | 🇺🇸 English quotes · 🇮🇳 Telugu quotes |

- Switching any preference reloads the puzzles automatically.
- Click **🔄 Regenerate** to get a fresh set of puzzles from the same quote library.
- Click **🖨️ Print PDF** to open the browser print dialog and save as PDF.

---

### Drop Quote Puzzle

**Go to Drop Quote in the navbar.**

Letters from a quote are split into columns and shown above a blank answer grid. The letters have been shuffled within each column — your job is to figure out which letter drops into which blank slot to spell out the quote row by row.

**Preferences (top bar):**

| Option | Description |
|---|---|
| **Column Width** | How many columns wide the puzzle is: 10, 15, 20, or 25 |
| **Solution** | Hidden · Revealed |
| **Language** | 🇺🇸 English · 🇮🇳 Telugu |

- Wider columns = more letters per row = harder puzzle.
- Click **🖨️ Print PDF** to print all puzzles as a book.

---

### Rebus Puzzle

**Go to Rebus in the navbar.**

Each letter of a target word is clued by an image. Identify the picture, find the letter at the position shown in the hint (e.g. `2/5` means the 2nd letter of a 5-letter word), and combine all the letters to spell the answer.

**How to generate a puzzle:**

1. Type a word into the **Word** field (e.g. `METRO`) and click one of the generate count buttons — **1, 10, 25, 50, or 100** puzzles.
2. Or upload a `.txt` word list file (one word per line) and click **Upload** to generate puzzles for every word in the file.

**After generating:**

- Use the **Solution** toggle to reveal or hide the answer letters and answer word.
- Click **🖨️ Print PDF** to print all puzzles.

**Image source** is set in **Settings**:

| Mode | Description |
|---|---|
| **Pixabay** | Real photographs fetched from Pixabay |
| **HuggingFace** | AI-generated images using FLUX.1 model |
| **Telugu** | Telugu word clues with Pixabay photographs |

> **Note:** The first time an image is generated for a word it is saved locally, so future puzzles load it instantly without calling the API again.

---

### Printing

Every puzzle page is designed for clean browser printing:

1. Click the **🖨️ Print PDF** button on any puzzle page.
2. In the browser print dialog, set destination to **Save as PDF**.
3. Each puzzle prints on its own page with its puzzle number shown.
4. The preference bar, solution toggles, and other controls are automatically hidden from the printed output.

---

## 🛠️ Developer Guide

This section is for developers setting up, maintaining, or extending the project.

### Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask |
| Frontend | HTML, CSS, Bootstrap 5, Jinja2 |
| JavaScript | jQuery, DataTables |
| Image APIs | Pixabay REST API, HuggingFace Inference API (FLUX.1-schnell) |
| Telugu API | Ananya grapheme cluster API (jasthi.com) |
| Data | Plain text files (`quotes.txt`, `quotes_telugu.txt`) |
| Cache | JSON files in `cache/` folder |
| Version Control | Git, GitHub |

---

### Project Structure
snakes/
│
├── app.py                      # Main Flask app — all routes, caching, CRUD
├── requirements.txt            # Python dependencies
├── .env                        # Secret keys (never commit this)
├── .gitignore
│
├── core/                       # Puzzle generation logic
│   ├── Grid.py                 # Snake puzzle grid (recursive backtracking)
│   ├── Cell.py                 # Individual grid cell with Telugu filler support
│   ├── DropQuote.py            # Drop Quote puzzle — column splitting logic
│   ├── RebusBase.py            # Shared base class for English Rebus generators
│   ├── Rebus.py                # Rebus using HuggingFace AI image generation
│   ├── RebusPixabay.py         # Rebus using Pixabay photo search
│   ├── RebusTelugu.py          # Telugu Rebus using local cluster index
│   └── helpers.py              # Quote file I/O and CRUD helpers
│
├── data/
│   ├── quotes.txt              # English quote library (one quote per line)
│   ├── quotes_telugu.txt       # Telugu quote library (one quote per line)
│   └── word_bank.py            # English & Telugu word banks + LETTER_INDEX
│
├── cache/                      # Auto-generated puzzle cache (JSON files)
│
├── static/
│   ├── css/
│   │   ├── layout.css          # Global layout, navbar, pref bar, footer
│   │   ├── home.css            # Home page styles
│   │   ├── snake.css           # Snake grid and cell styles
│   │   ├── dropquote.css       # Drop Quote board styles
│   │   ├── rebus.css           # Rebus image clues and blank styles
│   │   └── print.css           # All @media print rules
│   ├── js/
│   │   └── script.js           # DataTable init, CRUD fetch calls
│   └── img/
│       ├── nav-bar.png         # Navbar logo
│       └── rebus/              # Cached rebus images (auto-generated)
│
└── templates/
├── layout.html             # Base Jinja2 template (navbar + footer)
├── home.html               # Landing page
├── load_quotes.html        # Quote management page
├── snakes.html             # Snake puzzle page
├── dropquote.html          # Drop Quote puzzle page
├── rebus.html              # Rebus puzzle page
└── settings.html           # Rebus image source settings

---

### Installation & Setup

#### 1. Clone the repository
```bash
git clone https://github.com/sjasthi/snakes.git
cd snakes
```

#### 2. Create a virtual environment
```bash
python -m venv .venv
```

Activate it:
- **Windows:** `.venv\Scripts\activate`
- **Mac/Linux:** `source .venv/bin/activate`

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Create the `.env` file
SECRET_KEY=your_random_secret_key_here
HF_TOKEN=your_huggingface_token_here
PIXABAY_API_KEY=your_pixabay_api_key_here

#### 5. Run the app
```bash
python app.py
```

Open your browser and go to `http://127.0.0.1:5000`

---


### Environment Variables & API Keys

| Variable | Required | Description | Where to get it |
|---|---|---|---|
| `SECRET_KEY` | ✅ Yes | Flask session encryption key | `python -c "import secrets; print(secrets.token_hex(32))"` |
| `HF_TOKEN` | HuggingFace mode | HuggingFace API bearer token | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| `PIXABAY_API_KEY` | Pixabay & Telugu mode | Pixabay REST API key | [pixabay.com/api/docs](https://pixabay.com/api/docs/) |

---

### External APIs & Dependencies

**Pixabay API** — fetches real photos for Rebus clues. Endpoint: `https://pixabay.com/api/`. Falls back to `?` placeholder on failure.

**HuggingFace FLUX.1-schnell** — generates AI images for English Rebus clues. Endpoint: `https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell`. Falls back to `?` placeholder on failure.

**Ananya API** — splits Telugu text into grapheme clusters. Endpoint: `https://jasthi.com/ananya/api.php/characters/logical`. Falls back to `list(quote)` if unreachable. Skipped entirely for English-only quotes.

**Image caching** — all fetched/generated images are saved to `static/img/rebus/<word>.png` on first use and reused on subsequent requests.

---

### Caching System
cache_snakes_{lang}{difficulty}.json       # e.g. cache_snakes_english_normal.json
cache_dropquote{lang}_w{width}.json        # e.g. cache_dropquote_telugu_w20.json

Cache is automatically cleared when quotes are added, removed, or replaced. Use the **🔄 Regenerate** button or call `POST /clear-cache` to manually bust it.

---

### Adding a New Language

1. Add `data/quotes_spanish.txt`
2. Register in `helpers.py`: `"spanish": "data/quotes_spanish.txt"`
3. Add to `VALID_LANGS` in `app.py`: `("english", "telugu", "spanish")`
4. Add the toggle button to `snakes.html`, `dropquote.html`, and `load_quotes.html`

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.