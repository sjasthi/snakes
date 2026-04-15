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


class RebusTelugu:
    """
    Telugu Rebus generator using lusters from ananya() API.
    """

    def __init__(self, target_word: str):
        self.target_word = target_word.strip()
        self.clusters = get_clusters_cached(self.target_word)
        self.clues = self.generate_clues()

    def generate_clues(self):
        clues = []
        for cluster in self.clusters:
            clue = self.find_clue_word(cluster)
            clues.append(clue)
        return clues

    def find_clue_word(self, cluster: str):
        candidates = []

        for telugu_word, english_word in WORD_BANK_TELUGU.items():
            word_clusters = get_clusters_cached(telugu_word)

            for i, wc in enumerate(word_clusters):
                if wc == cluster:
                    candidates.append({
                        "clue_word": telugu_word,
                        "english": english_word,
                        "cluster": cluster,
                        "position": i + 1,
                        "length": len(word_clusters),
                        "hint": f"{i + 1}/{len(word_clusters)}",
                        "image": None
                    })

        if candidates:
            return random.choice(candidates)

        return {
            "clue_word": None,
            "english": None,
            "cluster": cluster,
            "position": None,
            "length": None,
            "hint": "?",
            "image": None
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