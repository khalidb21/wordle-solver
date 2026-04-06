from words import get_word_list
from user_actions import check_guess


class MinimaxSolver:
    def __init__(self):
        self.all_words = get_word_list()
        self.possible_words = self.all_words.copy()

    def get_feedback_pattern(self, guess, target):
        return tuple(check_guess(guess, target))

    def filter_possible_words(self, guess, feedback):
        self.possible_words = [
            word for word in self.possible_words
            if tuple(check_guess(guess, word)) == tuple(feedback)
        ]

    def score_guess(self, guess):
        partitions = {}

        for target in self.possible_words:
            pattern = self.get_feedback_pattern(guess, target)
            partitions[pattern] = partitions.get(pattern, 0) + 1

        return max(partitions.values())

    def best_guess(self):
        best_word = None
        best_score = float("inf")

        for guess in self.possible_words:  # faster than all_words
            score = self.score_guess(guess)
            if score < best_score:
                best_score = score
                best_word = guess

        return best_word

    def next_guess(self, last_guess=None, last_feedback=None):
        if last_guess and last_feedback:
            self.filter_possible_words(last_guess, last_feedback)

        return self.best_guess()