import random
from data.word_bank import LETTER_INDEX


class RebusBase:
    """
    Shared base class for English Rebus puzzle generators (HuggingFace and Pixabay variants).
    Subclasses differ only in which image-generation backend they use.
    """

    def __init__(self, target_word: str, used_words: set = None):
        self.target_word = target_word.upper().strip()
        # Track used words across multiple puzzles (passed in by caller)
        self.used_words = used_words if used_words is not None else set()
        self.clues = self.generate_clues()

    def generate_clues(self):
        """
        For each letter in the target word, find a unique clue word
        that contains that letter. Returns a list of clue dicts.
        """
        clues = []
        used_within_puzzle = set()

        for letter in self.target_word:
            clue = self.find_clue_word(letter, used_within_puzzle)
            clues.append(clue)
            if clue["clue_word"]:
                used_within_puzzle.add(clue["clue_word"])
                self.used_words.add(clue["clue_word"])
        return clues

    def find_clue_word(self, letter: str, used_within_puzzle: set):
        """
        O(1) lookup via LETTER_INDEX. Prefers words not yet used in this
        puzzle or globally. Falls back to reuse if the word bank is exhausted.
        """
        letter = letter.upper()
        all_candidates = LETTER_INDEX.get(letter, [])

        candidates = [
            c for c in all_candidates
            if c["clue_word"] not in used_within_puzzle
            and c["clue_word"] not in self.used_words
        ]

        if candidates:
            return random.choice(candidates)

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
