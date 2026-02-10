import random

LINES = [
    "A shadow moves where no one is watching.",
    "Someone lies. Someone listens.",
    "The night breathes quietly.",
    "Fear grows louder in silence.",
    "Not everyone here is innocent.",
    "Darkness remembers your name."
]


def whisper():
    return random.choice(LINES)
