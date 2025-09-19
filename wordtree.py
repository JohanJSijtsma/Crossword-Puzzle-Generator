import numpy as np
import random
import wordutil


# A Node contains one letter (or a turn symbol) and a list of children.
# The boolean end sgnifies if this Node could be the end of a word. For example,
# when traveling down the tree from LOIRE and this is the E Node, then self.end is True because LOIRE is a word, but
# it still has children. For example the T, because LOIRET is also stored in the tree structure
class Node:
    def __init__(self, letter='*'):
        self.letter = letter
        self.end = False
        self.children = []

    def set_letter(self, letter):
        self.letter = letter

    # Recursively adds a new word to the tree structure.
    def add_word(self, word_to_add):
        # When the end of the word is reached, designate this Node as a possible end point
        if len(word_to_add) <= 0:
            self.end = True
            return True

        # Check if the first letter of the word already exists among the children, if so continue
        # adding the rest of the word in that branch of the tree structure
        new_letter = word_to_add[0]
        for c in self.children:
            if c.letter == new_letter:
                return c.add_word(word_to_add[1:])          # early exit if word can be added to an existing branch
        # If no branch exists with the initial letter of the to be added word, create a node for that letter,
        # and continue adding the rest of the word from there
        new_node = Node(new_letter)
        result = new_node.add_word(word_to_add[1:])

        self.children.append(new_node)
        return result


    def get_random_word(self, prepend=True):
        if len(self.children) == 0:
            return self.letter
        else:
            if self.letter == wordutil.CH_TURN:
                return random.choice(self.children).get_random_word(False)
            else:
                if prepend:
                    return self.letter + random.choice(self.children).get_random_word(prepend)
                else:
                    return random.choice(self.children).get_random_word(prepend) + self.letter

    # Returns True when this Node's letter can fit on a certain square
    def letter_fits(self, puzzle, x, y):
        result = self.letter == puzzle[x, y] or puzzle[x, y] == wordutil.CH_EMPTY
        return result

    # (unused) Returns True when the spot below and above that square are empty (or out of bounds)
    def does_not_interfere(self, puzzle, x, y):
        above = y-1 < 0 or puzzle[x, y-1] == wordutil.CH_EMPTY
        below = y+1 > len(puzzle) or puzzle[x, y-1] == wordutil.CH_EMPTY
        return above and below

    # Eventually returns a list of all words that could fit on a specific square
    # Found word are collected in the list found_words, while current_word is the path that was traversed to get to this node.
    def find_words(self, current_word, found_words, puzzle, x, y):
        current_word += self.letter
        index = wordutil.word_depth(current_word)

        if index is None:
            for c in self.children:
                print("You're not supposed to be here")
            return

        # Stop when out of range
        if x+index > len(puzzle)-1 or x+index < 0:
            return

        # When this Node's letter still fits in the puzzle, continue searching. If this Node is an end-node, add the word collected so far to the list
        if self.letter_fits(puzzle, x + index, y) or self.letter == wordutil.CH_TURN:#and self.does_not_interfere(puzzle, x + index, y):
            # add word
            if self.end:
                found_words.append(current_word)
                #print("Word found, adding \"" + current_word + "\" to list")

            # Continue searching
            for c in self.children:
                c.find_words(current_word, found_words, puzzle, x, y)
        else:
            return

    def __str__(self):
        string = self.letter
        if len(self.children) <= 0:
            return string + "."
        elif len(self.children) == 1:
            return string
        else:
            for c in self.children:
                string += str(c) + "\n"
            return string

    def print(self, depth=0):
        string = self.letter
        if len(self.children) <= 0:
            return string + ".\n"

        string += self.children[0].print(depth+1)

        for c in self.children[1:]:
            string += "-" + " " * depth + c.print(depth+1)
        return string

# Tree structure that makes it much faster to find which words can fit in a puzzle than a lookup from a linear list
# This tree contains initial Nodes for all initial letters from words that were added.
class Tree:
    def __init__(self):
        self.initial_nodes = []

    def get_random_word(self):
        return random.choice(self.initial_nodes).get_random_word()

    # Finds all words that could fit in a certain square.
    # Words are collected in the 'words' list.
    def find_words(self, puzzle, x, y):
        words = []
        current_word = ""
        for n in self.initial_nodes:
            n.find_words(current_word, words, puzzle, x, y)
        return words

    # Add a word to the structure. If the first letter is not yet in the list of initial nodes, add it.
    def add_word(self, new_word):
        for n in self.initial_nodes:
            if n.letter==new_word[0]:
                return n.add_word(new_word[1:])
        new_node = Node(new_word[0])
        result = new_node.add_word(new_word[1:])
        self.initial_nodes.append(new_node)
        return result

    def __str__(self):
        string = ""
        for n in self.initial_nodes:
            string += n.print() + "\n"
        return string
