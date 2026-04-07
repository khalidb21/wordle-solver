# solver.py
# Uses information theory (entropy) to select optimal guesses based on feedback patterns, and dynamically narrows down the 
# candidate pool as the game progresses

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
    # Uses guess and target to calculate feedback pattern (green/yellow/gray) for each letter
    # Ex. feedback = ("green", "gray", "yellow", "gray", "yellow")
    def get_feedback_pattern(self, guess, target):
        
        # No need to caculate feedback if we've already seen this guess-target pair, just return the cached 
        key = (guess, target)
        if key in self.pattern_cache:
            return self.pattern_cache[key]

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

    # Entropy calculation for a guess
    # Used with list of possible words to calculate the expected information gain when guessing
    # Entropy is used to measure the expected information gain from a guess\
    def calculate_entropy(self, guess, words):
        pattern_counts = defaultdict(int)

        for target in words:
            pattern = self.get_feedback_pattern(guess, target)
            pattern_counts[pattern] += 1

        total = len(words)
        entropy = 0

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
        if len(possible_words) > 100:
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
