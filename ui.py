import pygame
from user_actions import handle_key, check_guess, set_tuples
from words import get_random_word

pygame.init()

WIDTH, HEIGHT = 500, 800
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

green, yellow, grey = [], [], []

# Reset function
def reset_game():
    return {
        "target_word": get_random_word(),
        "guesses": [],
        "feedback": [],
        "current_guess": "",
        "letter_status": {},
    }

game = reset_game()
print("Target word:", game["target_word"])  # debug

running = True

while running:
    screen.fill((255, 255, 255))

    # Restart button (define each frame)
    button_rect = pygame.Rect(150, 730, 200, 40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard input
        if event.type == pygame.KEYDOWN:
            game["current_guess"], submitted = handle_key(event, game["current_guess"])

            if submitted and len(game["guesses"]) < 6:
                guess = game["current_guess"]
                game["guesses"].append(guess)

                result = check_guess(guess, game["target_word"])
                green, yellow, grey = set_tuples(guess, game["target_word"], green, yellow, grey)
                print("Green:", green)
                print("Yellow:", yellow)
                print("Grey:", grey)
                game["feedback"].append(result)

                # Update letter status
                for i, letter in enumerate(guess):
                    color = result[i]

                    if letter not in game["letter_status"]:
                        game["letter_status"][letter] = color
                    else:
                        if color == "green":
                            game["letter_status"][letter] = "green"
                        elif color == "yellow" and game["letter_status"][letter] != "green":
                            game["letter_status"][letter] = "yellow"

                # Win/Lose messages
                if guess == game["target_word"]:
                    print("You win!")
                elif len(game["guesses"]) == 6:
                    print("You lose! Word was:", game["target_word"])

                game["current_guess"] = ""

        # Mouse click (restart)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                game = reset_game()
                print("New word:", game["target_word"])
                green, yellow, grey = [], [], []

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
    start_y = HEIGHT - 220

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

    # Draw restart button
    pygame.draw.rect(screen, (180, 180, 180), button_rect)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)

    button_text = SMALL_FONT.render("Restart", True, (0, 0, 0))
    screen.blit(button_text, (button_rect.x + 50, button_rect.y + 5))

    pygame.display.update()

pygame.quit()