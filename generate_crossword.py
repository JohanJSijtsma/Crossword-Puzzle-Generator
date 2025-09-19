import random
import sys
from puzzle import *
from wordtree import Tree
import wordutil

WIDTH = 13
HEIGHT = 13

example_puzzle = [['L','O','T','.','.','.','H','E','R','A','U','L','T'],
                  ['O','.','.','H','.','.','.','.','.','L','.','O','.'],
                  ['I','.','.','A','.','C','.','.','.','L','.','Z','.'],
                  ['R','.','J','U','R','A','.','.','.','I','.','E','.'],
                  ['E','.','.','T','.','N','.','.','.','E','.','R','.'],
                  ['T','.','.','E','.','T','.','M','A','R','N','E','.'],
                  ['C','.','.','M','.','A','.','.','R','.','.','.','V'],
                  ['H','.','.','A','.','L','A','N','D','E','S','.','E'],
                  ['E','.','.','R','.','.','I','.','E','.','A','.','R'],
                  ['R','E','U','N','I','O','N','.','N','O','R','D','.'],
                  ['.','U','.','E','.','.','.','.','N','.','T','.','.'],
                  ['.','R','.','.','.','A','R','D','E','C','H','E','.'],
                  ['M','E','U','S','E','.','.','.','S','.','E','.','.']]

list_of_allowed_words = []


def get_allowed_words(wordsfile):
    # Read all lines from the provided file.
    words = []
    file = open(wordsfile)
    for line in file:
        words.append(line.strip().upper())
    return words


def verify(puzzle) -> bool:
    # A puzzle is an N by M grid, with each grid containing either an emtpy or a letter from the alphabet

    # A word is a sequence of letters, either horizontally left to right or vertically top to bottom,
    # Uninterrupted by an empty.
    words = get_words(puzzle)

    #print("in verify", list_of_allowed_words)

    #All words are from the provided list
    for word in words:
        if word not in list_of_allowed_words:
            #print(str(word) + " not foound in list of allowed words", list_of_allowed_words)
            return False

    #All words occur at most once
    if wordutil.contains_duplicates(words):
        return False

    return True


def add_random_word_in_spot(coord, wordlist:Tree, current_puzzle):
    # Find words that could possibly fit on the specified square.
    # Currently does not take into account interference from other rows (if the word is going horizontally) or columns (if vertically).
    # This is why we still verify if the word added results in a valid puzzle.
    candidates = wordlist.find_words(current_puzzle, coord[0], coord[1])
    random.shuffle(candidates)

    for c in candidates:
        temp_puzzle = current_puzzle.copy()
        add_word(temp_puzzle, c, coord[0], coord[1])

        # After the new word is added to a temporary puzzle, check if the result is valid, and that the result is different (so we don't end up in a loop of adding the same word time and time again).
        # If so add the word the the real puzzle
        if verify(temp_puzzle) and not np.array_equal(temp_puzzle, current_puzzle):
            coords = add_word(current_puzzle, c, coord[0], coord[1])
            return coords
    return []


# An older function that generates a puzzle, not by trying to add words to sqaures with letters but to all squares in a random order, takes a lot longer and does not guarantee a connected puzzle
def generate_puzzle_random(n, m, wordlist:Tree):
    puzzle = generate_empty_puzzle(n, m)
    all_coords = [(x, y) for x in range(n) for y in range(m)]
    random.shuffle(all_coords)
    for coords in all_coords:
        new_coords =  add_random_word_in_spot(coords, wordlist, puzzle)
        if new_coords == []:
            add_random_word_in_spot((coords[1], coords[0]), wordlist, puzzle.T)


def generate_puzzle(n, m, wordlist:Tree):
    puzzle = generate_empty_puzzle(n, m)
    coords = {(random.randrange(0, m-1), random.randrange(0, n-1))}

    # Starting from one random square. Pick on square where a letter was added, add a random word there if possible, and then move to the next square.
    # Repeat this until all squares with letters have been tried.
    while len(coords)>0:
        c = coords.pop()
        # First try to add a word over one axis
        new_coords = add_random_word_in_spot(c, wordlist, puzzle)
        if new_coords == []:
            # Then transpose the puzzle to try the other axis.
            new_coords = add_random_word_in_spot((c[1], c[0]), wordlist, puzzle.T)
            # The squares of the added word are from the transposed puzzle, so we swap the x and y values.
            new_coords = [(y, x) for (x, y) in new_coords]
        if new_coords!=[]:
            coords.update(new_coords)

    return puzzle


def report_puzzle(puzzle):
    print(puzzle)
    print("Puzzle Attributes:")
    calculate_density(puzzle, printout=True)
    count_questions(puzzle, printout=True)


def research_function(w , h, tries, wordlist:Tree):
    max_d = generate_empty_puzzle(w, h)
    max_q = generate_empty_puzzle(w, h)

    for i in range(tries):
        if i % 10 == 0:
            print("try", i+1)

        fresh_puzzle = generate_puzzle(w, h, wordlist)

        # Overwrite the currently found densest or questionest puzzle if the are more dense or have more questions
        if calculate_density(max_d) < calculate_density(fresh_puzzle):
            max_d = fresh_puzzle
        if count_questions(fresh_puzzle) > count_questions(max_q):
            max_q = fresh_puzzle

    print("RESULTS AFTER", tries, "TRIES")
    print("MAX DENSITY FOUND:")
    report_puzzle(max_d)
    print("MAX QUESTIONS FOUND:")
    report_puzzle(max_q)


def main():
    global list_of_allowed_words
    global WIDTH
    global HEIGHT

    # Get arguments
    if len(sys.argv) > 2:
        WIDTH = int(sys.argv[1])
        HEIGHT = int(sys.argv[2])

    tries = 1
    filename = "dictionary.txt"
    if len(sys.argv)>3:
        filename = sys.argv[3]
    if len(sys.argv) > 4:
        tries = int(sys.argv[4])

    # Get allowed words from the provided file
    list_of_allowed_words = get_allowed_words(filename)

    # Turn the list of words into the Tree data-structure
    # We inject a TURN character into the word. We do this for all possible locations within each word
    wordtree = Tree()
    for word in list_of_allowed_words:
        for modified_word in wordutil.inject_everywhere(word, wordutil.CH_TURN, reverse_second_half=True):
            wordtree.add_word(modified_word.upper())

    # Perform the research. Find the densest and find the most questionest puzzle
    research_function(WIDTH, HEIGHT, tries, wordtree)


if __name__ == '__main__':
    main()
