# solver.py
# Uses information theory (entropy) to select optimal guesses based on feedback patterns, and dynamically narrows down the 
# candidate pool as the game progresses
# Input: list of possible words to guess, feedback patterns to filter list (green/yellow/gray)
# Output: best guess based on entropy, and filtered list of possible words

import math
from collections import defaultdict
from words import WORD_LIST


class WordleSolver:

    # First initialize the solver with input of word list
    def __init__(self, word_list=None):
        
        # Two lists: one for the current possible words, and a full list for reference when calculating entropy
        self.possible_words = word_list or WORD_LIST
        self.all_words = self.possible_words.copy()

        # Cache for previously calculated feedback patterns
        self.pattern_cache = {}

    # Feedback pattern calculation with caching
    # Uses guess and target word (unknown) to calculate feedback pattern (green/yellow/gray) for each letter
    # Ex. feedback = ("green", "gray", "yellow", "gray", "yellow")
    def get_feedback_pattern(self, guess, target):
        
        # No need to caculate feedback if we've already seen this guess-target pair, just return the cached 
        key = (guess, target)
        if key in self.pattern_cache:
            return self.pattern_cache[key]

        # Fill the tuple with "gray" by default, then update to "green" and "yellow" as needed
        result = ["gray"] * 5
        target_chars = list(target)

        # First pass: greens
        for i in range(5):
            if guess[i] == target[i]:
                result[i] = "green"
                target_chars[i] = None

        # Second pass: yellows
        for i in range(5):
            if result[i] == "gray" and guess[i] in target_chars:
                result[i] = "yellow"
                target_chars[target_chars.index(guess[i])] = None

        self.pattern_cache[key] = tuple(result)
        return self.pattern_cache[key]

    # Filtering possible words based on feedback
    # Returns a list of words that would produce the same feedback pattern if guessed
    def filter_words(self, guess, feedback, words):
        return [
            word for word in words
            if self.get_feedback_pattern(guess, word) == feedback
        ]

    # Entropy calculation for a guess - Used with list of possible words to calculate the expected information gain when guessing
    # Entropy: average level of expected information gain from a guess using possible words as target pool
    # Measured in bits - 1 bit would cut the possible candidate pool in half, 2 bits would cut it to a quarter, etc.
    def calculate_entropy(self, guess, words):

        # this dictionary works as a bucket to group words based on colour patterns
        pattern_counts = defaultdict(int)

        for candidate in words:
            pattern = self.get_feedback_pattern(guess, candidate)
            pattern_counts[pattern] += 1

        # number of possible target words, used to calculate probabilities for each feedback pattern
        total = len(words)
        entropy = 0

        # Shannon Entropy formula: H(X) = -Σ p(x) log2 p(x)
        # p is probability of each feedback pattern
        for count in pattern_counts.values():
            p = count / total
            entropy -= p * math.log2(p)

        return entropy

    # This is the main solving function
    # Best guess selection based on maximum entropy
    def get_best_guess(self, possible_words):
        if len(possible_words) == 1:
            return possible_words[0]

        # Dynamic candidate reduction
        # switch to only possible answers to prioritize a winning guess as the pool shrinks
        # number is abitrary
        if len(possible_words) > 50:
            candidates = self.all_words
        else:
            candidates = possible_words

        best_word = None
        best_entropy = -1

        for candidate in candidates:
            entropy = self.calculate_entropy(candidate, possible_words)

            if entropy > best_entropy:
                best_entropy = entropy
                best_word = candidate

        return best_word

    # Get words with highest entropy for display
    # Returns a list of tuples (word, entropy) for the top n guesses based on their entropy values
    def get_top_guesses(self, possible_words, n=5):
        ranked_guesses = []

        for word in self.all_words:
            entropy = self.calculate_entropy(word, possible_words)
            ranked_guesses.append((word, entropy))

        ranked_guesses.sort(key=lambda x: x[1], reverse=True)
        return ranked_guesses[:n]
