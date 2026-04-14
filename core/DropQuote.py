import random
import unicodedata
from core.Grid import ananya


def is_text_cluster(cluster):
    return all(unicodedata.category(ch)[0] in ("L", "M") for ch in cluster)


class DropQuote:
    def __init__(self, quote: str, width: int = 20):
        self.width = width
        self.quote = ananya(quote)
        self.columns = [self.letters_in_column(i) for i in range(self.width)]

    def split_quote(self):
        rows = []
        row = []

        for i, cluster in enumerate(self.quote, start=1):

            # End of row
            if i % self.width == 0:
                if is_text_cluster(cluster):
                    row.append('_')
                else:
                    row.append(cluster)
                rows.append("".join(row))
                row = []
                continue

            # Inside row
            if cluster == ' ':
                row.append(' ')
            elif is_text_cluster(cluster):
                row.append('_')
            else:
                row.append(cluster)

        if row:
            rows.append("".join(row))

        return rows

    def letters_in_column(self, col):
        letters = [
            ch.upper() if ch.isascii() else ch
            for ch in self.quote[col::self.width]  # start:stop:step
            if is_text_cluster(ch)
        ]

        random.shuffle(letters)
        return letters


if __name__ == '__main__':
    q = "బాల్యన్ని మించిన బడిలేదు కుతూహలాన్ని మించిన గురువు లేడు."
    q1 = "We're going up, up, up, it's our moment. You know together we're glowing. Gonna be, gonna be Golden."

    d = DropQuote(q1)

    for row in d.split_quote():
        print(*row)

    for column in d.columns:
        print(column)
    print(ananya(q))
