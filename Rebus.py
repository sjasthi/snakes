import os
import random


class Rebus:
    def __init__(self, word):
        self.word = word
        self.results = []
        self.WORD_BANK = {
            'a': ["apple", "astronaut", "ant"],
            'b': ["banana", "boat", "bear"],
            'c': ["cat", "castle", "candle"],
            'd': ["dog", "dragon", "desk"],
            'e': ["egg", "eagle", "engine"],
            'f': ["fish", "forest", "fork"],
            'g': ["goat", "garden", "ghost"],
            'h': ["house", "horse", "hat"],
            'i': ["ice", "island", "igloo"],
            'j': ["jungle", "jacket", "jar"],
            'k': ["kite", "kangaroo", "key"],
            'l': ["lion", "lamp", "leaf"],
            'm': ["music", "mountain", "mouse"],
            'n': ["nest", "ninja", "nose"],
            'o': ["orc", "orange", "ocean"],
            'p': ["pizza", "piano", "pumpkin"],
            'q': ["queen", "quilt", "quail"],
            'r': ["robot", "river", "rose"],
            's': ["snake", "sun", "shark"],
            't': ["tower", "tiger", "tree"],
            'u': ["umbrella", "unicorn", "urn"],
            'v': ["vase", "violin", "village"],
            'w': ["whale", "window", "wolf"],
            'x': ["xylophone", "x-ray"],
            'y': ["yacht", "yak", "yarn"],
            'z': ["zebra", "zoo", "zipper"]
        }

        self.play_game()

    def generate_word(self, letter):
        return random.choice(self.WORD_BANK[letter.lower()])

    def count_matches(self, word, original):
        return len(set(word.lower()) & set(self.word.lower()))

    def get_image(self, word):
        folder = "static/images"
        possible_exts = [".png", ".jpg", ".jpeg", ".webp", ".gif"]

        for ext in possible_exts:
            path = os.path.join(folder, word + ext)
            if os.path.exists(path):
                return "images/" + word + ext

        return None

    def play_game(self):
        total_letters = len(self.word)

        for letter in self.word:
            generated = self.generate_word(letter)
            matches = self.count_matches(generated, self.word)
            image_file = self.get_image(generated)

            self.results.append({
                "image": image_file,
                "matches": matches,
                "total": total_letters
            })


if __name__ == "__main__":
    p = Rebus('octopus')
    for i in p.results:
        print(f"{i.get('generated')} {i.get('matches')}/{i.get('total')}")
