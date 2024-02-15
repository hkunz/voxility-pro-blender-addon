import string
import random

def randomize_string(length: int=10):
    characters = string.ascii_letters + string.digits
    str = ''.join(random.choice(characters) for _ in range(length))
    return str
