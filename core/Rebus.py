import requests
import os
from dotenv import load_dotenv
from core.RebusBase import RebusBase


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

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"Image saved for {word} HuggingFace")
            return filepath
        else:
            print(f"Failed for {word}: {response.status_code} — {response.text}")
    except Exception as e:
        print(f"Warning: HuggingFace image fetch failed for '{word}': {e}")

    return None


class Rebus(RebusBase):
    """Rebus puzzle generator — images sourced from HuggingFace (AI-generated)."""
    pass


if __name__ == '__main__':
    result = generate_image("CAT")
    print(result)
