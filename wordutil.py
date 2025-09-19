import numpy as np

# Default characters for a black square in the puzzle and the turn character in the Tree structure
CH_EMPTY = '.'
CH_TURN = ','


# Returns True if list contains duplicates
def contains_duplicates(list):
    list_without_duplicates = np.unique(list)
    if len(list) == len(list_without_duplicates):
        return False
    elif len(list) > len(list_without_duplicates):
        return True
    else:
        print("panic")
        return True     # In case something goes wrong here, default to not accepting

# Writing or reading a word in the puzzle can start from any letter in the word.
# For example, if one word in the crossword puzzle contains an F, and we want to write CAFE from the F, then the string saved in the Tree structure is 'FE,AC'
# The F and E will be written normally (left to right), the C and A will be written right to left instead. The , marks the spot from where to switch.
# The Word Depth is the index where the last letter of the supplied *word* parameter will be written.
# For example, word_depth(F) = 0, word_depth(FE) = 1, word_depth(FE, A)=-1, word_depth(FE, AC) = -2
def word_depth(word):
    if word == "":
        return None
    count = -1
    turned = False
    for letter in word:
        if letter == CH_TURN:
            count = 0
            turned = True
            continue
        if turned:
            count -= 1
        else:
            count += 1
    return count


# Turns CAFE into CA,FE (for example)
def inject_character(string, character, pos):
    return string[:pos] + character + string[pos:]

# Turns CAFE into FE,AC (for example)
def inject_character_reverse_second_half(string, character, pos):
    return string[pos:] + character + string[:pos][::-1]

# Turns CAFE into [C,AFE   CA,FE   CAF,E]
def inject_everywhere(string, character=CH_TURN, reverse_second_half=False):
    all_strings = [string]
    for i in range(1, len(string)):
        if reverse_second_half:
            all_strings.append(inject_character_reverse_second_half(string, character, i))
        else:

            all_strings.append(inject_character(string, character, i))
    return all_strings
