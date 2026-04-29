# 🐍 Snakes — A Multi-Lingual Puzzle Generator

**Course:** ICS 499 — Software Engineering & Capstone Project  
**Professor:** Siva Jasthi  
**Semester:** Spring 2026  
**Authors:** Nathan Vo · Rocky Vang

---

A web-based puzzle book generator built with Python and Flask. The application takes a collection of quotes and generates printable puzzle books featuring three puzzle types — Snake Word puzzles, Drop Quote puzzles, and Rebus image puzzles — with full support for both English and Telugu languages.

---

## 📚 Documentation

| Document | Audience | Description |
|---|---|---|
| [USER_GUIDE.md](USER_GUIDE.md) | End users | How to use the app — no coding knowledge required |
| [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) | Developers | Setup, APIs, architecture, and how to extend the project |

---

## ✨ Features

- **Snake Puzzle** — A quote snakes through a letter grid surrounded by random filler. Trace the path to reveal the message.
- **Drop Quote Puzzle** — Letters are dropped into shuffled columns above a blank answer grid.
- **Rebus Puzzle** — Each letter of a target word is clued by an image. Identify the image, find the letter, spell the word.
- **English & Telugu support** — Full language switching on Snake, Drop Quote, and Load Quotes pages.
- **Three difficulty levels** — Easy (10×10), Normal (15×15), Hard (20×20) for Snake puzzles.
- **Three Rebus image modes** — Pixabay real photos, HuggingFace AI-generated images, Telugu word bank.
- **Show / Hide Solution** — Toggle answer visibility before printing on all puzzle types.
- **Print to PDF** — Every puzzle page prints cleanly with puzzle numbers and automatic page breaks.
- **Quote management** — Full CRUD (Add, Remove, Replace) with DataTable search and pagination.
- **Puzzle caching** — Generated puzzles are cached as JSON to avoid regenerating on every page load.

---

## 🚀 Quick Start

```bash
git clone https://github.com/sjasthi/snakes.git
cd snakes
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
# Create .env with SECRET_KEY, HF_TOKEN, PIXABAY_API_KEY
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for full setup instructions and API key details.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask |
| Frontend | HTML, CSS, Bootstrap 5, Jinja2 |
| JavaScript | jQuery, DataTables |
| Image APIs | Pixabay, HuggingFace FLUX.1-schnell |
| Telugu API | Ananya (jasthi.com) |
| Version Control | Git, GitHub |

---

## 📝 License

This project is licensed under the MIT License.