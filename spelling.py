"""
Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html

Copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php

Refactored by Trevor Beers
"""

import re
from collections import Counter


# In practice, we would use a Moonpig-specific corpus, e.g. product titles/descriptions/tags
with open("corpus.txt") as f:
    file = f.read()

words_list = re.findall(r"\w+", file.lower())
WORDS = Counter(words_list)


def generate_1_edit(word: str) -> set[str]:
    """Generate candidates that are 1 edit away from the word."""

    letters = "abcdefghijklmnopqrstuvwxyz"
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    deletions = [L + R[1:] for L, R in splits if R]
    transpositions = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    substitutions = [L + c + R[1:] for L, R in splits if R for c in letters]
    insertions = [L + c + R for L, R in splits for c in letters]

    return set(deletions + transpositions + substitutions + insertions)


def generate_2_edits(word: str) -> set[str]:
    """Generate candidates that are 2 edits away from the word."""

    edits_list = set()
    # Add one edit
    for e1 in generate_1_edit(word):
        # Add second edit
        edits_list |= generate_1_edit(e1)
    return edits_list


def filter_words(words: set[str]) -> list[str]:
    return list(set(w for w in words if w in WORDS))


def correct_spelling(word: str) -> str:
    """Find the most probable spelling correction for the word."""

    word = word.lower()

    # If the input is already a correctly spelled word, return it
    if word in WORDS:
        candidates = [word]

    # Try to find valid words within 1 edit of the input
    elif word_list := filter_words(generate_1_edit(word)):
        candidates = word_list

    # Try to find valid words within 2 edits of the input
    elif word_list := filter_words(generate_2_edits(word)):
        candidates = word_list

    else:
        candidates = [word]

    # Choose candidate that shows up most in the corpus
    return max(candidates, key=lambda w: WORDS[w] / sum(WORDS.values()))


if __name__ == "__main__":
    print(correct_spelling("ya"))
