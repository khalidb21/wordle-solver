# user_actions.py

def check_guess(guess, target):
    result = ["gray"] * 5
    target_list = list(target)

    # Green pass
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = "green"
            target_list[i] = None

    # Yellow pass
    for i in range(5):
        if result[i] == "gray" and guess[i] in target_list:
            result[i] = "yellow"
            target_list[target_list.index(guess[i])] = None

    return result


def handle_key(event, current_guess):
    if event.key == 8:  # backspace
        return current_guess[:-1], False

    elif event.key == 13:  # enter
        if len(current_guess) == 5:
            return current_guess, True
        return current_guess, False

    else:
        if len(current_guess) < 5 and event.unicode.isalpha():
            return current_guess + event.unicode.lower(), False

    return current_guess, False