import random
import requests
import os
from dotenv import load_dotenv
from word_bank import WORD_BANK

load_dotenv()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
IMAGE_FOLDER = "static/img/rebus"


def generate_image_pixabay(word: str):
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    filepath = os.path.join(IMAGE_FOLDER, f"{word.lower()}.png")

    # Return cached image if it exists
    if os.path.exists(filepath):
        return filepath

    api_url = "https://pixabay.com/api/"

    params = {
        "key": PIXABAY_API_KEY,
        "q": word.lower(),
        "image_type": "photo",
        "per_page": 10,
        "safesearch": "true"
    }

    response = requests.get(api_url, params=params)

    if response.status_code != 200:
        print(f"Pixabay request failed: {response.status_code} — {response.text}")
        return None

    data = response.json()
    hits = data.get("hits", [])

    if not hits:
        print(f"No images found for {word}")
        return None

    # Pick a random image
    image_data = random.choice(hits)
    image_url = image_data.get("webformatURL")

    try:
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(img_response.content)
            print(f"Image saved for {word} Pixabay")
            return filepath
        else:
            print(f"Failed to download image: {img_response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None


class RebusPixabay:
    """
    Given a target word, find one clue word per letter.
    Each clue word contains that letter at a specific position.
    """

    def __init__(self, target_word: str):
        self.target_word = target_word.upper().strip()
        self.clues = self.generate_clues()

    def generate_clues(self):
        clues = []
        for letter in self.target_word:
            clue = self.find_clue_word(letter)
            clues.append(clue)
        return clues

    def find_clue_word(self, letter: str):
        candidates = []
        for word in WORD_BANK:
            for i, ch in enumerate(word.upper()):
                if ch == letter.upper():
                    candidates.append({
                        "clue_word": word,
                        "letter": letter.upper(),
                        "position": i + 1,
                        "length": len(word),
                        "hint": f"{i + 1}/{len(word)}"
                    })

        if candidates:
            return random.choice(candidates)
        else:
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
    result = generate_image_pixabay("dog")
    print(result)
