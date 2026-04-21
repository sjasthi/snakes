import random
import requests
import os
from dotenv import load_dotenv
from data.word_bank import WORD_BANK, LETTER_INDEX

load_dotenv()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_FOLDER = os.path.join(BASE_DIR, "static", "img", "rebus")



def generate_image_pixabay(english_word: str):
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    filepath = os.path.join(IMAGE_FOLDER, f"{english_word.lower()}.png")

    if os.path.exists(filepath):
        return filepath

    params = {
        "key": PIXABAY_API_KEY,
        "q": english_word,
        "image_type": "photo",
        "per_page": 10,
        "safesearch": "true"
    }

    response = requests.get("https://pixabay.com/api/", params=params)
    hits = response.json().get("hits", [])

    if not hits:
        return None

    image_url = random.choice(hits).get("webformatURL")
    img = requests.get(image_url)

    if img.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(img.content)
            print(f"Image saved for {english_word} Pixabay")
        return filepath

    return None


class RebusPixabay:
    """
    Given a target word, find one clue word per letter.
    Each clue word contains that letter at a specific position.
    """

    def __init__(self, target_word: str, used_words: set = None):
        self.target_word = target_word.upper().strip()
        self.used_words = used_words if used_words is not None else set()
        self.clues = self.generate_clues()

    def generate_clues(self):
        clues = []
        used_in_this_puzzle = set()

        for letter in self.target_word:
            clue = self.find_clue_word(letter, used_in_this_puzzle)
            clues.append(clue)
            if clue["clue_word"]:
                used_in_this_puzzle.add(clue["clue_word"])
                self.used_words.add(clue["clue_word"])
        return clues

    def find_clue_word(self, letter: str, used_in_this_puzzle: set):
        letter = letter.upper()
        
        # Get all candidates for this letter from the index
        all_candidates = LETTER_INDEX.get(letter, [])
        
        # Filter out already used words
        candidates = [
            c for c in all_candidates
            if c["clue_word"] not in used_in_this_puzzle
            and c["clue_word"] not in self.used_words
        ]
        
        if candidates:
            return random.choice(candidates)
        
        # Fallback — word bank exhausted, allow reuse
        print(f"Warning: No unique word found for '{letter}', allowing reuse.")
        if all_candidates:
            return random.choice(all_candidates)
        
        return {
            "clue_word": None,
            "letter": letter,
            "position": None,
            "length": None,
            "hint": "?"
        }

    def to_dict(self):
        return {
            "target_word": self.target_word,
            "clues": self.clues
        }


if __name__ == '__main__':
    result = generate_image_pixabay("dog")
    print(result)
