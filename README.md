# 🐍 Snakes — A Multi-Lingual Puzzle Generator

**Course:** ICS 499 — Software Engineering & Capstone Project  
**Professor:** Siva Jasthi  
**Semester:** Spring 2026  
**Authors:** Nathan Vo · Rocky Vang  

A web-based puzzle book generator built with Python and Flask. The application takes a collection of quotes and generates printable puzzle books featuring Snake Word puzzles, Drop Quote puzzles, and Rebus image puzzles. Users can manage their quote library, customize puzzle preferences, and print the generated puzzles.

## ✨ Features

* **Snake Puzzle** — A quote snakes through a letter grid in a winding path, surrounded by random filler letters. Players trace the path to reveal the quote.
* **Drop Quote Puzzle** — Letters are dropped into columns above a blank answer grid. Players figure out which letter belongs in each slot to reveal the quote.
* **Rebus Puzzle** — Each letter of a target word is clued by an image. Players identify the image, find the marked letter, and combine them to spell the answer.
* **Load Quotes** — Upload a `.txt` file of quotes and manage them with full CRUD support (Add, Remove, Replace).
* **Language Support** — English and Telugu quote libraries are managed and generated independently.
* **Difficulty Levels** — Easy (10x10), Normal (15x15), Hard (20x20) for Snake puzzles.
* **Column Width** — Adjustable column width for Drop Quote puzzles: 10, 15, 20, or 25.
* **Show / Hide Solution** — Toggle solution visibility before printing on all puzzle types.
* **Print to PDF** — Print any puzzle page directly from the browser with clean page breaks and puzzle numbers.
* **jQuery DataTable** — Searchable, sortable, paginated quote table on the Load Quotes page.

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python, Flask |
| **Frontend** | HTML, CSS, Bootstrap 5, Jinja2 |
| **JavaScript** | jQuery, DataTables |
| **Image APIs** | Pixabay REST API, HuggingFace FLUX.1-schnell |
| **Telugu API** | Ananya grapheme cluster API (jasthi.com) |
| **Data** | Plain text files (`quotes.txt`, `quotes_telugu.txt`) |
| **Version Control**| Git, GitHub |

## 📖 How to Use

### Load Quotes
1. Go to **Load Quotes** in the navbar.
2. Use the language toggle to switch between English and Telugu libraries.
3. Upload a `.txt` file with one quote per line to populate the library.
4. Use the Add, Remove, and Replace fields to manage individual quotes.
5. Use the search box above the table to filter quotes instantly.
> **Note:** Editing quotes automatically clears the puzzle cache so your next generated puzzle reflects the change.

### Snake Puzzle
1. Go to **Snakes** in the navbar.
2. Select a difficulty — Easy (10x10), Normal (15x15), or Hard (20x20).
3. Select a language — English or Telugu.
4. Each puzzle displays a grid with the quote hidden as a winding snake path.
5. Toggle **Solution** to *Revealed* to highlight the path before printing.
6. Click **Regenerate** to get a fresh set of puzzles.
7. Click **Print PDF** to print a clean puzzle book.

### Drop Quote Puzzle
1. Go to **Drop Quote** in the navbar.
2. Select a column width — 10, 15, 20, or 25.
3. Select a language — English or Telugu.
4. Toggle **Show Solution** to reveal or hide the answer cells.
5. Click **Regenerate** for a fresh set, or **Print PDF** to print.

### Rebus Puzzle
1. Go to **Rebus** in the navbar.
2. Type a word into the Word field, then click a count button (1, 10, 25, 50, or 100) to generate that many puzzles.
3. Or upload a `.txt` word list file and click **Upload** to generate one puzzle per word.
4. Use the **Solution** toggle to show or hide answer letters and the answer word.
5. Click **Print PDF** to print all puzzles.
> **Note:** The image source (Pixabay, HuggingFace, or Telugu) is set on the Settings page. Images are cached locally after the first fetch.

## 🖨️ Printing
* Click the **Print PDF** button on any puzzle page.
* In the browser print dialog, set Destination to **Save as PDF**.
* Each puzzle prints on its own page with its puzzle number.
* The navbar, preference bar, and solution toggles are hidden from the printed output.

## 📝 License
This project is licensed under the MIT License. See the `LICENSE` file for details.