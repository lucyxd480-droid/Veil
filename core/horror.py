import random


HORROR_LINES = [
    "You feel watched.",
    "Your thoughts are not yours.",
    "Someone knows your secret.",
    "The darkness remembers you.",
]


def horror():
    return random.choice(HORROR_LINES)
