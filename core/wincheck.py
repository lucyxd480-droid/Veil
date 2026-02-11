"""
Win condition checker.
Determines if either faction has won.
"""

from core.roles import EVIL
from core.state import games


def check_win(chat_id):
    """Return 'innocents', 'traitors', or None."""

    game = games.get(chat_id)
    if not game or not game.get("started"):
        return None

    alive = set(game.get("alive", set()))
    roles = game.get("roles", {})

    if not alive:
        return None  # Safety guard

    evil_alive = {uid for uid in alive if roles.get(uid) in EVIL}
    good_alive = alive - evil_alive

    # Good wins if no evil remains
    if not evil_alive:
        return "innocents"

    # Evil wins if equal or majority
    if len(evil_alive) >= len(good_alive):
        return "traitors"

    return None
