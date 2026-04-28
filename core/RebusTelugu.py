import random
from data.word_bank import WORD_BANK_TELUGU
from core.Grid import ananya
from core.RebusPixabay import generate_image_pixabay


_cluster_cache = {}


# Saves time on API calls
def get_clusters_cached(word: str):
    if word not in _cluster_cache:
        _cluster_cache[word] = ananya(word)
    return _cluster_cache[word]

# ── Pre-build Telugu index at startup (same speed improvement as English) ──
def build_telugu_cluster_index():
    """
    Build a lookup dictionary mapping each cluster to all Telugu words
    containing that cluster, with position info.
    Called once at import time.
    """
    index = {}
    for telugu_word, english_word in WORD_BANK_TELUGU.items():
        word_clusters = get_clusters_cached(telugu_word)
        for i, cluster in enumerate(word_clusters):
            if cluster not in index:
                index[cluster] = []
            index[cluster].append({
                "clue_word":  telugu_word,
                "english":    english_word,
                "cluster":    cluster,
                "position":   i + 1,
                "length":     len(word_clusters),
                "hint":       f"{i + 1}/{len(word_clusters)}",
                "image":      None
            })
    return index

# Lazy load — only builds when first needed
_telugu_index = None

def get_telugu_index():
    global _telugu_index
    if _telugu_index is None:
        _telugu_index = build_telugu_cluster_index()
    return _telugu_index

class RebusTelugu:
    """
    Telugu Rebus generator using lusters from ananya() API.
    """

    def __init__(self, target_word: str, used_words: set = None):
        self.target_word = target_word.strip()
        self.clusters = get_clusters_cached(self.target_word)
        # used_words tracks Telugu words used across ALL puzzles
        self.used_words  = used_words if used_words is not None else set()
        self.clues = self.generate_clues()

    def generate_clues(self):
        clues = []
        # Track Telugu words used within THIS puzzle only
        used_in_this_puzzle = set()

        for cluster in self.clusters:
            clue = self.find_clue_word(cluster, used_in_this_puzzle)
            clues.append(clue)
            if clue["clue_word"]:
                used_in_this_puzzle.add(clue["clue_word"])
                self.used_words.add(clue["clue_word"])  # mark globally too
        return clues

    def find_clue_word(self, cluster: str, used_in_this_puzzle: set):
        """
        O(1) lookup using pre-built index.
        Skips words already used in this puzzle or across all puzzles.
        """
        all_candidates = get_telugu_index().get(cluster, [])

        # Filter out already used words
        candidates = [
            c for c in all_candidates
            if c["clue_word"] not in used_in_this_puzzle
            and c["clue_word"] not in self.used_words
        ]

        if candidates:
            return random.choice(candidates)

        # Fallback — allow reuse if word bank exhausted for this cluster
        print(f"Warning: No unique Telugu word found for cluster '{cluster}', allowing reuse.")
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

    def attach_images(self, image_func):
        for clue in self.clues:
            if clue["english"]:
                clue["image"] = image_func(clue["english"])

    def to_dict(self):
        return {
            "target_word": self.target_word,
            "clusters": self.clusters,
            "clues": self.clues
        }


if __name__ == "__main__":
    rebus = RebusTelugu("తిమింగలం")
    rebus.attach_images(generate_image_pixabay)

    print(rebus.to_dict())