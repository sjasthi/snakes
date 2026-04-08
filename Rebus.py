import random
import requests
import os
from dotenv import load_dotenv
from word_bank import WORD_BANK

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

    def __init__(self, target_word: str):
        self.target_word = target_word.upper().strip()
        self.clues = self.generate_clues()

    def generate_clues(self):
        """
        For each letter in the target word, find a clue word
        that contains that letter.
        Returns a list of dicts with clue info.
        """
        clues = []
        for letter in self.target_word:
            clue = self.find_clue_word(letter)
            clues.append(clue)
        return clues

    def find_clue_word(self, letter: str):
        """
        Search the word bank for words containing the given letter.
        Pick one randomly and return the word, position, and length.
        """
        candidates = []
        for word in WORD_BANK:
            for i, ch in enumerate(word.upper()):
                if ch == letter.upper():
                    candidates.append({
                        "clue_word": word,
                        "letter": letter.upper(),
                        "position": i + 1,       # 1-based position
                        "length": len(word),
                        "hint": f"{i + 1}/{len(word)}"
                    })

        if candidates:
            return random.choice(candidates)
        else:
            # Fallback if no word found for that letter
            return {
                "clue_word": None,
                "letter": letter.upper(),
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
