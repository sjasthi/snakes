import random
import unicodedata
from data.word_bank import WORD_BANK_TELUGU
from core.RebusPixabay import generate_image_pixabay


def split_telugu_clusters(word: str) -> list:
    """
    Split a Telugu word into grapheme clusters without calling any external API.
    Combines a base character with any following combining marks (vowel signs, etc).
    """
    clusters = []
    current  = ""
    for ch in word:
        cat = unicodedata.category(ch)
        # Mn = Non-spacing mark (vowel signs like ా, ి, etc.)
        # Mc = Spacing combining mark
        # Me = Enclosing mark
        if cat in ("Mn", "Mc", "Me") and current:
            current += ch
        else:
            if current:
                clusters.append(current)
            current = ch
    if current:
        clusters.append(current)
    return clusters


# ── Pre-build Telugu cluster index at import time (no API calls) ──────────────

def build_telugu_cluster_index() -> dict:
    index = {}
    for telugu_word, english_word in WORD_BANK_TELUGU.items():
        clusters = split_telugu_clusters(telugu_word)
        for i, cluster in enumerate(clusters):
            if cluster not in index:
                index[cluster] = []
            index[cluster].append({
                "clue_word": telugu_word,
                "english":   english_word,
                "cluster":   cluster,
                "position":  i + 1,
                "length":    len(clusters),
                "hint":      f"{i + 1}/{len(clusters)}",
                "image":     None
            })
    return index


TELUGU_INDEX = build_telugu_cluster_index()


class RebusTelugu:
    """Telugu Rebus generator — no external API calls during puzzle construction."""

    def __init__(self, target_word: str, used_words: set = None):
        self.target_word = target_word.strip()
        self.clusters    = split_telugu_clusters(self.target_word)
        self.used_words  = used_words if used_words is not None else set()
        self.clues       = self.generate_clues()

    def generate_clues(self):
        clues               = []
        used_in_this_puzzle = set()

        for cluster in self.clusters:
            clue = self.find_clue_word(cluster, used_in_this_puzzle)
            clues.append(clue)
            if clue["clue_word"]:
                used_in_this_puzzle.add(clue["clue_word"])
                self.used_words.add(clue["clue_word"])
        return clues

    def find_clue_word(self, cluster: str, used_in_this_puzzle: set):
        all_candidates = TELUGU_INDEX.get(cluster, [])

        candidates = [
            c for c in all_candidates
            if c["clue_word"] not in used_in_this_puzzle
            and c["clue_word"] not in self.used_words
        ]

        if candidates:
            return random.choice(candidates)

        print(f"Warning: No unique Telugu word for cluster '{cluster}', allowing reuse.")
        if all_candidates:
            return random.choice(all_candidates)

        return {
            "clue_word": None,
            "english":   None,
            "cluster":   cluster,
            "position":  None,
            "length":    None,
            "hint":      "?",
            "image":     None
        }

    def to_dict(self):
        return {
            "target_word": self.target_word,
            "clusters":    self.clusters,
            "clues":       self.clues
        }


if __name__ == "__main__":
    rebus = RebusTelugu("తిమింగలం")
    print(rebus.to_dict())