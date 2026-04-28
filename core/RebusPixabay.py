import random
import requests
import os
from dotenv import load_dotenv
from core.RebusBase import RebusBase

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

    try:
        response = requests.get("https://pixabay.com/api/", params=params, timeout=10)
        response.raise_for_status()
        hits = response.json().get("hits", [])

        if not hits:
            return None

        image_url = random.choice(hits).get("webformatURL")
        img = requests.get(image_url, timeout=10)

        if img.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(img.content)
                print(f"Image saved for {english_word} Pixabay")
            return filepath
    except Exception as e:
        print(f"Warning: Pixabay image fetch failed for '{english_word}': {e}")

    return None


class RebusPixabay(RebusBase):
    """Rebus puzzle generator — images sourced from Pixabay (real photos)."""
    pass


if __name__ == '__main__':
    result = generate_image_pixabay("dog")
    print(result)
