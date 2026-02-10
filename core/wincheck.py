from core.state import games


def check_win(chat_id):
    """
    Win conditions per group (chat)
    """

    game = games.get(chat_id)
    if not game:
        return None

    alive = game.get("alive", [])
    roles = game.get("roles", {})

    evil_roles = ["traitor", "assassin", "cultist", "zealot", "mindbreaker"]

    traitors = [u for u in alive if roles.get(u) in evil_roles]
    innocents = [u for u in alive if roles.get(u) not in evil_roles]

    if not traitors:
        return "innocents"

    if len(traitors) >= len(innocents):
        return "traitors"

    return None
