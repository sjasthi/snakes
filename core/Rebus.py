import random
import requests
import os
from dotenv import load_dotenv
from data.word_bank import WORD_BANK, LETTER_INDEX


load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
IMAGE_FOLDER = "static/img/rebus"

def generate_image(word: str):
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    filepath = os.path.join(IMAGE_FOLDER, f"{word.lower()}.png")

    if os.path.exists(filepath):
        return filepath

    API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": f"a simple clear image of a {word.lower()}, white background, no text",
        "parameters": {
            "num_inference_steps": 4,
            "guidance_scale": 0.0
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Image saved for {word} HuggingFace")
        return filepath
    else:
        print(f"Failed for {word}: {response.status_code} — {response.text}")
        print(f"URL used: {API_URL}")
        return None

class Rebus:
    """
    Given a target word, find one clue word per letter.
    Each clue word contains that letter at a specific position.
    """

    def __init__(self, target_word: str, used_words: set = None):
        self.target_word = target_word.upper().strip()
        # track used word accross multiple puzzles
        self.used_words = used_words if used_words is not None else set()
        self.clues = self.generate_clues()

    def generate_clues(self):
        """
        For each letter in the target word, find a clue word
        that contains that letter.
        Returns a list of dicts with clue info.
        """
        clues = []

        # Track used word within puzzle
        used_within_puzzle = set()

        for letter in self.target_word:
            clue = self.find_clue_word(letter, used_within_puzzle)
            clues.append(clue)
            if clue["clue_word"]:
                used_within_puzzle.add(clue["clue_word"])
                self.used_words.add(clue["clue_word"])  # mark as used globally too
        return clues

    def find_clue_word(self, letter: str, used_within_puzzle: set):
        """
        Search the word bank for words containing the given letter.
        Pick one randomly and return the word, position, and length.
        """
        letter = letter.upper()
    
        # Get all candidates for this letter from the index
        all_candidates = LETTER_INDEX.get(letter, [])
        
        # Filter out already used words
        candidates = [
            c for c in all_candidates
            if c["clue_word"] not in used_within_puzzle
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
    result = generate_image("CAT")
    print(result)
