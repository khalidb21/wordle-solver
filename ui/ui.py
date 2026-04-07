import pygame
from ui.user_actions import handle_key, check_guess
from words import get_random_word
from solver import WordleSolver

pygame.init()

WIDTH, HEIGHT = 500, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")

FONT = pygame.font.SysFont(None, 48)
SMALL_FONT = pygame.font.SysFont(None, 36)

ROWS, COLS = 6, 5
CELL_SIZE = 60
MARGIN = 10

COLORS = {
    "gray": (120, 120, 120),
    "yellow": (200, 180, 0),
    "green": (0, 180, 0),
    "empty": (200, 200, 200)
}


def reset_game():
    solver = WordleSolver()
    return {
        "target_word": get_random_word(),
        "guesses": [],
        "feedback": [],
        "current_guess": "",
        "letter_status": {},
        "solver": solver,
        "possible_words": solver.possible_words.copy(),
        "ai_mode": False,
        "last_guess": None,
        "last_feedback": None,
        "ai_thinking": False
    }


game = reset_game()
print("Target word:", game["target_word"])

clock = pygame.time.Clock()

AI_DELAY = 500
last_ai_time = 0

running = True

while running:
    screen.fill((255, 255, 255))

    restart_button = pygame.Rect(50, 780, 150, 40)
    ai_button = pygame.Rect(300, 780, 150, 40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Manual input
        if event.type == pygame.KEYDOWN and not game["ai_mode"]:
            game["current_guess"], submitted = handle_key(event, game["current_guess"])

            if submitted and len(game["guesses"]) < 6:
                guess = game["current_guess"]
                result = check_guess(guess, game["target_word"])

                game["guesses"].append(guess)
                game["feedback"].append(result)

                # update keyboard colors
                for i, letter in enumerate(guess):
                    color = result[i]
                    if letter not in game["letter_status"]:
                        game["letter_status"][letter] = color
                    else:
                        if color == "green":
                            game["letter_status"][letter] = "green"
                        elif color == "yellow" and game["letter_status"][letter] != "green":
                            game["letter_status"][letter] = "yellow"

                game["current_guess"] = ""

        # Buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                game = reset_game()
                print("New word:", game["target_word"])

            if ai_button.collidepoint(event.pos):
                game["solver"] = WordleSolver()
                game["possible_words"] = game["solver"].possible_words.copy()
                game["ai_mode"] = True
                game["last_guess"] = None
                game["last_feedback"] = None
                game["ai_thinking"] = True

    # AI step
    if game["ai_mode"] and len(game["guesses"]) < 6:
        current_time = pygame.time.get_ticks()

        if current_time - last_ai_time > AI_DELAY:
            last_ai_time = current_time
            game["ai_thinking"] = True

            solver = game["solver"]

            # Step 1: pick best guess
            guess = solver.get_best_guess(game["possible_words"])

            # Step 2: compute feedback
            result = solver.get_feedback_pattern(guess, game["target_word"])

            # Step 3: filter possible words
            game["possible_words"] = solver.filter_words(
                guess,
                result,
                game["possible_words"]
            )

            # Step 4: store guess
            game["guesses"].append(guess)
            game["feedback"].append(result)

            # update keyboard colors
            for i, letter in enumerate(guess):
                color = result[i]
                if letter not in game["letter_status"]:
                    game["letter_status"][letter] = color
                else:
                    if color == "green":
                        game["letter_status"][letter] = "green"
                    elif color == "yellow" and game["letter_status"][letter] != "green":
                        game["letter_status"][letter] = "yellow"

            game["last_guess"] = guess
            game["last_feedback"] = result
            game["ai_thinking"] = False

            if guess == game["target_word"]:
                print("AI solved it!")
                game["ai_mode"] = False
            elif len(game["guesses"]) == 6:
                print("AI failed! Word was:", game["target_word"])
                game["ai_mode"] = False

    # Draw grid
    for row in range(ROWS):
        for col in range(COLS):
            x = col * (CELL_SIZE + MARGIN) + 50
            y = row * (CELL_SIZE + MARGIN) + 50

            color = COLORS["empty"]
            letter = ""

            if row < len(game["guesses"]):
                color = COLORS[game["feedback"][row][col]]
                letter = game["guesses"][row][col]
            elif row == len(game["guesses"]) and col < len(game["current_guess"]):
                letter = game["current_guess"][col]

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 2)

            if letter:
                text = FONT.render(letter.upper(), True, (0, 0, 0))
                screen.blit(text, (x + 18, y + 10))

    # Draw keyboard
    keyboard_rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    start_y = HEIGHT - 260

    for row_index, row in enumerate(keyboard_rows):
        for col_index, letter in enumerate(row):
            x = col_index * 40 + (WIDTH - len(row) * 40) // 2
            y = start_y + row_index * 50

            color = COLORS["empty"]
            if letter in game["letter_status"]:
                color = COLORS[game["letter_status"][letter]]

            pygame.draw.rect(screen, color, (x, y, 35, 40))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 35, 40), 2)

            text = SMALL_FONT.render(letter.upper(), True, (0, 0, 0))
            screen.blit(text, (x + 5, y + 5))

    # Restart button
    pygame.draw.rect(screen, (180, 180, 180), restart_button)
    pygame.draw.rect(screen, (0, 0, 0), restart_button, 2)
    screen.blit(SMALL_FONT.render("Restart", True, (0, 0, 0)), (restart_button.x + 30, restart_button.y + 5))

    # AI button
    pygame.draw.rect(screen, (150, 200, 150), ai_button)
    pygame.draw.rect(screen, (0, 0, 0), ai_button, 2)
    screen.blit(SMALL_FONT.render("Solve AI", True, (0, 0, 0)), (ai_button.x + 20, ai_button.y + 5))

    # AI thinking text
    if game["ai_thinking"]:
        screen.blit(SMALL_FONT.render("AI Thinking...", True, (0, 0, 0)), (170, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()