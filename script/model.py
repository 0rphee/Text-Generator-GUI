from typing import Union
from nltk import WhitespaceTokenizer, FreqDist, trigrams
from collections import defaultdict
from random import choice, choices


class Trigrams:
    ending_chars = {".", "!", "?"}

    def __init__(self, tokens):
        frequency = FreqDist(tuple(trigrams(tokens)))
        self.trigram_freq = defaultdict(dict)
        for head_n_tail, num in frequency.items():
            head1, head2, tail = head_n_tail
            head_tup = (head1, head2)
            del head1, head2
            self.trigram_freq[head_tup][tail]: int = num

    def get_n_tail(self, head_input: list, single_tail: bool) -> Union[str, tuple]:
        head_input: tuple = tuple(head_input)
        try:
            tails, freqs = self.trigram_freq[head_input].keys(), self.trigram_freq[head_input].values()
            tails, freqs = tuple(tails), tuple(freqs)
            weighed_tail = choices(tails, freqs)[0]
            if single_tail:
                return weighed_tail
            else:
                pair_tail = list(zip(tails, freqs))
                pair_tail.sort(key=lambda x: x[1], reverse=True)
                return weighed_tail, pair_tail
        except Exception as my:
            return "not found"

    def get_initial_rand_head(self) -> list:  # gets rand word, recourses if not capitalized and with ending char
        rand_head: tuple = choice(list(self.trigram_freq.keys()))
        rand_head: str = " ".join(rand_head)
        is_capitalized = rand_head.capitalize() == rand_head and rand_head[0].isalpha()
        has_ending_char = rand_head[-1] in Trigrams.ending_chars
        return rand_head.split() if is_capitalized and not has_ending_char else self.get_initial_rand_head()

    def generate_line(self) -> list:
        text_line: list = self.get_initial_rand_head()
        while True:
            next_token = self.get_n_tail(text_line[-2:], True)
            text_line.append(next_token)
            if len(text_line) >= 5 and next_token[-1] in Trigrams.ending_chars:
                return text_line


def format_text_line(line: list) -> str:
    return " ".join(line) + "\n"


def process_trigrams() -> Trigrams:
    filename = "corpus.txt"
    with open(filename, "r", encoding="utf-8") as corpus:
        wtk = WhitespaceTokenizer()  # object that makes tokens
        return Trigrams(wtk.tokenize(corpus.read()))  # trigrams are generated from the tokenized results


def gen_txt_lines(n_lines: int, my_trigrams: Trigrams) -> str:
    text = []
    for _ in range(n_lines):
        text_line = format_text_line(my_trigrams.generate_line())
        text.append(text_line)
    return "".join(text)


def main():
    my_trigrams = process_trigrams()
    generated_text = gen_txt_lines(10, my_trigrams)  # todo what about transforming this into a method of Bigrams
    print(generated_text)


if __name__ == "__main__":
    main()
