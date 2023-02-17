# Author: Ben Lehrburger
# Date: 2/12/23
# Purpose: play the NYT Spelling Bee from your terminal

import random
import re

# REPLACE WITH YOUR OWN FILE PATH
PATH = 'YOUR_PATH_HERE'

# Print intro messages
print('\nWelcome to the Spelling Bee (terminal version)!\n')
print('Please allow a few moments to generate a completely new game.'
      ' This can sometimes take up to two minutes depending on the complexity of the starting letters.\n')
print('The controls for this game are as follows:\n')
print('Enter S for score info')
print('Enter W to see correct words')
print('Enter L for puzzle letters')
print('Enter C for controls')
print('Enter N to start new game')
print('Enter Q to quit game\n')

# Create an array of all valid words
valid_words_path = f'{PATH}validWords.txt'
valid_words_file = open(valid_words_path)
valid_words = []

for line in valid_words_file:

    this_word = ''.join(re.findall(r'\w+', line))

    if len(this_word) >= 4:
        valid_words.append(this_word)


alphabet = 'abcdefghijklmnopqrtuvwxyz'
alphabet = [*alphabet]

loading_messages = ['Simulating letter combos...', 'Contacting New York Times...', 'Checking panagrams...',
                    'Picking center letter...', 'Calculating point values...', 'Verifying difficulty...']


# Generate a new Spelling Bee game
# Base Case: no panagrams found
# Returns: successful game with letters, center, words, and panagrams
def generate_game():

    this_puzzle = None
    panagrams = []
    words = []

    vowel_present = False
    vowels = ['a', 'e', 'i', 'o', 'u']

    # Generate new puzzle letters until it has vowels
    while vowel_present is False:

        this_puzzle = random.sample(alphabet, 7)

        for vowel in vowels:

            if vowel in this_puzzle:
                vowel_present = True

    center_letter = random.choice(this_puzzle)
    word_index = 0

    # Check every valid word against puzzle letters
    while word_index < len(valid_words):

        word = valid_words[word_index]

        # Disregard word if no center letter
        if center_letter not in word:
            word_index += 1

        else:

            mutable_puzzle_letters = this_puzzle.copy()
            remaining_letters = word

            # Iterate over each letter in the valid word to see if it fits the puzzle
            for letter in word:

                if letter in this_puzzle:
                    remaining_letters = remaining_letters[1:]

                    if letter in mutable_puzzle_letters:
                        mutable_puzzle_letters.remove(letter)

                    if not remaining_letters:

                        # Mark word as panagram if it uses all puzzle letters
                        if not mutable_puzzle_letters:

                            panagrams.append(word)
                            words.append(word)
                            word_index += 1

                        else:
                            words.append(word)
                            word_index += 1

                    # Disregard word if it contains a letter not in the puzzle
                    else:
                        pass

                else:
                    word_index += 1

    # Return if puzzle letters can form panagram
    if panagrams:

        this_puzzles_data = [this_puzzle, words, panagrams, center_letter]
        return this_puzzles_data

    # Return base case if puzzle letters do not form panagram
    else:

        if loading_messages:
            current_message = random.choice(loading_messages)
            print(current_message)
            loading_messages.remove(current_message)

        return generate_game()


# Check if a word is a panagram for the given puzzle letters
def is_word_panagram(word, letters):

    unused_letters = letters.copy()

    for char in word:
        if char in unused_letters:
            unused_letters.remove(char)

    if not unused_letters:
        return True

    else:
        return False


# Get the score of a word for the given puzzle letters
def get_score(word, letters):

    if len(word) == 4:
        return 1

    elif is_word_panagram(word, letters):
        return len(word) * 2

    else:
        return len(word)


# Control UI for initiating a new game
def initialize_game(this_puzzle, words, center_letter):

    point_values = 0

    print('\nSuccessfully generated a game!\n')
    print('This games letters are: ', *this_puzzle, sep=' ')
    print('And the center letter is: ', center_letter)

    for word in words:
        point_values += get_score(word, this_puzzle)

    print('The total number of possible points is: ' + str(point_values) + '\n')

    return point_values


# Track data for current game
this_puzzle, words, panagrams, center_letter = generate_game()
point_values = initialize_game(this_puzzle, words, center_letter)
correct_words, correct_panagrams = [], []
current_score = 0


# Run in command line until force quit
while True:

    try:

        inputted_value = input('--> Enter a word or command: ')

        # Valid word
        if inputted_value in words:

            correct_words.append(inputted_value)
            points = get_score(inputted_value, this_puzzle)
            current_score += points

            if is_word_panagram(inputted_value, this_puzzle):
                correct_panagrams.append(inputted_value)
                print('\nPanagram!')

            print('\n+' + str(points) + ' points!')
            print('Total score is ' + str(current_score) + '\n')

        else:

            # Found all words
            if current_score == point_values:
                print('\nCongratulations! You have found all words possible for this puzzle.')
                print('Enter N to start new game.\n')

            # Hidden command to get valid words
            elif inputted_value =='a' or inputted_value =='A':
                print(words)

            # Quit game
            elif inputted_value == 'q' or inputted_value == 'Q':
                print('\nGame over!\n')
                break

            # View controls
            elif inputted_value == 'c' or inputted_value == 'C':
                print('\nThe controls for this game are as follows:\n')
                print('Enter S for score info')
                print('Enter W to see correct words')
                print('Enter L for puzzle letters')
                print('Enter C for controls')
                print('Enter N to start new game')
                print('Enter Q to quit game\n')

            # Shuffle letters
            elif inputted_value == 'l' or inputted_value == 'L':
                random.shuffle(this_puzzle)
                print('\nThis puzzles letters are:', *this_puzzle, sep=' ')
                print('And the center letter is: ' + str(center_letter) + '\n')

            # Check score
            elif inputted_value == 's' or inputted_value == 'S':
                print('\nYou have found ' + str(len(correct_words)) + ' words out of ' + str(len(words)) + ' total possible words')
                print('You have scored ' + str(current_score) + ' points out of ' + str(point_values) + ' total possible points')
                print('You have found ' + str(len(correct_panagrams)) + ' panagrams out of ' + str(len(panagrams)) + ' total possible panagrams\n')

            # See found words
            elif inputted_value == 'w' or inputted_value == 'W':
                print('\nThe words you have found thus far are:\n')
                print(*correct_words, sep='\n')

            # New game
            elif inputted_value == 'n' or inputted_value == 'N':
                this_puzzle, words, panagrams, center_letter = generate_game()
                point_values = initialize_game(this_puzzle, words, center_letter)
                correct_words, correct_panagrams, current_score = [], [], 0

            elif len(inputted_value) < 4:
                print('\nToo short\n')

            elif center_letter not in inputted_value:
                print('\nMissing center letter\n')

            else:
                print('\nInvalid word\n')

    except:
        break
