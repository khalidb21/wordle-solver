# words.py
import random
from wordfreq import top_n_list

# Keep words that are only 5 letters long and contain only alphabetic characters
def get_word_list():
    words = top_n_list("en", 10000)
    return [w for w in words if len(w) == 5 and w.isalpha()]

WORD_LIST = get_word_list()

def get_random_word():
    return random.choice(WORD_LIST)