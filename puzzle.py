import numpy as np
import wordutil


def generate_empty_puzzle(n, m):
    return  np.char.array([[wordutil.CH_EMPTY] * n] * m)


def add_word(puzzle, word, x, y):
    # Add a word to a puzzle, and return a list of squares where letters were added
    coords = []
    for i in range(len(word)):
        # The word_depth function calculates the x coordinate where the letter will be written
        index = wordutil.word_depth(word[:i + 1])

        next_letter = word[:i + 1][-1]
        if not next_letter == wordutil.CH_TURN:
            puzzle[x + index][y] = next_letter
            coords.append((x + index, y))
    return coords


def get_words_from_line(line):
    words = []
    word = ""
    for l in line:
        if l == wordutil.CH_EMPTY:  # Once we reach an empty the word ends
            if len(word) == 1:      # If the word we are building is only one character long, it was only passing from another dimension and we ignore it
                word = ""
            if len(word) > 1:       # If the word is longer than one character we add it to the list
                words.append(word)
                word = ""
            if len(word) == 0:      # Previous letter was also empty, so no word
                pass
        else:
            word = word + l
    # At the end of the line also add the word (unless it was passing)
    if len(word) > 1:
        words.append(word)

    return words


def get_horizontal_words(puzzle):
    words = []
    for row in puzzle:
        words.extend(get_words_from_line(row))
    return words


def get_vertical_words(puzzle):
    words = get_horizontal_words(puzzle.T)
    return words


def get_words(puzzle):
    words = get_horizontal_words(puzzle)
    words.extend(get_vertical_words(puzzle))
    return words


def calculate_density(puzzle, printout=False):
    total_squares = 0
    filled_squares = 0
    for y in puzzle:
        for x in y:
            total_squares += 1
            if x != wordutil.CH_EMPTY:
                filled_squares += 1

    density = filled_squares / total_squares
    if printout:
        print("height:", len(puzzle))
        print("width:", len(puzzle[0]))
        print("total cells:", total_squares)
        print("total filled:", filled_squares)
        print("density:", density)
    return density


def count_questions(puzzle, printout=False):
    count = len(get_words(puzzle))
    if printout:
        print("questions:", count)
    return count
