import random


class DropQuote:
    def __init__(self, quote: str):
        self.width = 20
        self.quote = quote.upper()
        self.columns = [self.letters_in_column(i) for i in range(self.width)]

    # def split_quote(self):
    #     for i, letter in enumerate(self.quote, start=1):
    #         if i % self.width == 0 and not letter.isalnum():
    #             print(letter)
    #         elif i % self.width == 0 and letter.isalnum():
    #             print('_')
    #             # print(letter)
    #         elif letter == ' ':
    #             print(letter, end='')
    #         else:
    #             print('_', end='')
    #             # print(letter, end='')

    def split_quote(self):
        rows = []
        row = []

        for i, letter in enumerate(self.quote, start=1):

            # End of row
            if i % self.width == 0:
                if letter.isalnum():
                    row.append('_')
                else:
                    row.append(letter)
                rows.append("".join(row))
                row = []
                continue

            # Inside a row
            if letter == ' ':
                row.append(' ')
            elif letter.isalnum():
                row.append('_')
            else:
                row.append(letter)

        if row:
            rows.append("".join(row))

        return rows

    def letters_in_column(self, col):
        letters = [
                ch
                for ch in self.quote[col::self.width]   # start:stop:step
                if ch.isalnum()
            ]

        random.shuffle(letters)
        return letters


if __name__ == '__main__':
    q = 'Everybody has a plan till they get punched in the face'
    q1 = "We're going up, up, up, it's our moment. You know together we're glowing. Gonna be, gonna be Golden."

    d = DropQuote(q1)

    for row in d.split_quote():
        print(*row)

    for column in d.columns:
        print(column)
    # print(len(d.columns))