# solver_cli.py
# Command-line interface for demonstrating the WordleSolver
# Options: 1) Watch the solver solve a random word, 2) Show best starting words based on entropy, 3) Solve a user-provided word, 4) Exit

from solver import WordleSolver
from words import get_random_word, WORD_LIST

# display guess with colored feedback symbols (green/yellow/gray) for each letter
def display_feedback(guess, feedback):
    feedback_symbols = {
        "green": "🟩",
        "yellow": "🟨",
        "gray": "⬜"
    }

    return " ".join(
        f"{letter}{feedback_symbols.get(color, '❓')}"
        for letter, color in zip(guess.upper(), feedback)
    )

# Attempts to solve a random target word, showing the process step-by-step
def solver_solves_random():
    solver = WordleSolver()
    target = get_random_word()

    print("\n" + "=" * 60)
    print("SOLVER DEMONSTRATION (Random Word)")
    print("=" * 60)
    print()

    possible_words = solver.possible_words.copy()

    for attempt in range(6):
        guess = solver.get_best_guess(possible_words)
        feedback = solver.get_feedback_pattern(guess, target)

        print(f"Attempt {attempt + 1}: {guess.upper()}")
        print(display_feedback(guess, feedback))

        if guess == target:
            print(f"\n✓ Solved in {attempt + 1} guesses!")
            return

        possible_words = solver.filter_words(guess, feedback, possible_words)

        print(f"Remaining possibilities: {len(possible_words)}")
        print()

    print(f"✗ Failed! Target was: {target.upper()}")

# Attempts to solve a user-provided target word, showing the process step-by-step
def solver_solves_user_word():
    solver = WordleSolver()

    while True:
        user_word = input("Enter a 5-letter target word: ").strip().lower()
        if len(user_word) != 5:
            print("Word must be exactly 5 letters. Try again.")
        elif user_word not in WORD_LIST:
            print("Word not in valid word list. Try again.")
        else:
            break

    print("\n" + "=" * 60)
    print(f"SOLVER DEMONSTRATION (Target: {user_word.upper()})")
    print("=" * 60)
    print()

    possible_words = solver.possible_words.copy()

    for attempt in range(6):
        guess = solver.get_best_guess(possible_words)
        feedback = solver.get_feedback_pattern(guess, user_word)

        print(f"Attempt {attempt + 1}: {guess.upper()}")
        print(display_feedback(guess, feedback))

        if guess == user_word:
            print(f"\n✓ Solved in {attempt + 1} guesses!")
            return

        possible_words = solver.filter_words(guess, feedback, possible_words)

        print(f"Remaining possibilities: {len(possible_words)}")
        print()

    print(f"✗ Failed! Target was: {user_word.upper()}")


# Display best starting words based on their entropy values + expected remaining candidates after the first guess
def show_best_starting_words():
    solver = WordleSolver()

    print("\n" + "=" * 60)
    print("TOP STARTING WORDS (By Entropy)")
    print("=" * 60)
    print()
    print("These words provide the most information for the first guess.\n")

    top_guesses = solver.get_top_guesses(solver.possible_words, n=10)
    total_words = len(solver.possible_words)

    for i, (word, entropy) in enumerate(top_guesses, 1):
        expected_remaining = total_words / (2 ** entropy)
        print(
            f"{i:2d}. {word.upper():<10} | "
            f"Entropy: {entropy:.4f} bits | "
            f"Expected remaining: {expected_remaining:.1f} words"
        )

    print()


def main():
    # Main menu loop for user interaction
    while True:
        print("\n" + "=" * 60)
        print("WORDLE SOLVER - Information Theory Edition")
        print("=" * 60)
        print("1. Watch solver solve a random word")
        print("2. Show best starting words")
        print("3. Solve a word you provide")
        print("4. Exit")
        print()

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            solver_solves_random()
        elif choice == "2":
            show_best_starting_words()
        elif choice == "3":
            solver_solves_user_word()
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()