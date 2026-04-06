import math
from collections import defaultdict
from words import WORD_LIST


class WordleSolver:
    def __init__(self, word_list=None):
        self.possible_words = word_list or WORD_LIST
        self.all_words = self.possible_words.copy()

        # Cache for (guess, target) → feedback
        self.pattern_cache = {}

    # Feedback pattern calculation with caching
    def get_feedback_pattern(self, guess, target):
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
    def filter_words(self, guess, feedback, words):
        return [
            word for word in words
            if self.get_feedback_pattern(guess, word) == feedback
        ]

    # Entropy calculation for a guess
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

    # Main solving loop to demonstrate the solver's capabilities
    def solve(self, target_word, verbose=True):
        possible_words = self.possible_words.copy()

        for attempt in range(6):
            guess = self.get_best_guess(possible_words)

            if guess is None:
                print("No valid words left!")
                return -1

            feedback = self.get_feedback_pattern(guess, target_word)

            if verbose:
                print(f"Attempt {attempt + 1}: {guess.upper()}")
                print(f"  Feedback: {feedback}")
                print(f"  Remaining: {len(possible_words)}")

            if guess == target_word:
                if verbose:
                    print(f"✓ Solved in {attempt + 1} guesses!")
                return attempt + 1

            possible_words = self.filter_words(guess, feedback, possible_words)

            if verbose and len(possible_words) <= 10:
                print(f"  Candidates: {possible_words}")
                print()

        print(f"✗ Failed. Target was: {target_word}")
        return -1

    # Get words with highest entropy for display
    def get_top_guesses(self, possible_words, n=5):
        results = []

        for word in self.all_words:
            entropy = self.calculate_entropy(word, possible_words)
            results.append((word, entropy))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:n]


# Test demo for the solver
def demo():
    import random

    solver = WordleSolver()
    target = random.choice(solver.possible_words)

    print("=" * 50)
    print("WORDLE SOLVER DEMO (Optimized)")
    print("=" * 50)
    print("Target word is hidden...\n")

    solver.solve(target)

    print("\nActual word:", target.upper())


if __name__ == "__main__":
    demo()