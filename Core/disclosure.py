import random

MESSAGES = [
    "Some trust was misplaced.",
    "Silence shifted the balance.",
    "A betrayal went unnoticed.",
    "Belief moved, but truth remained hidden.",
    "The Veil tightened."
]

def disclosure():
    return random.choice(MESSAGES)
