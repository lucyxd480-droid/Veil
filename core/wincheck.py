from core.state import game


def check_win():
    """
    Basic win condition:
    - Traitors win if innocents <= traitors
    - Innocents win if no traitor alive
    """

    alive = game.get("alive", [])
    roles = game.get("roles", {})

    traitors = [u for u in alive if roles.get(u) in ["traitor", "assassin", "cultist", "zealot"]]
    innocents = [u for u in alive if roles.get(u) not in ["traitor", "assassin", "cultist", "zealot"]]

    if not traitors:
        return "innocents"

    if len(traitors) >= len(innocents):
        return "traitors"

    return None
