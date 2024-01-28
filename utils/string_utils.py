import string
import random

def randomize_string():
    characters = string.ascii_letters + string.digits
    str = ''.join(random.choice(characters) for _ in range(10))
    return str
